import server
from scipy.spatial.distance import cosine
from flask import session, request
from flask_socketio import disconnect
import boto3
from botocore.config import Config
import jwt
import requests
from bs4 import BeautifulSoup
import json
import openai
import MySQLdb.cursors
from datetime import datetime, date
import os


# Database cursor interface
class Cursor:
    def __init__(self):
        self.cursor = server.db.connection.cursor(MySQLdb.cursors.DictCursor)
    
    def execute(self, sql, argsdict):
        self.cursor.execute(sql, argsdict)

    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()
    
    def lastrowid(self):
        return self.cursor.lastrowid
    
    def close(self):
        self.cursor.close()

    def rowcount(self):
        return self.cursor.rowcount
    
    def rollback(self):
        server.db.connection.rollback()
    
    def __del__(self):
        server.db.connection.commit()
        self.cursor.close()

# Web socket interface
class Socket:
    def __init__(self):
        self.socket = server.sio

    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            return super().default(obj)

    def emit(self, event, data):
        self.socket.emit(event, json.loads(json.dumps(data, cls=self.CustomJSONEncoder)))

class AWSClient:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            region_name=os.getenv("AWS_REGION", "us-east-2"),
            config=Config(signature_version='s3v4')
        )

    def generate_presigned_url(self, intention, file_key, file_type):
        params = {
            "Bucket": os.getenv("S3_BUCKET_NAME"),
            "Key": file_key,
        }
        if intention == "put_object":
            params["ContentType"] = file_type

        return self.s3.generate_presigned_url(
            intention,
            params,
            ExpiresIn=3600
        )

    def delete_object(self, key):
        self.s3.delete_object(
            Bucket=os.getenv('S3_BUCKET_NAME'),
            Key=key
        )

    def copy_object(self, key, new_key):
        self.s3.copy_object(
            Bucket=os.getenv("S3_BUCKET_NAME"),
            CopySource={"Bucket": os.getenv("S3_BUCKET_NAME"), "Key": key},
            Key=new_key
        )

    def move_object(self, key, new_key):
        self.copy_object(key, new_key)
        self.delete_object(key)

    def delete_uploaded_objects(self, keys):
        self.create_invalidation(keys)
        for key in keys:
            self.delete_object(key)

# OpenAI chatbot interface
class Chatbot:
    def __init__(self):
        # Load precomputed content embeddings (one-time operation)
        # self.content_embeddings = self.load_embeddings_from_database()
        openai.api_key = server.secret.OPENAI_API_KEY

        # Crawl website and generate embeddings
        self.create_embeddings()

        # Load embeddings from JSON file
        self.content_embeddings = self.load_embeddings_from_json()

    # Crawling and embedding methods
    def create_embeddings(self):
        pages_content = self.crawl_website()
        embeddings = self.generate_embeddings(pages_content)
        self.save_embeddings_to_json(embeddings)

    def scrape_page(self, url):
        """Scrape a single webpage and return the text content."""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract text from paragraph tags or specific sections
        page_text = " ".join([p.get_text() for p in soup.find_all('p')])
        
        return page_text

    def crawl_website(self):
        """Crawl the website starting from the home URL and collect content."""
        base_url = 'http://localhost:3000/'
        visited = set()
        to_visit = [
            'http://localhost:3000/',
            'http://localhost:3000/urgent-care/info/acute-conditions/cold-flu'
        ]
        pages_content = {}

        while to_visit:
            url = to_visit.pop(0)
            if url not in visited:
                visited.add(url)
                page_content = self.scrape_page(url)
                pages_content[url] = page_content
                
                # Add more URLs to visit (example: all anchor tags)
                soup = BeautifulSoup(requests.get(url).text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    full_url = requests.compat.urljoin(base_url, link['href'])
                    if full_url not in visited and base_url in full_url:
                        to_visit.append(full_url)

        return pages_content  # Dictionary with URL as keys and content as values

    def split_into_chunks(self, text, max_tokens=300):
        """Split text into chunks based on a token limit (approx. number of words)."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), max_tokens):
            chunks.append(" ".join(words[i:i + max_tokens]))
        return chunks
    
    def generate_embeddings(self, pages_content):
        embeddings = []
        for url, content in pages_content.items():
            chunks = self.split_into_chunks(content)
            for chunk in chunks:
                embedding = self.embed_content(chunk)
                embeddings.append({
                    'url': url,
                    'content': chunk,
                    'embedding': embedding
                })
        return embeddings
    
    # Embedded content storage / retrieval methods
    def save_embeddings_to_json(self, embeddings, filename="embeddings.json"):
        """Save embeddings to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(embeddings, f)

    def load_embeddings_from_json(self, filename="embeddings.json"):
        """Load embeddings from a JSON file."""
        with open(filename, 'r') as f:
            return json.load(f)
    
    # Response methods
    def embed_content(self, text):
        """Create embedding for text using OpenAI API"""
        response = openai.embeddings.create(input=text,
        model="text-embedding-ada-002")
        return response.data[0].embedding

    def find_best_match(self, question_embedding, content_embeddings):
        """Find the most similar content chunk by comparing embeddings"""
        # Each item in content_embeddings should be a dict with 'content' and 'embedding'
        best_match = min(content_embeddings, key=lambda x: cosine(question_embedding, x['embedding']))
        return best_match  # e.g., {'content': '...', 'url': '...', 'embedding': [...]}

    def summarize_content(self, content):
        """Summarize the matched content using GPT (chat-based API)"""
        response = openai.chat.completions.create(
            model="gpt-4o",  # Or "gpt-3.5-turbo" depending on your model
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant of a website of a medical clinic. You provide users with information about the clinic's services and answer their questions, based on the information in the website."
                },
                {"role": "user", "content": f"Summarize this content: {content}"}
            ],
        )
        return response.choices[0].message.content.strip()

    def chatbot_response(self, question):
        """Main logic to process user question"""
        # Embed the user's question
        question_embedding = self.embed_content(question)

        # Find the most similar content on the website
        best_match = self.find_best_match(question_embedding, self.content_embeddings)

        # Summarize the best match
        summary = self.summarize_content(best_match['content'])

        # Provide a link to the full page if needed
        response = {
            'summary': summary,
            'link': best_match['url']  # e.g., link to the full article
        }

        # Store the question in session (optional)
        session['last_question'] = question

        return response