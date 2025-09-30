import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_spotify_token():
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_string = base64.b64encode(auth_string.encode()).decode()
    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {b64_auth_string}"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def get_spotify_preview(song_name, artist):
    token = get_spotify_token()
    query = f"{song_name} {artist}"
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {}
    items = response.json().get("tracks", {}).get("items", [])
    if items:
        track = items[0]
        return {
            "spotify_url": track["external_urls"]["spotify"],
            "preview_url": track["preview_url"],
            "album_cover": track["album"]["images"][0]["url"] if track["album"]["images"] else None
        }
    return {}
