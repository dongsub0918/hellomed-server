CREATE TABLE ebdb.carousel_items (
    id SERIAL PRIMARY KEY,
    imageSrc VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    href VARCHAR(255)
);