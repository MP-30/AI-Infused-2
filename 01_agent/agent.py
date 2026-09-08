import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

PRICES = {
    "shoes": 799,
    "hat": 399,
    "bag": 1420,
    "shorts": 1299,
    "pants": 1699,
}


def get_price(item):
    print(f"🔧 tool called: get_price({item})")

    return f"₹{PRICES.get(item.lower(), 'unknown')}"


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_price",
            "description": "Get the price of a shop item the user asks about.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The item name",
                    }
                },
                "required": ["item"],
            },
        },
    }
]


def agent(user_message):
    messages = [
        {
            "role": "user",
            "content": user_message,
        }
    ]

    # 1. Send user message + available tools to the model
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages,
        tools=tools,
    )

    msg = response.choices[0].message

    # 2. Check whether the model requested a tool
    if msg.tool_calls:
        # Add assistant's tool-call message
        messages.append(msg)

        # 3. Execute each requested tool
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)

            result = get_price(args["item"])

            # Add tool result back to conversation
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )

        # 4. Send tool result back to model
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=messages,
        )

        msg = response.choices[0].message

    return msg.content

if __name__ == "__main__":
    print(agent("How much are the Hat?"))
    print(agent("Hi! What can you help with?"))