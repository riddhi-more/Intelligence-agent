# 📊 Market Intelligence Agent

An AI-powered agent that answers complex financial and market 
questions by autonomously searching the web, performing 
calculations, and analysing text — built with LangChain, 
LangGraph, and Groq.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-1.x-green)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70b-purple)
![Tavily](https://img.shields.io/badge/Tavily-Search_API-orange)
![Free](https://img.shields.io/badge/APIs-Free_Tier-brightgreen)

---

## 🚀 What It Does

Ask complex questions that require multiple steps to answer:

- **"What is the Bank of England base rate and how much 
  interest would £10,000 earn in a year?"**
  → Agent searches for rate, then calculates interest

- **"What is Barclays current share price and what would 
  500 shares cost?"**
  → Agent searches price, then calculates total cost

- **"How many words are in this market report summary?"**
  → Agent analyses the text directly

---

## 🧠 How It Works — ReAct Loop
```
User Question
     ↓
REASON  → What do I need to answer this?
ACT     → Call the right tool
OBSERVE → Read what the tool returned
REPEAT  → Do I have the full answer?
     ↓
Final Answer
```

---

## 🛠️ Tech Stack

| Tool | Purpose | Production Equivalent |
|------|---------|----------------------|
| LangGraph | Agent orchestration | LangGraph Enterprise |
| LangChain | Framework | LangChain |
| Groq API | LLM inference (free) | Azure OpenAI / AWS Bedrock |
| Tavily Search | Web search (free) | Bing Search API |
| llama-3.3-70b | Language model | GPT-4 / Claude |
| Streamlit | Web UI | React / Internal portal |

---

## 🔧 Three Tools

**Tool 1 — Tavily Web Search**
Searches the internet for real-time information.
Production equivalent: Bing Search API, Bloomberg Terminal API

**Tool 2 — Calculator**
Performs mathematical calculations with input sanitisation.
Prevents code injection via allowed character validation.

**Tool 3 — Text Analyser**
Counts words, characters, and sentences in any text.

---

## 📁 Project Structure
```
market-intelligence-agent/
│
├── agent.py        # Core agent logic — brain + tools
├── app.py          # Streamlit UI layer
├── .env            # API keys (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/market-intelligence-agent.git
cd market-intelligence-agent
```

### 2. Create virtual environment
```bash
py -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install langchain langchain-groq langchain-community 
            langchain-tavily langgraph python-dotenv streamlit
```

### 4. Get free API keys
- **Groq:** console.groq.com (free, no credit card)
- **Tavily:** tavily.com (free, 1000 searches/month)

### 5. Add API keys
Create `.env` file:
```
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

### 6. Run
```bash
# Terminal mode
python agent.py

# Web UI
streamlit run app.py
```

---

## 💡 Key Engineering Decisions

**Why LangGraph over old LangChain agents?**
LangGraph 1.x consolidated agent orchestration — 
the ReAct loop, prompt management, and execution 
are all built into `create_agent`. Cleaner, more 
maintainable, and the direction LangChain is moving.

**Why Tavily over DuckDuckGo?**
Tavily is purpose-built for AI agents — returns 
structured, AI-optimised results. DuckDuckGo returns 
raw HTML scrapes. In production I would use Bing 
Search API or Bloomberg Terminal API.

**Why llama-3.3-70b over 8b?**
Tool calling requires strong reasoning. The 8b model 
generates malformed function calls on complex expressions.
70b handles multi-step tool orchestration reliably.

**Why input sanitisation on calculator?**
`eval()` executes any Python code. Without sanitisation 
a malicious user could inject system commands. 
Allowing only `0-9 + - * / . ( )` prevents code injection.

---

## 🏦 Enterprise Context

Built as a proof of concept for a market intelligence 
assistant at a financial services firm. The agent can be 
extended with:

- Bloomberg Terminal API for live market data
- Internal RAG system for company documentation  
- Jira integration for automatic incident creation
- Teams/Slack integration for alert notifications

---

## 🔮 Coming Soon

- [ ] LangGraph multi-agent workflow (Project 4)
- [ ] Azure OpenAI integration
- [ ] Bing Search API swap
- [ ] Async tool execution for faster responses

---

## 📄 License

MIT License — free to use and modify.
