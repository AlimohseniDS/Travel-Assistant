from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz
from datetime import datetime, timedelta
import os
import re
import json
import pytz
import torch
import requests
import googlemaps
from datetime import datetime, timedelta
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import gradio as gr
from build_prompts import build_prompt

from travel_utils import (
    estimate_flight_time,
    get_cheapest_flight,
    get_hotel_price,
    get_top_restaurants
)

from llm_utils import generate_itinerary, generate_with_gemini, text_generator, gemini_model

# === Load environment variables
load_dotenv()
TP_API_TOKEN = os.getenv("TRAVELPAYOUTS_API_KEY")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
amadeus_token = None

# === User data state
user_data = {
    "name": None, "origin": None, "destination": None,
    "travel_date": None, "return_date": None,
    "budget": None, "special_needs": None,
    "final_itinerary": None, "plan_parts": [], "current_part": None
}
step_order = ["name", "origin", "destination", "travel_date", "return_date", "budget", "special_needs"]

def save_profile():
    if user_data["name"]:
        os.makedirs("profiles", exist_ok=True)
        with open(f"profiles/{user_data['name'].lower()}.json", "w") as f:
            json.dump(user_data, f)

def load_profile(name):
    path = f"profiles/{name.lower()}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None

def validate_input(field, value):
    if field in ["name", "origin", "destination"]:
        return bool(re.fullmatch(r"[A-Za-z ]{2,}", value)), f"❌ Enter a valid {field} (letters only)."
    elif field in ["travel_date", "return_date"]:
        try:
            datetime.strptime(value.strip(), "%d %B %Y")
            return True, ""
        except:
            return False, "❌ Use format like: 5 May 2025"
    elif field == "budget":
        return bool(re.match(r"^\d+(\.\d+)?\s?(AUD|USD|EUR|GBP|dollars)?$", value.strip(), re.IGNORECASE)), "❌ Use format like: 3000 AUD"
    return True, ""


def paginate_text(text, chunk_size=250):
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def assistant_system(user_input, history):
    user_input_clean = user_input.lower().strip()

    # === Reset Logic ===
    if user_input_clean == "reset":
        if user_data.get("name"):
            path = f"profiles/{user_data['name'].lower()}.json"
            if os.path.exists(path):
                os.remove(path)
        for k in user_data:
            user_data[k] = None
        user_data["plan_parts"] = []
        user_data["current_part"] = None
        return "🔄 Profile reset complete. Let's start again.\n\nWhat's your name?"

    # === Handle 'next' ===
    if user_input_clean == "next":
        if user_data.get("plan_parts") and user_data.get("current_part") is not None:
            i = user_data["current_part"] + 1
            if i < len(user_data["plan_parts"]):
                user_data["current_part"] = i
                text = user_data["plan_parts"][i]
                if i + 1 < len(user_data["plan_parts"]):
                    text += "\n\nType 'next' to continue."
                else:
                    text += "\n\n✅ END OF ITINERARY."
                return text
            return "✅ END OF ITINERARY."
        return "⚠️ No itinerary found. Please generate one first."

    # === Step-by-Step Input Collection ===
    for field in step_order:
        if user_data[field] is None:
            valid, msg = validate_input(field, user_input)
            if not valid:
                return msg
            user_data[field] = user_input.strip()
            if field == "name":
                existing = load_profile(user_data["name"])
                if existing:
                    user_data.update(existing)
                    return f"👋 Welcome back {user_data['name']}. Type 'generate plan' or 'reset'."
            prompts = {
                "origin": "What city are you flying from?",
                "destination": "Where would you like to travel?",
                "travel_date": "When will you leave? (e.g., 5 May 2025)",
                "return_date": "When will you return? (e.g., 10 May 2025)",
                "budget": "What’s your budget? (e.g., 3000 AUD)",
                "special_needs": "Any special needs/preferences?"
            }
            next_field = step_order[step_order.index(field) + 1] if step_order.index(field) + 1 < len(step_order) else None
            return prompts.get(next_field, "✅ All set. Type 'generate plan' when you're ready.")

    # === Main Generation Block ===
    if "generate plan" in user_input_clean:
        try:
            save_profile()
            nights = (datetime.strptime(user_data["return_date"], "%d %B %Y") -
                      datetime.strptime(user_data["travel_date"], "%d %B %Y")).days
            if nights < 1:
                return "❌ Return date must be after departure."
            if nights > 90:
                return "❌ Trip too long. Please choose a return date within 90 days."

            flight = get_cheapest_flight(user_data["destination"], user_data["origin"])
            hotel = get_hotel_price(user_data["destination"]) * nights
            budget = float(re.findall(r"\d+", user_data["budget"])[0])
            remaining = budget - flight - hotel

            warning = ""
            if remaining < 0:
                warning = f"⚠️ Warning: Your flight and hotel costs exceed your budget by ~{abs(remaining):.2f} AUD.\n\n"

            restaurants = get_top_restaurants(user_data["destination"])
            if not restaurants:
                restaurants = [{"name": "No restaurants found", "rating": "N/A", "price": "N/A", "address": "N/A"}]

            dep_str, arr_str = estimate_flight_time(user_data["origin"], user_data["destination"], user_data["travel_date"])

            # === Build the original prompt ===
            prompt = build_prompt(user_data, flight, hotel, remaining, dep_str, arr_str, nights, restaurants, warning)

            # === Generate itinerary ===
            generated = generate_itinerary(prompt, user_data.get("model_choice", "Local"))

            # # === Save to CSV ===
            # save_prompts_and_itineraries_to_csv(user_data, flight, hotel, remaining, dep_str, arr_str, nights, restaurants)

            # === Pagination setup ===
            user_data["plan_parts"] = paginate_text(generated)
            user_data["current_part"] = 0

            response = user_data["plan_parts"][0]
            if len(user_data["plan_parts"]) > 1:
                response += "\n\nType 'next' to continue."
            else:
                response += "\n\n✅ END OF ITINERARY."
            user_data["final_itinerary"] = generated
            return response

        except Exception as e:
            return f"❌ Error generating plan: {e}"

    return "✅ Type 'generate plan' or 'reset'."

# === Gradio Interface ===
with gr.Blocks() as demo:
    gr.Markdown("# Travel Assistant")

    with gr.Row():
        gr.Markdown("### Trip Planner")
        model_selector = gr.Dropdown(
            choices=["Local - Mistral-7B model", "Remote - gemini-1.5-pro"],
            value="Local - Mistral-7B model",
            label="Select Model",
            interactive=True,
            scale=2
        )

    chatbot = gr.Chatbot(label="Trip Planner", value=[
        ("", "Hi! I'm here to help you plan your next adventure."),
        ("", "What's your name?")
    ])

    # Input Section: Textbox + Send Button
    with gr.Row():
        msg = gr.Textbox(placeholder="Type your reply here…", show_label=False, scale=8)
        send_button = gr.Button("Send", scale=1)

    # === Respond Function ===
    def respond(user_input, chat_history, model_choice):
        # Save the selected model type into user_data
        user_data["model_choice"] = "Local" if "Local" in model_choice else "Remote"

        # Call your assistant logic
        response = assistant_system(user_input, chat_history)

        # Update chat history
        if user_input.lower().strip() == "generate plan":
            chat_history.append((user_input, "Your plan is ready."))
            chat_history.append(("", response))
        elif user_input.lower().strip() == "next":
            chat_history.append(("", response))
        else:
            chat_history.append((user_input, response))

        return chat_history, chat_history, "", model_choice  # Clear textbox after sending

    # === Connect Both Textbox Submit (Enter) and Send Button ===
    inputs = [msg, chatbot, model_selector]
    outputs = [chatbot, chatbot, msg, model_selector]

    msg.submit(fn=respond, inputs=inputs, outputs=outputs)
    send_button.click(fn=respond, inputs=inputs, outputs=outputs)

# === Launch the App ===
if __name__ == "__main__":
    demo.launch()

