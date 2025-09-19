from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize OpenAI client function
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Please set it in your environment variables.")
    return OpenAI(api_key=api_key)

def build_prompt(time_of_day, meal_type, symptoms, food=None, user_question=None):
    return f"""
You are a health explainer bot called “Why the Slump?” that helps people understand 
why they feel tired, sleepy, bloated, restless, or hungry at different times of the day.  

The user will provide:
- Time of day (morning, midday, night)
- Meal type (light, heavy, or full)
- Symptoms (list of feelings such as tired, sleepy, bloated, hungry, restless, jittery, etc.)
- Specific food they ate (optional, e.g., pongal, salad, biryani)
- A user question (optional, e.g., “Why do I feel like napping after lunch?”)

Your job:
1. Interpret the meal type and, if given, the specific food. Mention common qualities of that food (e.g., carb-heavy, oily, spicy, fried, protein-rich, light, etc.).
2. Consider the time of day — explain why slumps may happen in the morning, afternoon, or night.
3. Connect the food/meal + timing + symptoms into a simple lifestyle-based explanation.
4. Keep the explanation clear and conversational, 2–4 sentences long.
5. Do not give medical advice or diagnoses. Only provide general explanations.

User input:
- Time of day: {time_of_day}
- Meal type: {meal_type}
- Symptoms: {", ".join(symptoms)}
- Specific food: {food if food else "Not provided"}
- User question: {user_question if user_question else "Not provided"}

Now generate an explanation:
"""

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Why the Slump? API is running!",
        "endpoints": {
            "POST /api/slump": "Explain why you feel tired/sluggish after eating"
        },
        "example_request": {
            "time_of_day": "midday",
            "meal_type": "heavy",
            "symptoms": ["tired", "sleepy"],
            "food": "biryani",
            "user_question": "Why do I feel sleepy after lunch?"
        }
    })

@app.route("/api/slump", methods=["POST"])
def explain_slump():
    data = request.json

    # Required fields
    time_of_day = data.get("time_of_day")
    meal_type = data.get("meal_type")
    food = data.get("food")
    user_question = data.get("user_question")

    # Handle symptom(s) as string or list
    symptoms = []
    if "symptom" in data and isinstance(data["symptom"], str):
        symptoms.append(data["symptom"])
    if "symptoms" in data and isinstance(data["symptoms"], list):
        symptoms.extend(data["symptoms"])

    if not time_of_day or not meal_type or not symptoms:
        return jsonify({
            "error": "time_of_day, meal_type, and at least one symptom are required"
        }), 400

    # Build prompt
    prompt = build_prompt(time_of_day, meal_type, symptoms, food, user_question)

    try:
        client = get_openai_client()
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        explanation = completion.choices[0].message.content.strip()
    except Exception as e:
        return jsonify({
            "error": "Failed to generate explanation",
            "details": str(e)
        }), 500

    return jsonify({
        "time_of_day": time_of_day,
        "meal_type": meal_type,
        "symptoms": symptoms,
        "food": food,
        "user_question": user_question,
        "explanation": explanation
    })

if __name__ == "__main__":
    app.run(debug=True)
