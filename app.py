from pathlib import Path
import chainlit as cl
from src.llm import ask_order, messages

@cl.on_chat_start
@cl.on_message
async def main(message: cl.Message = None):
    # This part will execute during chat start
    if message is None:
        # Add startup message
        language = cl.user_session.get("languages").split(",")[0]

        root_path = Path(__file__).parent
        
        translated_chainlit_md_path = root_path / f"chainlit_{language}.md"
        default_chainlit_md_path = root_path / "chainlit.md"
        
        # Check if translated markdown exists, otherwise use the default
        if translated_chainlit_md_path.exists():
            message_content = translated_chainlit_md_path.read_text()
        else:
            message_content = default_chainlit_md_path.read_text()
        
        startup_message = cl.Message(content=message_content)
        await startup_message.send()
    
    # This part will execute when a user sends a message
    else:
        # Custom message handling logic
        messages.append({"role": "user", "content": message.content})
        
        # Generate assistant's response
        response = ask_order(messages)
        messages.append({"role": "assistant", "content": response})

        # Send the response back to the user
        await cl.Message(content=response).send()
