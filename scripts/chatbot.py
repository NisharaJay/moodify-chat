import pandas as pd
from sklearn.model_selection import train_test_split
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from difflib import SequenceMatcher
import warnings
import random
from scripts.spotify_auth import get_spotify_preview

warnings.filterwarnings("ignore", category=UserWarning, module="langchain")

#Load Dataset
print("Loading songs dataset...")
try:
    df = pd.read_csv("./dataset/songs.csv")  # Ensure dataset path is correct
except FileNotFoundError:
    print("Error: 'dataset/songs.csv' not found.")
    exit()

# Split dataset
train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

# Embeddings
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#Helper Functions
def df_to_docs(dataframe):
    docs = []
    for _, row in dataframe.iterrows():
        text = f"{row['song_name']} by {row['artist']}. Mood: {row['mood']}. Lyrics: {row['lyrics'][:100]}"
        docs.append(Document(page_content=text, metadata={
            "song_name": row['song_name'],
            "artist": row['artist'],
            "mood": row['mood'],
            "lyrics": row['lyrics']
        }))
    return docs

train_docs = df_to_docs(train_df)
vectordb = Chroma.from_documents(train_docs, embedding=embed_model)

def extract_mood(user_input):
    return user_input.lower().replace("i feel ", "").strip()

def is_match(a, b, threshold=0.5):
    suggestion_parts = b.split(" by ")
    suggested_song_name = suggestion_parts[0] if suggestion_parts else ""
    return SequenceMatcher(None, a.lower(), suggested_song_name.lower()).ratio() > threshold

#Song Suggestion Function

def suggest_song(user_input):
    mood = extract_mood(user_input)
    
    search_results = vectordb.similarity_search(query=mood, k=100)
    
    # Filter and shuffle
    mood_docs_metadata = []
    for doc in search_results:
        if doc.metadata['mood'].lower() == mood:
            mood_docs_metadata.append(doc.metadata)
    
    if not mood_docs_metadata:
        return {"text": f"No relevant song found for the mood: '{mood}'.", "songs": []}

    # Shuffle the list to get different songs each time
    random.shuffle(mood_docs_metadata)
    doc = mood_docs_metadata[0]
    
    spotify_data = get_spotify_preview(doc['song_name'], doc['artist'])

    return {
        "text": f"🎶 Here's a suggestion: {doc['song_name']} by {doc['artist']} (Mood: {doc['mood']})",
        "songs": [{
            "title": doc['song_name'],
            "artist": doc['artist'],
            "emoji": "🎵",
            "spotify_url": spotify_data.get("spotify_url"),
            "preview_url": spotify_data.get("preview_url"),
            "album_cover": spotify_data.get("album_cover")
        }]
    }