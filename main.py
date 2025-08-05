import os
from dotenv import load_dotenv
import chainlit as cl

from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff
from tools.travel_tool import get_flights, suggest_hotels, get_experiences, get_destination

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Setup Gemini client and model
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# DestinationAgent
destination_agent = Agent(
    name="DestinationAgent",
    instructions="""
You help users find travel destinations based on their mood or interests.
Always use the `get_destination` tool.
Start your response with: "Based on your mood, here are some destinations you might love:"
Never generate destinations yourself — only use the tool.
""",
    model=model,
    tools=[get_destination]
)

# BookingAgent
booking_agent = Agent(
    name="BookingAgent",
    instructions="""
You help users book flights and hotels.
Use `get_flights` and `suggest_hotels` tools ONLY.
Start responses with something like:
- "Here are some mock flight options I found:"
- "These are some hotel suggestions you might consider:"
Never make up bookings yourself.
""",
    model=model,
    tools=[get_flights, suggest_hotels]
)

# ExploreAgent
explore_agent = Agent(
    name="ExploreAgent",
    instructions="""
You suggest local attractions, experiences, and food in a destination.
Always use the `get_experiences` tool.
Start your response with: "Here are some great experiences and foods to explore:"
Do not generate experiences yourself — always use the tool.
""",
    model=model,
    tools=[get_experiences]
)

# TriageAgent
triage_agent = Agent(
    name="TriageAgent",
    instructions="""
You are responsible for routing user queries to the right expert agent:
- If user wants to find a destination: delegate to DestinationAgent
- If they want to book flights or hotels: delegate to BookingAgent
- If they want to explore things to do or food: delegate to ExploreAgent
Always respond with the final output of the delegated agent.
""",
    model=model,
    handoffs=[
        handoff(agent=destination_agent),
        handoff(agent=booking_agent),
        handoff(agent=explore_agent)
    ]
)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=(
            "**Welcome to Travel Designer Assistant! ✈️🌍**\n\n"
            "I'm here to help you:\n"
            "👉 Find travel destinations based on your mood\n"
            "👉 Book mock flights and hotels\n"
            "👉 Explore local attractions and food experiences\n\n"
            "Just type what you're looking for!"
        )
    ).send()

# Message Handler
@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    result = await Runner.run(triage_agent, user_input)
    await cl.Message(content=result.final_output).send()
