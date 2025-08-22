from agents import Agent, Runner, tool, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI
from dotenv import load_dotenv
import os
from tools import get_web_data

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,
)


agent = Agent(
   name="Web Search Agent",
    instructions = """
    You are a helpful assistant with access to real-time web search.
    - Use the get_web_data search tool whenever the user asks for up-to-date information (e.g., news, esports, live data, sports)
      OR things you dont know.
    - Always return concise, clear answers based on the search results.
    - Include source links when possible.
    """,
    tools=[get_web_data], #<---- realtime data with web_data from tavily api mention in assignment form https://www.tavily.com/
    tool_use_behavior="stop_on_first_tool" #<--- using this for both (e.g what is 3+2 and what is the weather of gaza) query at a time.
    # tool_use_behavior='stop_on_first_tool' #<--- using this for 1 query at a time.
)


def ask_agent(query: str):
    res = Runner.run_sync(
        agent,
        input=query,
        run_config=config,
    )
    print(f"You: {query}")
    print(f"Agent: {res.final_output}\n")


if __name__ == "__main__":
    print('welcome i am helpful general agents with a Web Search Tool')
    user_input=str(input('Enter your query: '))
    ask_agent(user_input)
