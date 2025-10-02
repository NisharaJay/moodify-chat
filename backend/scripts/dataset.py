from faker import Faker
import pandas as pd
import random

fake = Faker()

moods = ["happy", "sad", "energetic", "nostalgic", "angry", "relaxed", "romantic", "motivated", "calm", "excited"]

songs = []
for _ in range(1000):
    song_name = fake.sentence(nb_words=3).replace(".", "")
    artist = fake.name()
    lyrics = fake.text(max_nb_chars=80)
    mood = random.choice(moods)
    songs.append([song_name, artist, lyrics, mood])

df = pd.DataFrame(songs, columns=["song_name", "artist", "lyrics", "mood"])
df.to_csv("songs.csv", index=False)
