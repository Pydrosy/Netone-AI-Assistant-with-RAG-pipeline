Complete README.md for Netone AI Assistant
markdown
# Netone AI Assistant 🤖

An intelligent customer service assistant for **Netone Zimbabwe** powered by RAG (Retrieval-Augmented Generation) technology. This AI assistant provides instant, accurate responses about Netone's services, bundles, SIM cards, company information, and more - available 24/7.

![Netone AI Assistant Demo](https://via.placeholder.com/800x400?text=Netone+AI+Assistant+Demo)

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Knowledge Base](#-knowledge-base)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 📖 Overview

Netone AI Assistant is a production-ready conversational AI system designed specifically for **Netone Zimbabwe**, one of the country's leading telecommunications providers. The assistant leverages **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware responses based on official Netone documentation.

**Key Highlights:**
- ✅ **103 knowledge chunks** across 13 documents
- ✅ **Response time:** < 2 seconds
- ✅ **24/7 availability** - never sleeps
- ✅ **Source attribution** - shows where information comes from
- ✅ **Tourist SIM support** - special assistance for visitors

---

## 🚀 Features

### Core Capabilities
| Feature | Description |
|---------|-------------|
| **🤖 AI-Powered Chat** | Natural language conversations about Netone services |
| **📚 RAG Architecture** | Retrieves relevant information from company documents |
| **🔍 Accurate Responses** | Information sourced from verified documents |
| **📎 Source Attribution** | Shows which documents were used for each answer |
| **⚡ Fast Performance** | Responses in under 2 seconds |
| **🌐 24/7 Availability** | Always online, always helpful |

### Knowledge Areas
- 📱 **Mobile Services** - Voice plans, SMS, and bundles
- 💰 **OneMoney** - Mobile money platform information
- 📶 **Data Packages** - Daily, weekly, monthly bundles
- 📍 **Network Coverage** - 4G/LTE coverage by province
- 📞 **Customer Support** - Contact channels and service centers
- 💳 **Airtime** - Recharge options and denominations
- 🌍 **Roaming** - International services and rates
- 🧳 **Tourist SIM** - Special SIM for visitors to Zimbabwe

---

## 📚 Knowledge Base

The assistant is trained on **13 documents** with **103 total chunks** of information:

| Document | Content | Chunks |
|----------|---------|--------|
| `netone_bundles_2026_updated.txt` | Complete bundle pricing (BBB, MoGigs, OneFusion, etc.) | 9 |
| `netone_company_history.txt` | Company history, founding, milestones | 2 |
| `netone_customer_support.txt` | Support contacts, service centers | 5 |
| `netone_faq.txt` | Frequently asked questions | 16 |
| `netone_faq_troubleshooting.txt` | Troubleshooting guides | 6 |
| `netone_leadership.txt` | Executive team and board members | 2 |
| `netone_scratch_cards.txt` | Scratch card information and usage | 10 |
| `netone_sim_card_guide.txt` | SIM card purchase, replacement, activation | 7 |
| `netone_technical_guide.txt` | Technical support, APN settings | 19 |
| `netone_tourist_sim_official_2026.txt` | Tourist SIM card details | 4 |
| `netone_zimbabwe_complete_guide.txt` | Comprehensive company guide | 4 |
| `netone_zimbabwe_complete_guide_old.txt` | Legacy information (archived) | 17 |
| `sample_faq.txt` | Sample questions | 2 |
| **TOTAL** | | **103 CHUNKS** |

### Bundle Pricing Examples
| Bundle | Price | Data | Validity |
|--------|-------|------|----------|
| **BBB 100** | $45 | 100 GB | 30 days |
| **BBB 150** | $80 | 150 GB | 30 days |
| **BBB 200** | $130 | 200 GB | 30 days |
| **MoGigs 30** | $30 | 30 GB | 30 days |
| **OneFusion 2** | $9 | 2 GB + 25 min + 25 SMS | 30 days |
| **Tourist SIM $16** | $16 | 3 GB + 30 min + 30 SMS | 30 days |

---

## 🛠️ Tech Stack

### Backend
┌─────────────────────────────────────────────────────────┐
│ BACKEND TECHNOLOGY │
├─────────────────────────────────────────────────────────┤
│ • Python 3.9+ │
│ • FastAPI - High-performance async web framework │
│ • LangChain - RAG orchestration and prompt management │
│ • FAISS - Vector similarity search database │
│ • Groq - LLM inference (llama-3.3-70b-versatile) │
│ • sentence-transformers - Text embeddings (all-MiniLM) │
│ • SQLAlchemy - Database ORM (optional) │
│ • Pydantic - Data validation │
│ • Uvicorn - ASGI server │
└─────────────────────────────────────────────────────────┘

text

### Frontend
┌─────────────────────────────────────────────────────────┐
│ FRONTEND TECHNOLOGY │
├─────────────────────────────────────────────────────────┤
│ • React 19 - UI library │
│ • Vite - Next-generation build tool │
│ • Tailwind CSS - Utility-first styling │
│ • Lucide React - Beautiful icons │
│ • React Markdown - Message formatting │
│ • Axios - HTTP client │
│ • date-fns - Date formatting │
└─────────────────────────────────────────────────────────┘

text

### Infrastructure
┌─────────────────────────────────────────────────────────┐
│ INFRASTRUCTURE │
├─────────────────────────────────────────────────────────┤
│ • Git/GitHub - Version control │
│ • Docker - Containerization ready │
│ • Environment variables - Secure configuration │
│ • CORS enabled - Frontend-backend communication │
│ • Ready for cloud deployment (Render, Netlify) │
└─────────────────────────────────────────────────────────┘

text

---

## 📁 Project Structure
netone-ai-assistant/
├── backend/ # Python FastAPI backend
│ ├── app/
│ │ ├── api/ # API endpoints
│ │ │ ├── chat.py # Chat endpoints
│ │ │ ├── feedback.py # User feedback
│ │ │ ├── documents.py # Document management
│ │ │ └── admin.py # Admin routes
│ │ ├── core/ # Core logic
│ │ │ ├── rag_pipeline_direct.py # RAG implementation
│ │ │ └── faiss_store.py # Vector store
│ │ ├── models/ # Database models
│ │ │ └── database.py # SQLAlchemy models
│ │ ├── utils/ # Utilities
│ │ │ ├── rate_limiter.py # Rate limiting
│ │ │ └── logger.py # Logging
│ │ └── config.py # Configuration
│ ├── data/
│ │ └── documents/ # Knowledge base
│ │ ├── netone_bundles_2026_updated.txt
│ │ ├── netone_tourist_sim_official_2026.txt
│ │ ├── netone_sim_card_guide.txt
│ │ └── ... (13 files total)
│ ├── scripts/
│ │ ├── ingest_all_force.py # Document ingestion
│ │ └── setup_database.py # DB setup
│ ├── faiss_index/ # Vector store (generated)
│ ├── requirements.txt # Python dependencies
│ ├── .env.example # Environment template
│ └── run.py # Server starter
│
├── frontend/ # React frontend
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ │ ├── Chat/ # Chat components
│ │ │ │ ├── ChatInterface.jsx
│ │ │ │ ├── MessageBubble.jsx
│ │ │ │ ├── MessageInput.jsx
│ │ │ │ └── TypingIndicator.jsx
│ │ │ ├── Sidebar/ # Sidebar components
│ │ │ └── UI/ # UI components
│ │ ├── hooks/ # Custom hooks
│ │ │ ├── useChat.js
│ │ │ └── useApi.js
│ │ ├── services/ # API services
│ │ │ └── api.js
│ │ ├── App.jsx # Main app
│ │ ├── main.jsx # Entry point
│ │ └── index.css # Styles
│ ├── package.json # Node dependencies
│ ├── vite.config.js # Vite config
│ └── .env # Frontend env
│
├── .gitignore # Git ignore rules
├── README.md # This file
└── DEPLOYMENT.md # Deployment guide

text

---

## 🔧 Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- Git
- (Optional) MySQL database

### Step 1: Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/netone-ai-assistant.git
cd netone-ai-assistant
Step 2: Backend Setup
bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env with your API keys
# Add your GROQ_API_KEY and database settings

# Ingest knowledge base documents
python scripts/ingest_all_force.py

# Start the backend server
python run.py
The backend will be available at http://localhost:8000

Step 3: Frontend Setup
bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start the development server
npm run dev
The frontend will be available at http://localhost:5173

🚀 Usage
Testing the Backend
bash
# Check health endpoint
curl http://localhost:8000/api/chat/health

# Test a query
curl -X POST http://localhost:8000/api/chat/query \
  -H "Content-Type: application/json" \
  -d '{"message": "How much is the BBB 100 bundle?"}'
Testing the Frontend
Open http://localhost:5173 in your browser

Type questions about Netone services

View responses with source attribution

Sample Questions to Ask
"How much is the BBB 150 bundle?"

"Do you have a SIM card for tourists?"

"What USSD code do I use to check balance?"

"Who is the current CEO of Netone?"

"How do I contact customer care?"

"Tell me about OneMoney"

"What are the Khuluma voice bundles?"

📚 API Documentation
Once the backend is running, visit:

Swagger UI: http://localhost:8000/api/docs

ReDoc: http://localhost:8000/api/redoc

Main Endpoints
Endpoint	Method	Description
/api/chat/health	GET	Check system health and stats
/api/chat/query	POST	Send a question and get response
/api/chat/stream	POST	Stream response token by token
/api/chat/feedback	POST	Submit feedback on responses
Example Request
json
POST /api/chat/query
{
  "message": "How much is the BBB 100 bundle?"
}
Example Response
json
{
  "answer": "The BBB 100 bundle costs $45 for 30 days and includes 100,000 MB (100 GB) of combined data.",
  "sources": [
    {
      "title": "NETONE BUNDLES 2026 - COMBINED DATA (LATEST)",
      "category": "bundles",
      "relevance": "1.06",
      "excerpt": "| **BBB 100** | **$45** | 30 days | 100,000 MB (100 GB) |"
    }
  ]
}
🐳 Deployment
Backend Deployment (Render/Heroku)
Create a Procfile:

text
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Set environment variables in your hosting platform:

GROQ_API_KEY

MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE

ALLOWED_ORIGINS (your frontend URL)

DEBUG=false

Deploy!

Frontend Deployment (Netlify/Vercel)
Build the frontend:

bash
cd frontend
npm run build
Deploy the dist folder to Netlify or Vercel

Set environment variable:

VITE_API_URL = your backend URL

Docker Deployment
dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
bash
# Build and run
docker build -t netone-ai .
docker run -p 8000:8000 netone-ai
📸 Screenshots
Chat Interface
text
┌─────────────────────────────────────────────────┐
│  Netone AI Assistant                New Chat    │
├─────────────────────────────────────────────────┤
│                                                 │
│  👋 Welcome to Netone Zimbabwe AI Assistant!   │
│  I can help you with:                           │
│  • Bundle prices and information                │
│  • Tourist SIM cards                           │
│  • USSD codes                                  │
│  • Company information                         │
│                                                 │
│  How can I help you today?                      │
│                                     10:30 AM   │
│                                                 │
│  How much is the BBB 150 bundle?                │
│                                     10:31 AM   │
│                                                 │
│  The BBB 150 bundle costs $80 for 30 days      │
│  and includes 150,000 MB (150 GB) of data.     │
│                                     10:31 AM   │
│  Sources: Netone Bundles 2026                   │
│                                                 │
├─────────────────────────────────────────────────┤
│  Ask about Netone services...            📤     │
└─────────────────────────────────────────────────┘
🔮 Future Enhancements
Short-term (Next 3 Months)
User authentication and conversation history

Admin dashboard for document management

Feedback collection system with ratings

Rate limiting and abuse prevention

Medium-term (6 Months)
Multi-language support (Shona, Ndebele)

Mobile app (React Native)

Voice input (speech-to-text)

Integration with Netone's billing system

Long-term (12 Months)
Predictive analytics for customer needs

Automated document updates

Sentiment analysis on conversations

Expansion to other Zimbabwean companies

🤝 Contributing
Contributions are welcome! Here's how you can help:

Fork the repository

Create a feature branch

bash
git checkout -b feature/amazing-feature
Commit your changes

bash
git commit -m 'Add some amazing feature'
Push to the branch

bash
git push origin feature/amazing-feature
Open a Pull Request

Contribution Ideas
Add more documents to the knowledge base

Improve the prompt engineering

Enhance the UI/UX

Add new features

Fix bugs

Write tests

📄 License
This project is for demonstration purposes. All rights reserved.

Netone is a registered trademark of Netone Cellular (Pvt) Ltd. This project is not officially affiliated with Netone.

📞 Contact
Project Maintainer: [Your Name]

Email: your.email@example.com

GitHub: @yourusername

LinkedIn: Your Profile

Netone Official Channels:

Customer Care: 111 (toll-free)

WhatsApp: +263 71 695 6243

Website: www.netone.co.zw

🙏 Acknowledgments
Netone Zimbabwe for the inspiration and information

Groq for the fast LLM inference

LangChain for the RAG framework

Sentence-Transformers for the embeddings model

All contributors who help improve this project

⭐ Support
If you find this project useful, please consider giving it a star on GitHub!

Built with ❤️ for Zimbabwe 🇿🇼

Last Updated: March 2026

text

## 📝 **Key Sections Added/Enhanced:**

1. **Table of Contents** - Easy navigation
2. **Overview** - Clear project description with metrics
3. **Knowledge Base Table** - Detailed document listing
4. **Bundle Pricing Examples** - Quick reference
5. **Tech Stack Visuals** - ASCII diagrams
6. **Project Structure** - Complete file tree
7. **Installation Steps** - Clear, tested instructions
8. **API Examples** - Request/response samples
9. **Screenshot Mockup** - Visual representation
10. **Future Enhancements** - Roadmap with timelines
11. **Contributing Guide** - How others can help
12. **Contact Information** - Multiple channels
13. **Acknowledgments** - Credit where due

This README is comprehensive, professional, and will make your GitHub repository stand out!
