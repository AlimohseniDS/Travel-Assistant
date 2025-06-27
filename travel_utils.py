
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import pytz
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
import os
import googlemaps
# === Load environment variables
load_dotenv()
TP_API_TOKEN = os.getenv("TRAVELPAYOUTS_API_KEY")
AMADEUS_CLIENT_ID = os.getenv("AMADEUS_CLIENT_ID")
AMADEUS_CLIENT_SECRET = os.getenv("AMADEUS_CLIENT_SECRET")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
amadeus_token = None

def estimate_flight_time(origin_city, destination_city, depart_date_str, flight_duration_hours=17):
    """
    Estimate flight departure and arrival time between any two cities, keeping output format the same.
    """
    geolocator = Nominatim(user_agent="flight_time_estimator_dynamic")
    tf = TimezoneFinder()

    # Geocode cities to coordinates
    origin_location = geolocator.geocode(origin_city)
    dest_location = geolocator.geocode(destination_city)

    if not origin_location or not dest_location:
        return "Error: Invalid city name(s)."

    # Timezones from lat/lon
    origin_tz_name = tf.timezone_at(lat=origin_location.latitude, lng=origin_location.longitude)
    dest_tz_name = tf.timezone_at(lat=dest_location.latitude, lng=dest_location.longitude)

    if not origin_tz_name or not dest_tz_name:
        return "Error: Timezone lookup failed."

    origin_tz = pytz.timezone(origin_tz_name)
    dest_tz = pytz.timezone(dest_tz_name)

    # Parse date and set departure time at 9:30 AM
    try:
        depart_date = datetime.strptime(depart_date_str, "%d %B %Y")
    except ValueError:
        return "Error: Incorrect date format. Use '26 April 2025'."

    dep_time = origin_tz.localize(depart_date.replace(hour=9, minute=30))
    arr_time = dep_time + timedelta(hours=flight_duration_hours)
    arr_time = arr_time.astimezone(dest_tz)

    # Keep your original formatting
    return dep_time.strftime("%d %b %Y %H:%M"), arr_time.strftime("%d %b %Y %H:%M")

def get_cheapest_flight(destination, origin="SYD", currency="AUD"):
    url = "https://api.travelpayouts.com/v1/prices/cheap"
    headers = {"X-Access-Token": TP_API_TOKEN}
    params = {"origin": origin.upper(), "destination": destination.upper(), "currency": currency.lower()}
    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
        return float(list(data["data"][destination.upper()].values())[0]["price"])
    except:
        return 1000  # Default fallback price

def get_amadeus_token():
    global amadeus_token
    if amadeus_token:
        return amadeus_token
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_CLIENT_ID,
        "client_secret": AMADEUS_CLIENT_SECRET
    }
    res = requests.post(url, data=payload)
    amadeus_token = res.json().get("access_token")
    return amadeus_token

def get_hotel_price(destination):
    city_codes = {
        "tehran": "THR", "tokyo": "TYO", "paris": "PAR",
        "sydney": "SYD", "melbourne": "MEL", "yazd": "AZD"
    }
    code = city_codes.get(destination.lower(), "TYO")
    token = get_amadeus_token()
    url = f"https://test.api.amadeus.com/v2/shopping/hotel-offers?cityCode={code}&adults=1"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(url, headers=headers)
        offers = res.json()["data"]
        prices = [float(o["offers"][0]["price"]["total"]) for o in offers if "offers" in o]
        return min(prices) if prices else 400
    except Exception as e:
        print(f"Error fetching hotel prices: {e}")
        return 400  # Default fallback price


def get_top_restaurants(destination):
    try:
        results = gmaps.places(query=f"restaurants in {destination}", type="restaurant")["results"]
        top = []
        seen_names = set()

        for r in results:
            name = r.get("name", "")
            address = r.get("formatted_address", "")
            rating = r.get("rating", "N/A")
            price = 15 * r.get("price_level", 2)

            if destination.lower() in address.lower() and name not in seen_names:
                top.append({
                    "name": name,
                    "rating": rating,
                    "price": price,
                    "address": address
                })
                seen_names.add(name)

            if len(top) >= 3:
                break

        return top
    except Exception as e:
        print(f"Error fetching restaurants: {e}")
        return []
