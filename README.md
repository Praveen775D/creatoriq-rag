# CreatorIQ RAG Analyzer

An AI-powered **Video Intelligence System** that compares **YouTube Shorts and Instagram Reels** using **RAG (Retrieval-Augmented Generation)** and provides deep insights like:

- Engagement comparison
- Content strategy analysis
- Creator performance breakdown
- AI-generated recommendations

---

##  Demo Overview

CreatorIQ analyzes two videos:

-  YouTube Shorts
-  Instagram Reels

And generates:

-  Metrics (views, likes, comments, engagement rate)
-  AI analysis using LLM (Groq / OpenAI)
-  Vector search (ChromaDB + embeddings)
-  Chat-based Q&A insights

---

##  System Architecture
Frontend (Next.js)
↓
Backend (FastAPI)
↓
Ingestion Layer
↓
YouTube Service / Instagram Service
↓
Metadata + Transcript Extraction
↓
Chunking Service
↓
Embeddings (HuggingFace BGE)
↓
Chroma Vector DB
↓
RAG Pipeline (LangChain / LangGraph)
↓
LLM (Groq / OpenAI)
↓
Final AI Analysis


---

##  Tech Stack

### Backend
- FastAPI
- LangChain / LangGraph
- ChromaDB (Vector Database)
- HuggingFace Embeddings (BAAI/bge-small-en-v1.5)
- yt-dlp (video metadata)
- YouTube Transcript API
- Groq / OpenAI LLM

### Frontend
- Next.js 14+
- TailwindCSS
- React Components
- TypeScript

---

##  Features

###  Video Ingestion
- Accepts YouTube & Instagram URLs
- Extracts metadata automatically
- Handles Shorts & Reels
- Fallback parsing for missing fields

###  AI Analysis
- Hook quality analysis
- Engagement signal detection
- Content structure evaluation
- Creator strategy insights

###  Metrics Engine
- Views
- Likes
- Comments
- Engagement Rate calculation

###  RAG System
- Stores video chunks in vector DB
- Retrieves similar context
- Generates grounded AI responses

###  AI Chat
Ask questions like:

- Why did Video A perform better?
- Which video is trending and why?
- How can creators improve engagement?

---

##  UI Features

- Modern SaaS-style dashboard
- Side-by-side video comparison
- Metric cards (views, likes, comments)
- Hashtag visualization
- AI insight panel
- Responsive layout

---

##  Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/your-username/creatoriq-rag.git
cd creatoriq-rag

2. Backend Setup
cd backend

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt

Create .env file:

OPENAI_API_KEY=your_key
GROQ_API_KEY=your_key
CHROMA_PERSIST_DIRECTORY=./chroma_db

Run backend:

uvicorn app.main:app --reload
3. Frontend Setup
cd frontend
npm install
npm run dev

Open: http://localhost:3000

Example Output

YouTube Video
Views: 10M+
Likes: 120K
Engagement: 1.2%
Instagram Reel
Views: (may vary based on API access)
Likes: 30K+
Engagement: computed dynamically
⚠️ Known Limitations

Instagram views may show 0 due to API restrictions
Some reels do not expose public analytics
Engagement is estimated using available metadata
Why Instagram Views = 0?

Instagram restricts:

play_count
view_count
reel insights

So system uses fallback:

like_count + comment_count

This is expected behavior in yt-dlp extraction.

Future Improvements
Add real Instagram Graph API integration
Add sentiment analysis on comments
Add retention prediction model
Add user authentication
Deploy on AWS / Vercel

 Project Highlights

✔ Full-stack AI system
✔ RAG-based architecture
✔ Real-world social media analytics
✔ Production-style UI
✔ Interview-ready project

Author
Udugundla Praveen

Built as a CreatorIQ AI Challenge Project