import os
import time
from dotenv import load_dotenv
from google import genai

# Load .env for local development
load_dotenv()

# Try environment variable first (local .env), then fall back to Streamlit secrets (cloud)
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        import streamlit as st
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

client = genai.Client(api_key=API_KEY)



def create_prompt(
    budget,
    days,
    interest,
    city,
    attractions
):
    """
    Creates a prompt for Gemini.
    """

    return f"""
You are an expert travel planner.

Create a detailed {days}-day travel itinerary.

City: {city}

Interest: {interest}

Budget: ₹{budget}

Recommended Attractions:
{', '.join(attractions)}

Instructions:

1. Make a day-wise itinerary.
2. Include timings.
3. Suggest breakfast, lunch and dinner.
4. Suggest local transport.
5. Give approximate spending.
6. Keep the itinerary within budget.
7. Add student travel tips.
8. Use headings and bullet points.
"""


def generate_itinerary(prompt):
    """
    Generates itinerary using Gemini with retry logic.
    """

    retries = 3

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except Exception:

            if attempt < retries - 1:
                time.sleep(5)
            else:
                return """
⚠️ Gemini is currently busy or the free quota has been exceeded.

Your recommendations have been generated successfully.

Please try generating the AI itinerary again after a few seconds.
"""