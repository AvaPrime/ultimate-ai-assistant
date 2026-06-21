from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from .tools import research, generate_image, analyze_image, send_email, add_to_notion_database
from .config import config

def create_agent():
    llm = ChatOpenAI(
        model=config.model,
        api_key=config.openrouter_key,
        base_url="https://openrouter.ai/api/v1",
        temperature=config.temperature,
        default_headers={
            "HTTP-Referer": "https://github.com/AvaPrime/ultimate-ai-assistant",
            "X-Title": "Ultimate AI Assistant"
        }
    )
    tools = [research, generate_image, analyze_image, send_email, add_to_notion_database]
    agent = create_react_agent(llm, tools)
    return AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True)