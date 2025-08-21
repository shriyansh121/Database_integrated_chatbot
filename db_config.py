import os
import streamlit as st 
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': st.secrets["DB_HOST"],
    'user': st.secrets["DB_USER"],
    'password': st.secrets["DB_PASSWORD2"],
    'database': st.secrets["DB_NAME"],
    'port': int(st.secrets["DB_PORT"])
}

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
 
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Your Company')
COMPANY_DESCRIPTION = os.getenv('COMPANY_DESCRIPTION', 'A leading company in innovation and technology')
