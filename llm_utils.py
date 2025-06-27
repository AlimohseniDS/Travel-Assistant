
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from google.generativeai import configure as gemini_configure, GenerativeModel as GeminiModel
from dotenv import load_dotenv
import googlemaps
# === Load environment variables
load_dotenv()
TP_API_TOKEN = os.getenv("TRAVELPAYOUTS_API_KEY")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
amadeus_token = None


# === Load Mistral-7B model
model_path = "/mnt/shared/Sayedali/mistral"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map="auto",
    trust_remote_code=True
)
text_generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=2048,
    do_sample=True,
    temperature=0.7,
    top_p=0.95
)

from google.generativeai import configure as gemini_configure, GenerativeModel as GeminiModel

# Load Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    gemini_configure(api_key=GEMINI_API_KEY)
    gemini_model = GeminiModel("gemini-1.5-pro")
else:
    gemini_model = None

def generate_with_gemini(prompt):
    if not gemini_model:
        return "❌ Gemini API key not configured."
    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Gemini API Error: {e}"


def generate_itinerary(prompt, model_choice="Local"):
    if model_choice == "Remote":
        print("🌐 Using Gemini API (remote)")
        return generate_with_gemini(prompt)  # Call Gemini API function
    else:
        print("🖥️ Using Mistral-7B (local)")
        result = text_generator(prompt)[0]["generated_text"]  # Local generation
        return result.strip()