from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()
def welcome_screen():

    welcome = Panel(
     Text("✈️ Welcome to Pilot Code", style="bold white"),
     border_style="#19e4f7",
     padding=(0, 1),
     expand=False,
    )
    console.print(Align.center(welcome))
    

# Your logo
    logo = r"""
 ██████╗ ██╗██╗      ██████╗ ████████╗
██╔══██╗██║██║     ██╔═══██╗╚══██╔══╝
██████╔╝██║██║     ██║   ██║   ██║
██╔═══╝ ██║██║     ██║   ██║   ██║
██║     ██║███████╗╚██████╔╝   ██║
╚═╝     ╚═╝╚══════╝ ╚═════╝    ╚═╝

 ██████╗ ██████╗ ██████╗ ███████╗
██╔════╝██╔═══██╗██╔══██╗██╔════╝
██║     ██║   ██║██║  ██║█████╗
██║     ██║   ██║██║  ██║██╔══╝
╚██████╗╚██████╔╝██████╔╝███████╗
 ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
"""

    logo_text = Text(logo)
    logo_text.stylize("#19e4f7")

    console.print()
    console.print()

# Center the logo
    console.print(Align.center(logo_text))

    console.print()
    console.print(
     Align.center(
        Text("Press Enter to continue", style="dim cyan")
     ) 
    )