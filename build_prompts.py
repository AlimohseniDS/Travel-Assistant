
# first style

# def build_prompt(data, flight, hotel, remain, dep_str, arr_str, nights, restaurants, warning=""):
#     prompt = f"""{warning}You are a helpful and professional travel planner.

# User details:
# Name: {data['name']}
# Travel route: {data['origin']} → {data['destination']}
# Departure date: {data['travel_date']}
# Return date: {data['return_date']} ({nights} nights)
# Budget: {data['budget']}
# Special needs: {data['special_needs']}

# Flight cost: {flight:.2f} AUD
# Departure: {dep_str}
# Arrival: {arr_str}

# Hotel cost for {nights} nights: {hotel:.2f} AUD

# Suggested restaurants:
# """
#     for r in restaurants:
#         prompt += f"- {r['name']} (Rating: {r['rating']}, Approx. {r['price']} AUD)\n  Address: {r['address']}\n"

#     prompt += f"\nRemaining budget: ~{remain:.2f} AUD\n\n"

#     prompt += (
#         "Now generate a realistic, structured itinerary broken into daily sections.\n\n"
#         "Use this format for each day:\n\n"
#         "Day X: [Short title for the day]\n\n"
#         "Time slots:\n"
#         "  - [HH:MM] - [Activity] (mention if free or approx. cost)\n\n"
#         "Meals:\n"
#         "  - Lunch: [Restaurant Name] (approx. cost)\n"
#         "  - Dinner: [Restaurant Name] (approx. cost)\n\n"
#         "Tips:\n"
#         "  - [Helpful daily travel tip, concise]\n\n"
#         "Only include activities that fit in one day realistically.\n"
#         "Do not repeat emojis, markdown symbols, or headers.\n"
#         "Keep the tone clean and practical.\n\n"
#         "At the end of the final day, write: END OF ITINERARY."
#     )
#     return prompt




# second style

# def build_prompt(data, flight, hotel, remain, dep_str, arr_str, nights, restaurants, warning=""):
#     prompt = f"""{warning}You are an experienced travel planner. Your task is to create a clear, realistic, and structured itinerary for the user based on the details provided below.

# ## User Details:
# - Name: {data['name']}
# - Travel Route: {data['origin']} → {data['destination']}
# - Departure Date: {data['travel_date']}
# - Return Date: {data['return_date']} ({nights} nights)
# - Total Budget: {data['budget']}
# - Special Needs / Preferences: {data['special_needs']}

# ## Flight Information:
# - Flight Cost: {flight:.2f} AUD
# - Departure Time: {dep_str}
# - Arrival Time: {arr_str}

# ## Hotel Information:
# - Hotel Cost for {nights} nights: {hotel:.2f} AUD

# ## Recommended Restaurants:
# """
#     for r in restaurants:
#         prompt += f"- {r['name']} | Rating: {r['rating']} | Approx. {r['price']} AUD\n  Address: {r['address']}\n"

#     prompt += f"""
# ## Remaining Budget (after flight and hotel): ~{remain:.2f} AUD

# ---

# ## Itinerary Generation Instructions:
# 1. Plan the itinerary **day-by-day**.
# 2. Each day should be **balanced** with sightseeing, activities, rest periods, and meals.
# 3. Activities should include **time slots**, **location names**, and **estimated costs**.
# 4. Provide suggestions for **lunch** and **dinner**, using the recommended restaurants where appropriate.
# 5. Offer **one helpful tip per day** (e.g., cultural advice, weather warnings, travel tips).
# 6. Ensure no activity overlaps or unrealistic scheduling.
# 7. Respect the budget constraint as much as possible. If exceeded, mention where the plan can be optimized.

# ---

# ## Output Format:
# Day X: [Short title describing the day]

# Time Slots:
#   - [HH:MM] – [Activity / Location] (Estimated Cost or Free)

# Meals:
#   - Lunch: [Restaurant Name] (Approx. Cost)
#   - Dinner: [Restaurant Name] (Approx. Cost)

# Daily Tip:
#   - [One concise helpful tip]

# ---

# ✅ End the itinerary with the statement:
# "END OF ITINERARY."
# Do not include emojis, bullet symbols, or markdown styling.

# Provide the itinerary directly below.
# """
#     return prompt


# third style

# def build_prompt(data, flight, hotel, remain, dep_str, arr_str, nights, restaurants, warning=""):
#     prompt = f"""{warning}

# Itinerary Details:
# - Name: {data['name']}
# - Route: {data['origin']} → {data['destination']}
# - Departure: {data['travel_date']} at {dep_str}
# - Return: {data['return_date']} at {arr_str} ({nights} nights)
# - Budget: {data['budget']} (Remaining after flight and hotel: ~{remain:.2f} AUD)
# - Special Needs / Preferences: {data['special_needs']}

# Flight Cost: {flight:.2f} AUD
# Hotel Cost for {nights} nights: {hotel:.2f} AUD

# Recommended Restaurants:
# """
#     for r in restaurants:
#         prompt += f"- {r['name']} | Rating: {r['rating']} | Approx. {r['price']} AUD\n  Address: {r['address']}\n"

#     prompt += f"""

# ======================
# Please generate a structured day-by-day itinerary. Use the following rules:

# 1. Write each day as: **Day X: [Short title describing the day]**
# 2. Under each day, use the following format:
#    Time Slots:
#      - [HH:MM] – [Activity / Location] (Estimated Cost or Free)
#    Meals:
#      - Lunch: [Restaurant Name] (Approx. Cost)
#      - Dinner: [Restaurant Name] (Approx. Cost)
#    Daily Tip:
#      - [Helpful advice for the day]

# 3. Do NOT start with any extra introductory sentences.
# 4. Do NOT use emojis, markdown, or bullet symbols (just clean text).
# 5. If the plan exceeds the budget, mention which parts could be optimised.
# 6. Ensure daily balance: sightseeing, activities, meals, and rest periods.
# 7. Respect realistic travel time between locations.
# 8. End the itinerary with this sentence exactly:
# END OF ITINERARY.
# """
#     return prompt


# fourth style

# def build_prompt(data, flight, hotel, remain, dep_str, arr_str, nights, restaurants, warning=""):
#     prompt = f"""{warning}

# Create the travel itinerary as a valid JSON object.

# The JSON should have:
# - A top-level "itinerary" list, each item is a day.
# - Each "day" object must contain:
#   - "day_number": integer (e.g., 1, 2, 3, ...)
#   - "title": short description of the day
#   - "time_slots": list of {{"time": "HH:MM", "activity": "activity description", "cost": "estimated cost or 'Free'"}}
#   - "meals": object with keys "breakfast", "lunch", "dinner", each value being a restaurant name and approximate cost (if any)
#   - "daily_tip": string (helpful advice for the day)

# Additional fields (only once at the start of the JSON):
# - "user_details": {{
#     "name": "{data['name']}",
#     "route": "{data['origin']} → {data['destination']}",
#     "departure": "{data['travel_date']} at {dep_str}",
#     "return": "{data['return_date']} at {arr_str}",
#     "nights": {nights},
#     "budget": "{data['budget']}",
#     "remaining_budget": "{remain:.2f} AUD",
#     "special_needs": "{data['special_needs']}"
#   }}
# - "flight": {{
#     "cost": "{flight:.2f} AUD",
#     "departure_time": "{dep_str}",
#     "arrival_time": "{arr_str}"
#   }}
# - "hotel": {{
#     "cost": "{hotel:.2f} AUD",
#     "nights": {nights}
#   }}
# - "recommended_restaurants": [
# """
#     for r in restaurants:
#         prompt += f"""    {{
#         "name": "{r['name']}",
#         "rating": "{r['rating']}",
#         "approx_price": "{r['price']} AUD",
#         "address": "{r['address']}"
#     }},"""
#     prompt = prompt.rstrip(",")  # Remove the last comma
#     prompt += """
# ]

# Rules for generation:
# 1. Do not include any introductory text before or after the JSON.
# 2. Ensure the JSON is complete and properly formatted.
# 3. Respect realistic scheduling between activities and meals.
# 4. Mention "remaining budget" at the end of each day if possible.
# 5. If the plan exceeds the budget, include a "budget_warning" field explaining which parts may be optimized.
# 6. End with a closing curly brace for the JSON object.

# Output only the JSON object.
# """
#     return prompt



# fifth style

def build_prompt(data, flight, hotel, remain, dep_str, arr_str, nights, restaurants, warning=""):
    # Construct the recommended restaurants list:
    restaurant_info = "\n".join(
        [f"- {r['name']} | Rating: {r['rating']} | Approx. {r['price']} AUD\n  Address: {r['address']}" for r in restaurants]
    )

    # Build the full prompt:
    prompt = f"""{warning}Please generate a structured, day-by-day travel itinerary based on the following user details:

User Details:
- Name: {data['name']}
- Route: {data['origin']} → {data['destination']}
- Departure: {data['travel_date']} at {dep_str}
- Return: {data['return_date']} at {arr_str} ({nights} nights)
- Budget: {data['budget']} AUD (Remaining after flight and hotel: ~{remain:.2f} AUD)
- Special Needs / Preferences: {data['special_needs']}

Flight Cost: {flight:.2f} AUD
Hotel Cost for {nights} nights: {hotel:.2f} AUD

Recommended Restaurants:
{restaurant_info}

============================

Itinerary Generation Rules:
1. Write each day as: Day X: [Short title describing the day].
2. Strictly follow this output structure under each day:

Day X: [Short title]

Time Slots:
[HH:MM] – [Activity / Location] (Estimated Cost or Free)
[HH:MM] – [Activity / Location] (Estimated Cost or Free)
[HH:MM] – [Activity / Location] (Estimated Cost or Free)

Meals:
Lunch: [Restaurant Name] (Approx. Cost)
Dinner: [Restaurant Name] (Approx. Cost)

Daily Tip:
[One concise helpful tip]

3. Each activity must appear on a **new line**.
4. Leave **one blank line between each day**.
5. Do **NOT** include markdown, emojis, bullet points, or extra explanatory text.
6. Avoid repeating the same restaurant too often unless necessary.
7. If the plan exceeds the budget, mention where the budget can be optimised.
8. Ensure daily balance: sightseeing, rest periods, meals, and realistic travel times between locations.
9. End the itinerary with this exact sentence:
END OF ITINERARY.

============================

Please directly output the itinerary below following these rules.
"""
    return prompt

