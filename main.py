from model import model
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage
from tools import web_search
from prompt import SYSTEM_PROMPT, CHEF_PROMPT
from photo_handler import build_image_message, choose_image_file
from logger_handler import logging


logging.info("Starting the Recipe AI Agent...")
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[web_search],
)


logging.info("Agent created successfully. Ready to process images.")
image_path = choose_image_file()  # Prompt the user to select an image file

logging.info(f"Image selected: {image_path}. Building message for the agent.")
message = build_image_message(image_path, CHEF_PROMPT)  # Build the message with the image

logging.info("Invoking the agent with the image message.")
response = agent.invoke(
    {
        "messages": [
            message
        ]
    }
)

logging.info("Received response from the agent.")
print(response["messages"][-1].content)