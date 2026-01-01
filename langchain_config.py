import os
from dotenv import load_dotenv
from newsapi import NewsApiClient
from loguru import logger

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# Load environment variables
load_dotenv()

# ----------- API KEYS -----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

if not NEWS_API_KEY:
    raise RuntimeError("NEWS_API_KEY not set")

# ----------- LLM -----------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=OPENAI_API_KEY,
)

# ----------- NEWS API -----------
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

def get_news_articles(query: str):
    try:
        response = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",
            page_size=3
        )
        return response.get("articles", [])
    except Exception as e:
        logger.error(f"NewsAPI error: {e}")
        return []

# ✅ THIS FUNCTION MUST EXIST AT TOP LEVEL
def get_summary(query: str) -> str:
    articles = get_news_articles(query)

    summaries = " ".join(
        [article.get("description", "") or "" for article in articles]
    )

    if not summaries.strip():
        return "No relevant news articles found."

    prompt = PromptTemplate.from_template(
        """
        You are an equity research analyst.

        Query:
        {query}

        News summaries:
        {summaries}

        Provide a concise, investment-focused summary.
        """
    )

    chain = RunnableSequence(prompt, llm)

    result = chain.invoke({
        "query": query,
        "summaries": summaries
    })

    return result
