from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistralAI
import asyncio
from mcp_use import MCPAgent, MCPClient
import os

load_dotenv()

# load api keys
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")

# config path
config_file = "browser_mcp.json"

# model 
model_llama = "llama-3.1-8b-instant"
model_mistral = "mistral-large-latest"

use_mistral = True

async def run_memory_chat():



    # create MCP client and agent with memory enabled
    client = MCPClient.from_config_file(config_file)

    if use_mistral:
        llm = ChatMistralAI(model_name=model_mistral)
    else:    
        llm = ChatGroq(model=model_llama)
    print("Initializing Chat...")

    # create agent with memory_enabled=True
    agent = MCPAgent(
        llm=llm,
        client=client,
        # mex_steps=15,
        memory_enabled=True
    ) 

    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("=================================\n")

    try:
        while True:
            # get user input
            user_input = input("\n: ")

            # check for exit command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # run the agent with user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response
                )
            except Exception as e:
                print(f"Error: {str(e)}")

    finally:
        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(run_memory_chat())








