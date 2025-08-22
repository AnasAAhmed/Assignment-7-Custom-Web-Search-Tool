from agents import function_tool
from dotenv import load_dotenv
import os
from tavily import TavilyClient
import requests
load_dotenv()

API_KEY = os.getenv('TAVILY_API_KEY')

@function_tool
def get_web_data(query: str):
    """this is a WebSearchTool to Fetch data/info from webpages of a given query. It is basically a web scraper."""
    print('get_web_data tools hits <---')

    try:
        tavily_client = TavilyClient(api_key=API_KEY)
        response = tavily_client.search(query=query,max_results=5)

        #extracting ifo from json data in strinf
        formatted = []
        for r in response["results"]:
         formatted.append(f"{r['title']} - {r['url']}\n{r['content']}")
        
        return "\n\n".join(formatted)
    
         #  e.g response return to agent
         # (title)4thrives Esports PUBG Mobile Team gets the 7th spot on PUBG World Cup at EWC for Pakistan - (url)https://www.gosugamers.net/pubg-mobile/teams/56593-4thrives-esports
         # (content)4THRIVES ESPORTS. participant-logo. 4thrives Esports. 4thrives. PK Pakistan ... Total Earnings. $18,750. Current Streak. 0. ,
         # (title)4thrives Esports - Liquipedia PUBG Mobile Wiki - (url)https://liquipedia.net/pubgmobile/4thrives_Esports
         # (content)4thrives Esports is a Pakistani PUBG Mobile Team ... Total Winnings : $182,594.

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data for city: {e}"
    except KeyError:
        return "Could not parse weather data lol."


