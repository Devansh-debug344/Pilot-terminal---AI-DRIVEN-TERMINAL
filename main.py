from AI.Agent.agent import Agent
from AI.Config.config import API
from AI.LLM.client import Client
from AI.UI.cliscreen import PilotApp
from AI.UI.cli import CLI

def app():
    client = Client(API.set_api())
    agent = Agent(client)
    PilotApp(agent=agent).run()
    # CLI(agent=agent).run()

if __name__ == "__main__":
      app()
