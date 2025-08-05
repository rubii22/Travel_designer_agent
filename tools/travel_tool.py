from agents.tool import function_tool

@function_tool("get_flights")
def get_flights(destination: str) -> str:
    return f"Mock flight options to {destination}: Flight A, Flight B, Flight C"

@function_tool("suggest_hotels")
def suggest_hotels(destination: str) -> str:
    return f"Mock hotel suggestions in {destination}: Hotel X, Hotel Y, Hotel Z"

@function_tool("get_experiences")
def get_experiences(destination: str) -> str:
    return f"Mock experiences in {destination}: Cooking class, City tour, Food tasting"

@function_tool("get_destination")
def get_destination(mood: str) -> str:
    if "relax" in mood.lower():
        return "Suggested destinations: Maldives, Bali, Santorini"
    elif "adventure" in mood.lower():
        return "Suggested destinations: Swiss Alps, Patagonia, Nepal"
    elif "culture" in mood.lower():
        return "Suggested destinations: Rome, Kyoto, Istanbul"
    else:
        return "Suggested destinations: Paris, Dubai, Thailand"
