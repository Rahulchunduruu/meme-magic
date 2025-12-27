import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

class Config:    
    #GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env file. Please add your API key.")
