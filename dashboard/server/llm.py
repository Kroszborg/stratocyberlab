import asyncio
from ollama import AsyncClient


BASE_URL = "http://172.30.0.100:11434/"
PROMPT = """
You are a cybersecurity expert assistant for StratoCyberLab. Keep responses concise and practical.
Important network information:
- The lab uses subnet 172.30.0.0/24
- The hackerlab container is at 172.30.0.2
- The dashboard is at 172.30.0.3
- The ollama service is at 172.30.0.100
- Challenge containers use IPs starting with 172.30.0.x

When helping with challenges:
- Always use the correct subnet (172.30.0.x)
- Verify IP addresses before suggesting them
- Guide users to use proper tools (nmap, curl, etc.)
- Encourage learning and understanding of commands
"""
DEFAULT_MODEL = "llama3.1"  # Using the already downloaded model
INIT_MESSAGES = [
    {"role": "system", "content": PROMPT},
    {"role": "assistant", "content": "Hi! I'm your cybersecurity assistant. I'll help you with the challenges using the correct network setup (172.30.0.0/24). What can I help you with?"}
]

client = AsyncClient(host=BASE_URL)


async def is_model_available(model: str = DEFAULT_MODEL) -> bool:
    """
    Check if the model is downloaded
    """
    models_dict = await client.list()
    models = models_dict["models"]

    if models is None:
        return False

    found = False
    for m in models:
        if model in m["name"]:
            found = True
    return found


async def pull_model(model: str = DEFAULT_MODEL):
    if not await is_model_available(model):
        response = await client.pull(model, stream=False)

        if response["status"] != "success":
            raise Exception(f"Error pulling model: {response}")


async def chat_with_llm(messages: list, model: str = DEFAULT_MODEL) -> list:
    """
    Send a chat reuest to the model defined by the model string.
    The last message in the list should contain a "user" role and the question.
    """
    # If the model is not present pull it
    if not await is_model_available(model):
        await pull_model(model)

    input_messages = INIT_MESSAGES + messages
    response = await client.chat(model=model, messages=input_messages)

    messages.append(
        {"role": "assistant", "content": response['message']['content']})
    return messages


async def delete_local_model(model: str = DEFAULT_MODEL):
    """Delete the local model"""
    if await is_model_available(model):
        await client.delete(model)


async def main():
    chat_messages = [{
        "role": "user", "content": "What does the tcpdump command do?"
    }]

    messages = await chat_with_llm(chat_messages, model="phi3")
    print(messages)

    # Delete the model
    # await delete_local_model("phi3")

if __name__ == '__main__':
    asyncio.run(main())
