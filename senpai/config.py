import os
from dotenv import load_dotenv

load_dotenv()

# App configuration
INITIAL_OBJECTIVE = os.getenv("INITIAL_OBJECTIVE")

OPENAI_MODEL= os.getenv("OPENAI_MODEL")
FAST_OPENAI_MODEL= os.getenv("FAST_OPENAI_MODEL")

GOOGLE_LOCATION=os.getenv("GOOGLE_LOCATION")
GOOGLE_LANGUAGE_CODE=os.getenv("GOOGLE_LANGUAGE_CODE")
GOOGLE_COUNTRY_CODE=os.getenv("GOOGLE_COUNTRY_CODE")

# Auth creds
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERP_API_KEY=os.getenv("SERP_API_KEY")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
