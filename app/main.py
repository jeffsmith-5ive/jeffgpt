
from rich.console import Console
from app.chat_engine import ChatEngine
from app.memory import ConversationMemory

def main():
    console = Console()
    console.print("[bold green]Calculator + Number Decoder[/bold green]")
    console.print("Type a math problem to use the calculator.")
    console.print("Type number codes to decode letters with A1Z26.")
    console.print("Example: 8 9 / 13 25 / 14 1 13 5")
    console.print("Press Enter for help, or type 'exit' to quit.\n")

    system_prompt = "You are a calculator with a number-to-letter decoder."
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
