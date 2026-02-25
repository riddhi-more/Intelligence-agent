from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain.tools import tool
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()

# BRAIN — Groq LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"  # upgraded from 8b to 70b older- llama-3.1-8b-instant"
)

# TOOL 1 — Web Search
search_tool = TavilySearch(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=3
)

# TOOL 2 — Calculator
@tool
def calculator(expression: str) -> str:
    """
    Useful for mathematical calculations.
    Input must be valid Python math expression.
    Use only numbers and operators + - * / and parentheses.
    Convert percentages to decimals. Example: 4.5% = 0.045
    """
    try:
        expression = expression.replace('%', '/100')
        expression = expression.replace('^', '**')
        allowed = set('0123456789+-*/.() ')
        if not all(c in allowed for c in expression):
            return "Invalid expression. Use only numbers and operators."
        result = eval(expression)
        return f"The result is: {result:.2f}"
    except Exception as e:
        return f"Could not calculate: {str(e)}"

# TOOL 3 — Text Analyser
@tool
def text_analyser(text: str) -> str:
    """
    Useful for analysing text.
    Use this when asked to count words, characters,
    or analyse the length of any text.
    """
    words = len(text.split())
    characters = len(text)
    sentences = text.count('.') + text.count('!') + text.count('?')
    return f"Words: {words}, Characters: {characters}, Sentences: {sentences}"

# Collect tools
tools = [search_tool, calculator, text_analyser]

# CREATE AGENT — brain + tools connected
agent = create_agent(
    model=llm,
    tools=tools
)

# RUN FUNCTION
def run_agent(question):
    print(f"\nQuestion: {question}")
    print("-" * 50)
    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })
    final_answer = result["messages"][-1].content
    print(f"\nFinal Answer: {final_answer}")
    return final_answer

# TEST
if __name__ == "__main__":
    run_agent("What is the current Bank of England base interest rate?")
    run_agent("If I invest 5000 at 0.045 annual interest for 3 years what is the total?")
    run_agent("How many words are in this sentence: The quick brown fox jumps over the lazy dog")
