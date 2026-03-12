from fastapi import FastAPI
import requests
import os
from groq import Groq

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

SHEET_URL = SHEET_URL = "https://docs.google.com/spreadsheets/d/1Vd6DaCvOlnZ_omVG_xGSj6kUT5OUpt3JGE7jDBXEAsQ/export?format=csv"
def get_games():
    response = requests.get(SHEET_URL)
    return response.text

@app.get("/recommend")
def recommend_game(sport: str):

    prompt = f"Recommend a pickup location in San Francisco for {sport}"

    chat = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"recommendation": chat.choices[0].message.content}
