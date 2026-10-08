"""
Roorkee Help AI Agent - Command Line Interface (CLI)
Allows chatting with the Roorkee AI Agent directly inside the VS Code terminal.
"""

import sys
from agent import RoorkeeAIAgent

# Ensure safe output on Windows terminal
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


def main():
    print("=" * 65)
    print("  🏛️  ROORKEE HELP AI AGENT - TERMINAL INTERFACE  🏛️")
    print("=" * 65)
    print("Type your questions about Roorkee (Emergency, IIT, Heritage, Food, Trains, etc.)")
    print("Type 'exit' or 'quit' to end.\n")

    agent = RoorkeeAIAgent()

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nGoodbye! Have a great time in Roorkee! 🙏")
                break

            response = agent.generate_response(user_input)
            print("\n" + "-" * 60)
            print(f"🤖 Roorkee AI [Intent: {response['category']}]:")
            print(response["answer"])
            print("-" * 60)

            if response.get("follow_up_suggestions"):
                print("💡 Suggestions you can ask:")
                for s in response["follow_up_suggestions"]:
                    print(f"   • {s}")

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended. 🙏")
            break


if __name__ == "__main__":
    main()
