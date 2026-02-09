import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    MODEL_NAME = "llama-3.3-70b-versatile"
    
    @staticmethod
    def validate():
        if not Config.GROQ_API_KEY:
            raise ValueError("Missing GROQ_API_KEY")