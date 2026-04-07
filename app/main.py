
from rich.console import Console
from app.chat_engine import ChatEngine
from app.memory import ConversationMemory

def main():
    console = Console()
    console.print("[bold green]Jeff Message Printer[/bold green]")
    console.print("Press Enter to print the message, or type 'exit' to quit.\n")

    system_prompt = "You print a fixed Jeff message."
    memory = ConversationMemory(system_prompt)
    engine = ChatEngine()

    while True:
        user_input = console.input("[bold blue]You:[/bold blue] ")
        if user_input.lower() in ["exit", "quit"]:
            console.print("[bold red]Goodbye![/bold red]")
            break

        memory.add_user_input(user_input)
        response = engine.get_response(memory.get_messages())
        memory.add_assistant_response(response)

        console.print(f"[bold magenta]Result:[/bold magenta]\n{response}\n")

if __name__ == "__main__":
    main()
