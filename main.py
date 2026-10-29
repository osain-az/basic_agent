import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.tools import LLM_TOOLS


SYSTEM_INSTRUCTION = """You are a helpful sales assistant for NovaTech electronics.
Use the catalog tools before making product claims or recommendations. Ask a short
clarifying question when the customer's budget or intended use is unclear. Explain
why each recommendation fits, state prices in euros, and never invent products,
specifications, availability, discounts, or order details. A demo checkout is only
a quote and must be described as a simulation that does not charge the customer.
"""


def create_sales_chat():
    """Create a Gemini chat with automatic access to the sales tools."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing from the environment.")

    client = genai.Client(api_key=api_key)
    return client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=LLM_TOOLS,
        ),
    )


def main():
    chat = create_sales_chat()
    print("NovaTech sales agent ready. Type 'quit' to exit.")

    while True:
        message = input("You: ").strip()
        if message.lower() in {"quit", "exit"}:
            break
        if not message:
            continue

        response = chat.send_message(message)
        print(f"Agent: {response.text}")


if __name__ == "__main__":
    main()
