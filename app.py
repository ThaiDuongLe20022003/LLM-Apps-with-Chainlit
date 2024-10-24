import chainlit as cl
from src.llm import ask_order, messages

# Load the content of chainlit.md
try:
    with open("chainlit.md", "r", encoding="utf-8") as file:
        markdown_content = file.read()
except FileNotFoundError:
    markdown_content = "Markdown file not found. Please check the file path."

@cl.on_chat_start
async def send_welcome_message():
    # Send the markdown content when the chatbot is initialized
    await cl.Message(content=markdown_content).send()

@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    messages.append({"role": "user", "content": message.content})
    response = ask_order(messages)
    messages.append({"role": "assistant", "content": response})

    # Send a response back to the user
    await cl.Message(content=response).send()

# Note: You should also have a run command to start the Chainlit app
if __name__ == "__main__":
    cl.run(main)