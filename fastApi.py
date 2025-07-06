from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import pickle
import pandas as pd
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Initialize FastAPI app
app = FastAPI()

# Allow frontend access (adjust origin in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model for API
class RecipeRequest(BaseModel):
    user_input: str

# Download required NLTK resources
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

# NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
ingredient_stopwords = stop_words.union({
    "teaspoon", "tablespoon", "ounce", "gram", "pound", "cup", "chopped", "fresh",
    "ground", "large", "sliced", "peeled", "cut", "freshly", "finely", "plus",
    "white", "clove", "room", "dry", "inch", "ingredient", "with", "and", "of"
})

# Load all model files
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

with open("known_ingredients.pkl", "rb") as f:
    known_ingredients = pickle.load(f)

with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("train_vectors.pkl", "rb") as f:
    train_vectors = pickle.load(f)

# Load dataset
df = pd.read_csv("recipes_with_emotions.csv")
print("Loaded recipes_with_emotions.csv")
print(df.head())

# Load emotion classifier
emotion_classifier = pipeline(
    "text-classification",
    model="bert_emotion_model",
    tokenizer="bert_emotion_model",
    return_all_scores=False
)

# -------------------------------
# Helper Functions
# -------------------------------

def extract_ingredients(text: str):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    lemmatized = [lemmatizer.lemmatize(w) for w in words]
    filtered = [w for w in lemmatized if w in known_ingredients and w not in ingredient_stopwords]
    return ", ".join(filtered)

def decode_emotion(label):
    try:
        encoded = int(label.split("_")[1])
        return label_encoder.inverse_transform([encoded])[0]
    except Exception:
        return "neutral"

def extract_calorie_range(text):
    matches = re.findall(r'under\s+(\d+)', text.lower())
    if matches:
        return 0, int(matches[0])
    return None

def get_emotion_message(emotion):
    messages = {
        "happy": "It's wonderful to see you're in a joyful mood! Let’s make something that keeps that happiness going.",
        "sadness": "I'm sorry you're feeling down. Here are some warm, comforting recipes to help you feel a little better.",
        "anger": "It’s okay to feel angry sometimes. These calming recipes might help bring you a moment of peace.",
        "surprise": "Life’s full of surprises! Why not try a dish that's as unexpected and exciting as your day?",
        "fear": "If you're feeling nervous or anxious, you're not alone. These soothing recipes might bring some calm and comfort.",
        "love": "What a beautiful feeling! These heartwarming recipes are perfect to enjoy with someone special—or to treat yourself with love."
    }
    return messages.get(emotion.lower(), "")

def user_explicitly_mentioned_emotion(text):
    emotion_keywords = ["happy", "sad", "angry", "love", "fear", "surprise", "joyful", "depressed", "anxious"]
    return any(word in text.lower() for word in emotion_keywords)

# -------------------------------
# Recommendation Function
# -------------------------------
def find_similar_recipe(user_input):
    # Detect emotion using classifier
    emotion_result = emotion_classifier(user_input)
    detected_label = emotion_result[0]["label"]
    detected_emotion = decode_emotion(detected_label)

    # Show emotion message ONLY if user explicitly expressed it
    if user_explicitly_mentioned_emotion(user_input):
        emotion_message = get_emotion_message(detected_emotion)
    else:
        emotion_message = ""

    # Ingredient + calorie parsing
    input_ingredients = extract_ingredients(user_input)
    cal_range = extract_calorie_range(user_input)

    if not input_ingredients or len(input_ingredients.split()) < 2:
        return {
            "message": emotion_message,
            "recipes": [{
                "title": "No Matching Recipe",
                "ingredients": "N/A",
                "directions": "Please enter more ingredients (at least 2).",
                "calories": 0
            }]
        }

    # Calorie filtering
    if cal_range:
        min_cal, max_cal = cal_range
        filtered_df = df[
            (df["total_calories"] >= min_cal) &
            (df["total_calories"] <= max_cal) &
            (df["total_calories"] > 20)
        ]
    else:
        filtered_df = df[df["total_calories"] > 20]

    if filtered_df.empty:
        return {
            "message": emotion_message,
            "recipes": [{
                "title": "No matching recipes in calorie range.",
                "ingredients": "N/A",
                "directions": "Try expanding your calorie range.",
                "calories": 0
            }]
        }

    # Emotion filter
    if detected_emotion:
        emotion_filtered_df = filtered_df[filtered_df["Emotion"] == detected_emotion]
        candidate_df = emotion_filtered_df if not emotion_filtered_df.empty else filtered_df
    else:
        candidate_df = filtered_df

    # TF-IDF + cosine similarity
    input_vector = vectorizer.transform([input_ingredients])
    candidate_vectors = vectorizer.transform(candidate_df["ingredients"])
    similarity_scores = cosine_similarity(input_vector, candidate_vectors)[0]

    top_indices = similarity_scores.argsort()[-3:][::-1]
    top_recipes = []

    for idx in top_indices:
        recipe = candidate_df.iloc[idx]
        score = similarity_scores[idx]
        top_recipes.append({
            "title": recipe["title"],
            "ingredients": recipe["cleaned_ingredients"],
            "directions": recipe["directions"],
            "calories": recipe["total_calories"],
            "similarity_score": round(float(score), 4)
        })

    return {
        "message": emotion_message,
        "recipes": top_recipes
    }

# -------------------------------
# API Endpoint
# -------------------------------
@app.post("/recommend-recipe")
async def recommend_recipe(request: RecipeRequest):
    try:
        result = find_similar_recipe(request.user_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
