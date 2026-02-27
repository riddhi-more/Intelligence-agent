# Autonomous Research Agent

An autonomous AI agent that reasons, searches the live web, performs calculations, and chains multiple tools together to answer complex multi-step questions. Demonstrates the ReAct pattern used in production agentic AI systems.

## What It Does

Ask a complex question. The agent autonomously decides which tools to use, in what order, and chains them to produce a complete answer — without any explicit if/else logic.

```
You: "What is the current population of Tokyo and how many times
      larger is it than London?"

🔍 Agent thinks: "I need to search for Tokyo's population."
   Agent calls:  TavilySearch("Tokyo population 2024")
   Agent gets:   "Tokyo population: approximately 13.96 million"

🔍 Agent thinks: "Now I need London's population."
   Agent calls:  TavilySearch("London population 2024")
   Agent gets:   "London population: approximately 8.9 million"

🧮 Agent thinks: "Now I can calculate the ratio."
   Agent calls:  calculator("13960000 / 8900000")
   Agent gets:   "Result: 1.57"

✅ Agent returns: "Tokyo (13.96M) is approximately 1.57 times larger than London (8.9M)."
```

## Chatbot vs RAG vs Agent

```
Chatbot   → answers from LLM training memory
             fixed knowledge, no real-time data, no actions

RAG       → answers from your documents
             private data, grounded responses, no real-time data

Agent     → takes autonomous actions
             live web search, real calculations,
             chains multiple steps, adapts based on results
```

## The ReAct Pattern — How the Agent Thinks

```
REASON  → "What do I need to answer this question?"
ACT     → Call the appropriate tool with the right input
OBSERVE → Read the tool result
REASON  → "Do I have enough or do I need another step?"
REPEAT  → Until the answer is complete
ANSWER  → Generate final response from all gathered information
```

The agent never follows a fixed script. It decides the path at runtime. The same agent handles single-step questions (one tool call) and complex multi-step questions (multiple chained calls) with identical code.

## Tools

| Tool | Purpose | Input | Production Equivalent |
|---|---|---|---|
| TavilySearch | Live web search | Search query string | Bing Search API |
| Calculator | Precise arithmetic | Math expression string | Same pattern |

## Why a 70B Model for Tool Calling?

Tool calling requires the LLM to generate valid structured JSON conforming to a schema. Testing showed:

```
Llama-3.1-8B  → malformed JSON on complex expressions
                 tool calls fail intermittently
                 not reliable enough for production

Llama-3.3-70B → 99%+ accurate tool call JSON
                 handles multi-tool chaining reliably
                 production-appropriate
```

Always benchmark tool call accuracy before committing to a model size.

## Security — Input Sanitisation on Calculator

The calculator uses Python's `eval()` to execute expressions. Without protection `eval()` will execute any Python code.

```python
# Without sanitisation — dangerous
eval("__import__('os').system('rm -rf /')")   # executes system commands

# With allowlist — safe
allowed = set('0123456789+-*/.() ')
# Only these characters can reach eval()
# Everything else is rejected before execution
```

Defence-in-depth: validation at the API gateway + JSON Schema check + allowlist inside the tool.

## Tech Stack

| Component | Development | Production Equivalent |
|---|---|---|
| LLM | Groq Llama-3.3-70B | Azure OpenAI GPT-4 |
| Orchestration | LangGraph + LangChain | LangGraph + Azure |
| Web search | Tavily | Bing Search API |
| Calculator | Python eval() + sanitisation | Same pattern |
| Tool interface | @tool decorator | Same pattern |

## Project Structure

```
autonomous-research-agent/
├── agent.py           # agent definition, tools, ReAct loop
├── .env               # API keys (never commit this)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
# 1. Clone and navigate
git clone <your-repo-url>
cd autonomous-research-agent

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install langgraph langchain langchain-groq langchain-tavily python-dotenv

# 4. Create .env file
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

# 5. Run
python agent.py
```

## Key Engineering Decisions

**Why Tavily over DuckDuckGo?**
Tavily returns clean structured JSON purpose-built for AI agents. DuckDuckGo returns raw HTML requiring parsing. Tavily provides an API key for monitoring and rate limiting — essential for controlling costs in production.

**Why does the docstring matter so much?**
The LLM reads tool docstrings to decide which tool to call. It semantically matches the user's question to each tool description. A vague docstring leads to wrong tool selection. Every docstring answers two questions: when to use this tool and how to format the input.

**Why a for loop in tool call handling?**
The LLM can decide to call the same tool multiple times in one response — for example searching for three different things at once. The for loop handles one tool call or ten with identical code. Without it only the first tool call executes and the rest are silently ignored.

**Why is the agent autonomous?**
There is no `if question mentions price, call search` logic anywhere. The LLM reads the question, reads the tool docstrings, and decides which tools to call. The execution path is different for every question — that is what makes it an agent rather than a scripted pipeline.

## Production Considerations

```
Tool validation      → validate tool call JSON against schema before executing
Retry logic          → retry with simplified prompt on malformed tool calls
Rate limiting        → cap tool calls per session to control API costs
Audit logging        → log every tool call with timestamp, input, output
Human checkpoints    → pause before irreversible actions for approval
Error handling       → tool failures return error strings, do not crash agent
```

## What Comes Next (Project 4)

Project 3 is one agent with multiple tools. Project 4 introduces three specialist agents — Researcher, Analyst, Writer — each with its own role and tools, communicating via shared state in a LangGraph graph.

## Skills Demonstrated

- ReAct agent architecture with autonomous tool selection
- Tool definition with @tool decorator and schema-aware docstrings
- Tool call handling — hasattr check, for loop, multi-tool if/elif routing
- Input sanitisation with character allowlist on eval()
- Model size benchmarking for tool calling reliability
- LangGraph agent orchestration
- Defence-in-depth input validation pattern
