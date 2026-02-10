import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ---------------------------------------------------------
    # 1. RETRIEVE KEYS IMMEDIATELY (Fixes the timing bug)
    # ---------------------------------------------------------
    
    # Try fetching from System Environment first (Local)
    _groq_key = os.getenv("GROQ_API_KEY")
    _tavily_key = os.getenv("TAVILY_API_KEY")
    
    
    if not _groq_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
        _groq_key = st.secrets["GROQ_API_KEY"]
        
    if not _tavily_key and hasattr(st, "secrets") and "TAVILY_API_KEY" in st.secrets:
        _tavily_key = st.secrets["TAVILY_API_KEY"]

    # ---------------------------------------------------------
    # 2. SET THE FINAL VALUES
    # ---------------------------------------------------------
    GROQ_API_KEY = _groq_key
    TAVILY_API_KEY = _tavily_key
    MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

    # ---------------------------------------------------------
    # 3. FORCE ENV VARS (For LangChain compatibility)
    # ---------------------------------------------------------
    if GROQ_API_KEY:
        os.environ["GROQ_API_KEY"] = GROQ_API_KEY
    
    if TAVILY_API_KEY:
        os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

    @staticmethod
    def validate():
        """
        Final check to ensure keys are valid.
        """
        if not Config.GROQ_API_KEY:
            raise ValueError("❌ Missing GROQ_API_KEY. Please set it in Streamlit Secrets.")
        if not Config.TAVILY_API_KEY:
            raise ValueError("❌ Missing TAVILY_API_KEY. Please set it in Streamlit Secrets.")