import asyncio
from agents import Agent, RunConfig, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
from agents import function_tool
from openai import AsyncOpenAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import pprint
load_dotenv()

GEMINI_MODEL: str = "gemini-2.0-flash"
GEMINI_API_KEY: str = "AIzaSyCLWffaoJ6tXGvrXfzzhBJyAznLVd-5YAA"
BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/openai/"

set_tracing_disabled(disabled=True)

client: AsyncOpenAI = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(model=GEMINI_MODEL, openai_client=client)
inventory = {}
class InventoryItem(BaseModel):
    item_name: str
    quantity: int

class UpdateItem(BaseModel):
    item_name: str
    new_quantity: int

@function_tool
def add_item(item: InventoryItem):
    """Add a new item to the inventory or increase quantity."""
    if item.item_name in inventory:
        inventory[item.item_name] += item.quantity
    else:
        inventory[item.item_name] = item.quantity
    return {"status": "success", "inventory": inventory}

@function_tool
def remove_item(item: InventoryItem):
    """Remove an item or decrease its quantity."""
    if item.item_name in inventory:
        inventory[item.item_name] -= item.quantity
        if inventory[item.item_name] <= 0:
            del inventory[item.item_name]
        return {"status": "success", "inventory": inventory}
    return {"status": "failed", "reason": "Item not found", "inventory": inventory}

@function_tool
def update_item(item: UpdateItem):
    """Update item quantity in the inventory."""
    if item.item_name in inventory:
        inventory[item.item_name] = item.new_quantity
        return {"status": "success", "inventory": inventory}
    return {"status": "failed", "reason": "Item not found", "inventory": inventory}

add_agent = Agent(
    name="Add Agent",
    instructions="You add items to the inventory.",
    tools=[add_item]
)

remove_agent = Agent(
    name="Remove Agent",
    instructions="You remove items from the inventory.",
    tools=[remove_item]
)

update_agent = Agent(
    name="Update Agent",
    instructions="You update item quantities in the inventory.",
    tools=[update_item]
)
async def main():
    print("\n--- Adding Item ---")
    result1 = await Runner.run(
        add_agent,
        "Add 10 mangoes",
        run_config=RunConfig(model=model)
    )
    pprint.pprint(result1.final_output)

    print("\n--- Removing Item ---")
    result2 = await Runner.run(
        remove_agent,
        "Remove 2 mangoes",
        run_config=RunConfig(model=model)
    )
    pprint.pprint(result2.final_output)

    print("\n--- Updating Item ---")
    result3 = await Runner.run(
        update_agent,
        "Update mangoes to 30 ",
        run_config=RunConfig(model=model)
    )
    pprint.pprint(result3.final_output)

    print("\n--- Final Inventory ---")
    pprint.pprint(inventory)

def start():
    asyncio.run(main())

if __name__ == "__main__":
    start()
