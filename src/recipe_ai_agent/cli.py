from langchain.agents import create_agent
from .logger_handler import logging
from .model import model
from .photo_handler import build_image_message, choose_image_file
from .prompt import CHEF_PROMPT, SYSTEM_PROMPT
from .tools import web_search


def main() -> None:
    logging.info("Starting the Recipe AI Agent...")
    agent = create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[web_search],
    )

    logging.info("Agent created successfully. Ready to process images.")
    image_path = choose_image_file()

    logging.info("Image selected: %s. Building message for the agent.", image_path)
    message = build_image_message(image_path, CHEF_PROMPT)

    logging.info("Invoking the agent with the image message.")
    response = agent.invoke({"messages": [message]})

    logging.info("Received response from the agent.")
    print(response["messages"][-1].content)
