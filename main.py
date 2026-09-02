from AI.UI.cli import CLI
from AI.Config.config import API
from AI.LLM.client import Client
from AI.Agent.agent import Agent


client =  Client(API.set_api()) 
agent = Agent(Client)

def app():
      client =  Client(API.set_api()) 
      agent = Agent(client)
      cli = CLI(agent)

      cli.run()

if __name__ == "__main__":
      app()