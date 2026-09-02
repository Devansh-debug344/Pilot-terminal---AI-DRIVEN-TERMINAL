import typer , os 
from pathlib import Path
from rich.console import Console
import subprocess
from .cliscreen import welcome_screen
from AI.Agent.agent import Agent
# import tkinter as tk
# from tkinter import filedialog
app = typer.Typer()
console = Console()
# welcome_screen()

class CLI:
    def __init__(self , agent : Agent):
        self.agent = agent
    
    def get_response(self , query : str):
        try:
           res = self.agent.request(query)

           return res

        except RuntimeError as ce:
           raise RuntimeError(f"Error {ce} in search function") from ce


# def gui():
#     root = tk.Tk()
#     root.title("PILOT TERMINAL")

#     tk.Label(root, text="Filename").pack()
#     filename_entry = tk.Entry(root, width=40)
#     filename_entry.pack()

#     tk.Label(root, text="Threshold").pack()
#     threshold_entry = tk.Entry(root)
#     threshold_entry.insert(0, "0.8")
#     threshold_entry.pack()

#     def run():
#         filename = filename_entry.get()
#         threshold = float(threshold_entry.get())
#         process_file(filename, threshold)

#     tk.Button(root, text="Process", command=run).pack(pady=10)

#     root.mainloop()

    def run(self):
      @app.command()
      def search(query : str) -> None:

        messages = self.get_response(query)

    # console.print(messages[len(messages) - 1].get('content'))
    # console.print(messages)
        console.print(messages)
        console.print("\n✨ Done!\n")
      app() 