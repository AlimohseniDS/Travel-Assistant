# ✈️ AI-Powered Travel Assistant

This project is an interactive chatbot that generates personalised, structured travel itineraries based on user preferences, real-time pricing data, and prompt-engineered instructions. It uses both a local Large Language Model (Mistral-7B) and a remote cloud model (Gemini 1.5 Pro) to offer flexible and robust itinerary planning.

## 🔧 Features

- 🧠 Dual LLM Support: Run locally with Mistral-7B or remotely via Gemini 1.5 Pro
- 🗣️ Gradio-based chatbot interface for smooth user interaction
- 📊 Real-time integration with flight, hotel, and restaurant APIs
- 📅 Structured itinerary generation with time slots, meals, tips, and budget calculation
- 🧾 Multiple prompt templates for output quality experimentation
- ⚠️ Budget warnings and fallback logic for API failures
- 🔐 Environment variable-based key protection

## 🗂️ Project Structure

| File | Description |
|------|-------------|
| `travel_assistant.py` | Main script with Gradio UI and user dialogue flow |
| `build_prompts.py` | Prompt engineering templates (5 versions) |
| `llm_utils.py` | LLM loading and generation logic (Mistral and Gemini) |
| `travel_utils.py` | Utility functions for time zones, APIs, and recommendations |
| `requirements.txt` | Project dependencies |
| `prompts_and_outputs.ipynb` | Notebook for prompt testing and output inspection |
| `Report.pdf` | Project documentation and evaluation |
| `.env.example` | Template for API credentials |

## 💻 Installation

```bash
git clone https://github.com/YOUR_USERNAME/travel-assistant.git
cd travel-assistant
pip install -r requirements.txt

## 🔐 API Configuration

Create a `.env` file in the root directory using the provided `.env.example` file:

```env
TRAVELPAYOUTS_API_KEY=your_travel_api_key
AMADEUS_CLIENT_ID=your_amadeus_client_id
AMADEUS_CLIENT_SECRET=your_amadeus_client_secret
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
GEMINI_API_KEY=your_gemini_api_key

## 🚀 Run the Application

Run the app using the following command:

```bash
python travel_assistant.py

## 📊 Models Supported

The Travel Assistant supports two LLM options:

- **Local – Mistral-7B**  
  Runs on your machine. Offers fast, offline, and privacy-preserving itinerary generation.

- **Remote – Gemini 1.5 Pro**  
  Uses Google’s powerful cloud-based LLM for highly fluent and multilingual responses.

You can select the preferred model using the dropdown menu in the chatbot interface.

## 📎 Example Commands

You can interact with the chatbot using simple text commands:

- `reset` – Clear the current profile and restart the planning process
- `next` – View the next section of the generated itinerary
- `generate plan` – Generate your full travel itinerary after providing all required information

## 📘 Project Report

For technical explanations, prompt engineering experiments, and evaluation details, please refer to the [`Report.pdf`](./Report.pdf) included in this repository.

It covers:

- System architecture
- Prompt template comparisons
- Local vs. remote model performance
- Privacy and hallucination mitigation
- Future improvements

## 🛡️ Privacy

This project is designed with privacy and user safety in mind:

- **Minimal data collection**: Only essential information (e.g., name, travel dates, budget) is collected for itinerary generation.
- **No sensitive details**: The system does not request or store passport numbers, payment details, or personal identifiers.
- **Secure API access**: All API keys are managed via environment variables and are not hard-coded.
- **Hallucination mitigation**: If the model generates unrealistic suggestions, the system flags them and offers budget optimisation tips.


