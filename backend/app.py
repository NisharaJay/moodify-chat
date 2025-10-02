from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .scripts.chatbot import suggest_song

#FastAPI Setup
app = FastAPI()

# Allow requests from frontend (localhost:3000)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Pydantic Models
class UserInput(BaseModel):
    text: str

class SongSuggestion(BaseModel):
    text: str
    songs: List[dict]

#Endpoint
@app.post("/suggest", response_model=SongSuggestion)
def get_suggestion(user_input: UserInput):
    return suggest_song(user_input.text)
