import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'your_username'),
    'password': os.getenv('DB_PASSWORD', 'your_password'),
    'database': os.getenv('DB_NAME', 'your_database'),
    'port': int(os.getenv('DB_PORT', 3306))
}

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

COMPANY_NAME = os.getenv('COMPANY_NAME', 'Your Company')
COMPANY_DESCRIPTION = os.getenv('COMPANY_DESCRIPTION', 'A leading company in innovation and technology')
