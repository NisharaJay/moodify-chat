### Moodify Chatbot
Moodify is an AI-powered music mood companion that recommends songs based on your current feelings. Just tell Moodify how you're feeling, and it will suggest tracks that match your vibe with Spotify previews.

#### Features
- Conversational chat interface for mood-based music suggestions.
- Quick mood buttons for instant recommendations (Happy, Sad, Energetic, Calm).
- Displays song details including album cover, artist, and title.
- Song previews directly in the chat.
- Fully responsive and visually appealing UI.

#### Technologies
- Python & FastAPI – Backend API for processing mood inputs and generating suggestions.
- PyTorch & HuggingFace Transformers – For embedding-based song retrieval and NLP.
- LangChain & Chroma – Vector database and embeddings for efficient recommendation.
- Next.js – Frontend framework for building the interactive chat interface.
- Tailwind CSS – Styling and responsive design.

#### Clone the repo
```bash
git clone https://github.com/NisharaJay/moodify-chat.git
cd moodify-chat
```
Install dependencies
```bash
npm install
```
Run the development server
```bash
npm run dev
```

##### Backend setup
Make sure your backend API is running at [http://localhost:8000/suggest]
```bash
pip install -r requirements.txt
uvicorn backend.app:app --reload --port 8000
