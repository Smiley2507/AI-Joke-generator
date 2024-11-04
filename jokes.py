import google.generativeai as genai
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

# Rate limiting variables
last_request_time = datetime.now()
MIN_REQUEST_INTERVAL = timedelta(seconds=1)

# Cache for previously generated jokes
joke_cache = set()
MAX_CACHE_SIZE = 1000

def generate_joke():
    """Generate a joke using the Gemini API with rate limiting and caching"""
    global last_request_time

    # Rate limiting check
    current_time = datetime.now()
    if current_time - last_request_time < MIN_REQUEST_INTERVAL:
        raise Exception("Please wait a moment before generating another joke")

    # Configure the model
    model = genai.GenerativeModel('gemini-pro')
    
    # Prompt engineering for better jokes
    prompt = """
    Generate a short, funny joke that's trending on social medias like X.
    No lame jokes, include dad-jokes if possible.
    The joke should be:
    - Family-friendly
    - Easy to understand
    - Not offensive
    - Preferably related to modern topics (technology, social media, etc.)
    Just return the joke itself, no additional text.
    """

    try:
        response = model.generate_content(prompt)
        joke = response.text.strip()

        # Check for duplicate jokes with 0.3% probability of allowing repeats
        if joke in joke_cache and random.random() > 0.003:
            return generate_joke()  # Recursively try again

        # Cache management
        joke_cache.add(joke)
        if len(joke_cache) > MAX_CACHE_SIZE:
            joke_cache.clear()  # Reset cache when it gets too large

        last_request_time = current_time
        return joke

    except Exception as e:
        return f"Sorry, I couldn't generate a joke right now. Error: {str(e)}"