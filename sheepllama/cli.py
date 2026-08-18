import os
import sys
import argparse
from groq import Groq
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live

console = Console()

def get_client():
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        console.print("[bold red]Error: GROQ_API_KEY environment variable not found.[/bold red]")
        sys.exit(1)
    return Groq(api_key=key)

def stream(client, messages, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        full_text = ""
        with Live(Markdown(""), refresh_per_second=15, console=console) as live:
            for chunk in response:
                content = chunk.choices.delta.content
                if content:
                    full_text += content
                    live.update(Markdown(full_text))
        return full_text
    except Exception as e:
        console.print(f"\n[bold red]Groq API Error:[/bold red] {e}")
        sys.exit(1)

def interactive_chat(client, model, system_prompt):
    console.print(f"[bold green]Sheepllama Interactive Session ({model})[/bold green]")
    console.print("[dim]Type 'exit' or 'quit' to close.[/dim]\n")
    
    history = [{"role": "system", "content": system_prompt}]
    
    while True:
        try:
            user_input = console.input("[bold purple]You > [/bold purple]").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                break
                
            history.append({"role": "user", "content": user_input})
            console.print("\n[bold cyan]Sheepllama:[/bold cyan]")
            
            reply = stream(client, history, model)
            history.append({"role": "assistant", "content": reply})
            console.print()
            
        except (KeyboardInterrupt, EOFError):
            break

def main():
    # Hard runtime block ensuring execution only happens on 3.10 - 3.14
    if sys.version_info >= (3, 15):
        console.print(
            f"[bold red]Error:[/bold red] Python {sys.version_info.major}.{sys.version_info.minor} is unsupported.\n"
            "[yellow]Sheepllama-CLI strictly supports Python 3.10, 3.11, 3.12, 3.13, and 3.14 only.[/yellow]"
        )
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Sheepllama-CLI")
    parser.add_argument("prompt", nargs="?", type=str, help="Your quick AI prompt")
    parser.add_argument("-m", "--model", default="llama-3.3-70b-versatile", help="Groq Model ID")
    parser.add_argument("-s", "--system", default="You are Sheepllama, a fast AI assistant.", help="System context")
    args = parser.parse_args()

    client = get_client()

    # Case 1: Standard Input / File Piping (e.g., cat text.log | sheepllama)
    if not sys.stdin.isatty():
        piped_data = sys.stdin.read().strip()
        final_prompt = f"{args.prompt}\n\n{piped_data}" if args.prompt else piped_data
        stream(client, [{"role": "system", "content": args.system}, {"role": "user", "content": final_prompt}], args.model)
        sys.exit(0)

    # Case 2: No inline string provided -> Start persistent chat loop
    if not args.prompt:
        interactive_chat(client, args.model, args.system)
        sys.exit(0)

    # Case 3: Simple quick single prompt command
    stream(client, [{"role": "system", "content": args.system}, {"role": "user", "content": args.prompt}], args.model)

if __name__ == "__main__":
    main()
