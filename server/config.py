import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\xb7\x94x\x8c\x96\x96C.\xd4D%e/V\x86\xa6SJ\x8f\xb0=\x02\x19P'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
SERVER_ROOT = pathlib.Path(__file__).resolve().parent
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
