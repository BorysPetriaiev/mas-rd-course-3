import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import web_search, read_url, write_report
from config import SYSTEM_PROMPT

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
)

tools = [web_search, read_url, write_report]
checkpointer = MemorySaver()

agent_executor = create_react_agent(
    llm, 
    tools=tools, 
    prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer
)