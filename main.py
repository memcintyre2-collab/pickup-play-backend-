from fastapi import FastAPI
import requests
import os
import csv
import io
from fastapi.responses import JSONResponse
from groq import GroqClient

app = FastAPI()

# Environment variables
SHEET_ID = os.getenv("SHEET_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq client
client = GroqClient(api_key=GROQ_API_KEY)

# Sheet URL
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Endpoint to fetch games
@app.get("/games")
def fetch_games():
    response = requests.get(SHEET_URL)
    f = io.StringIO(response.text)
    reader = csv.DictReader(f)
    games = list(reader)
    return JSONResponse(content={"games": games})

# Endpoint to recommend a game
@app.get("/recommend")
def recommend_game(sport: str):
    prompt = f"Recommend a pickup location in San Francisco for {sport}"
    chat = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"recommendation": chat.choices[0].message.content}
