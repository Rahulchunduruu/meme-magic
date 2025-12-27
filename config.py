import os
from dotenv import load_dotenv

# Load .env from parent directory
#env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv()

class Config:    
    GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
    GEMINI_API_KEY1=os.getenv('GEMINI_API_KEY1')
    GEMINI_API_KEY2=os.getenv('GEMINI_API_KEY2')
    GEMINI_API_KEY3=os.getenv('GEMINI_API_KEY3')
    GEMINI_API_KEY4=os.getenv('GEMINI_API_KEY4')
