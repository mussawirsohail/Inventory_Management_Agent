# # import re
# # from typing import Dict, Optional
# # from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel
# # from openai import AsyncOpenAI
# # from agents.tool import function_tool
# # import asyncio

# # import openai


# # GEMINI_MODEL = "gemini-2.0-flash"
# # GEMINI_API_KEY= "AIzaSyC--c4sf_xlddjaAgR_29YnsJzPVvlLtCc"
# # BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# # set_tracing_disabled(disabled = True)


# # class Item:
# #     def __init__(self, id: str, name: str, quantity: int, price: float):
# #         self.id = id
# #         self.name = name
# #         self.quantity = quantity
# #         self.price = price
# #     def __repr__(self):
# #         return f"Item(id={self.id}, name={self.name}, quantity={self.quantity}, price={self.price})"

# # inventory: Dict[str, Item] = {}

# # class Agent:
# #     def run(self, *args, **kwargs):
# #         raise NotImplementedError()

# # class AddAgent(Agent):
# #     def run(self, id: str, name: str, quantity: int, price: float):
# #         item = Item(id, name, quantity, price)
# #         inventory[id] = item
# #         return f"Added item: {item}"

# # class RemoveAgent(Agent):
# #     def run(self, id: str):
# #         item = inventory.pop(id, None)
# #         if item:
# #             return f"Removed item: {item}"
# #         else:
# #             return f"No item found with id {id}."

# # class UpdateAgent(Agent):
# #     def run(self, id: str, name: Optional[str]=None, quantity: Optional[int]=None, price: Optional[float]=None):
# #         item = inventory.get(id)
# #         if not item:
# #             return f"No item found with id {id}."
# #         if name is not None:
# #             item.name = name
# #         if quantity is not None:
# #             item.quantity = quantity
# #         if price is not None:
# #             item.price = price
# #         return f"Updated item: {item}"

# # # --- LLM Router ---
# # def llm_router(prompt: str):
# #     response = openai.ChatCompletion.create(
# #         model="gpt-3.5-turbo",
# #         messages=[
# #             {"role": "system", "content": "You are an inventory management assistant. You can add, remove, or update items."},
# #             {"role": "user", "content": prompt}
# #         ]
# #     )
# #     return response.choices[0].message['content']

# # # --- Simple intent parser (from LLM output or user prompt) ---
# # def parse_intent(text: str):
# #     text = text.lower()
# #     if "add" in text:
# #         match = re.search(r'id=(\S+),? name=(\S[\w ]+),? quantity=(\d+),? price=([\d.]+)', text)
# #         if match:
# #             return {
# #                 "agent": "add",
# #                 "id": match.group(1),
# #                 "name": match.group(2),
# #                 "quantity": int(match.group(3)),
# #                 "price": float(match.group(4))
# #             }
# #     elif "remove" in text or "delete" in text:
# #         match = re.search(r'id=(\S+)', text)
# #         if match:
# #             return {"agent": "remove", "id": match.group(1)}
# #     elif "update" in text:
# #         match = re.search(r'id=(\S+)(?:,? name=(\S[\w ]+))?(?:,? quantity=(\d+))?(?:,? price=([\d.]+))?', text)
# #         if match:
# #             return {
# #                 "agent": "update",
# #                 "id": match.group(1),
# #                 "name": match.group(2) if match.group(2) else None,
# #                 "quantity": int(match.group(3)) if match.group(3) else None,
# #                 "price": float(match.group(4)) if match.group(4) else None
# #             }
# #     return None

# # # --- Demo Runner ---
# # def demo():
# #     add_agent = AddAgent()
# #     remove_agent = RemoveAgent()
# #     update_agent = UpdateAgent()

# #     print("\n=== DEMO: LLM Router ===\n")
# #     prompts = [
# #         "Add a new item: id=SKU-1, name=Blue Pen, quantity=100, price=0.5",
# #         "Add item id=SKU-2 name=Notebook quantity=50 price=1.25",
# #         "Update item id=SKU-1 quantity=120 price=0.45",
# #         "Delete item id=SKU-2"
# #     ]
# #     for prompt in prompts:
# #         llm_response = llm_router(prompt)
# #         print(f"LLM response: {llm_response}")
# #         intent = parse_intent(prompt)
# #         if intent:
# #             if intent["agent"] == "add":
# #                 print(add_agent.run(intent["id"], intent["name"], intent["quantity"], intent["price"]))
# #             elif intent["agent"] == "remove":
# #                 print(remove_agent.run(intent["id"]))
# #             elif intent["agent"] == "update":
# #                 print(update_agent.run(intent["id"], name=intent.get("name"), quantity=intent.get("quantity"), price=intent.get("price")))
# #         print("Inventory:", list(inventory.values()))

# #     print("\n=== INVENTORY SNAPSHOT ===")
# #     print(list(inventory.values()))

# # if __name__ == "__main__":
# #     demo()











# import uuid
# from typing import Dict, List, Optional
# from agents import Agent as AISDKAgent, Runner, set_tracing_disabled
# from agents import OpenAIChatCompletionsModel, function_tool
# from openai import AsyncOpenAI
# import asyncio

# # Gemini configuration (using OpenAI-compatible endpoint)
# GEMINI_MODEL = "gemini-2.0-flash"
# GEMINI_API_KEY = "AIzaSyC--c4sf_xlddjaAgR_29YnsJzPVvlLtCc"  # Replace with your actual API key
# BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
# set_tracing_disabled(disabled=True)

# class SystemAgent:
#     def __init__(self, name: str, role: str, permissions: List[str]):
#         self.id = str(uuid.uuid4())
#         self.name = name
#         self.role = role
#         self.permissions = permissions
#         self.is_active = True

#     def __repr__(self):
#         return f"SystemAgent(id={self.id}, name={self.name}, role={self.role}, active={self.is_active})"

# class InventoryItem:
#     def __init__(self, name: str, category: str, quantity: int, price: float):
#         self.id = str(uuid.uuid4())
#         self.name = name
#         self.category = category
#         self.quantity = quantity
#         self.price = price

#     def __repr__(self):
#         return (f"InventoryItem(id={self.id}, name={self.name}, "
#                 f"category={self.category}, quantity={self.quantity}, price={self.price})")

# class AgenticSystem:
#     def __init__(self):
#         self.agents: Dict[str, SystemAgent] = {}
#         self.inventory: Dict[str, InventoryItem] = {}
#         self.audit_log: List[str] = []

#     # Agent Management
#     def add_agent(self, name: str, role: str, permissions: List[str]) -> SystemAgent:
#         agent = SystemAgent(name, role, permissions)
#         self.agents[agent.id] = agent
#         self._log(f"SystemAgent added: {agent.id}")
#         return agent

#     def delete_agent(self, agent_id: str) -> None:
#         if agent_id not in self.agents:
#             raise ValueError(f"SystemAgent ID {agent_id} not found")
#         agent = self.agents[agent_id]
#         agent.is_active = False
#         self._log(f"SystemAgent deactivated: {agent_id}")

#     def update_agent(self, agent_id: str, **kwargs) -> SystemAgent:
#         agent = self.agents.get(agent_id)
#         if not agent:
#             raise ValueError(f"SystemAgent ID {agent_id} not found")
        
#         for key, value in kwargs.items():
#             if hasattr(agent, key):
#                 setattr(agent, key, value)
#             else:
#                 raise AttributeError(f"Invalid attribute: {key}")
        
#         self._log(f"SystemAgent updated: {agent_id}")
#         return agent

#     def get_agent(self, agent_id: str) -> Optional[SystemAgent]:
#         return self.agents.get(agent_id)

#     def list_agents(self, active_only: bool = True) -> List[SystemAgent]:
#         return [agent for agent in self.agents.values() 
#                 if not active_only or agent.is_active]

#     # Inventory Management
#     def add_item(self, name: str, category: str, quantity: int, price: float) -> InventoryItem:
#         item = InventoryItem(name, category, quantity, price)
#         self.inventory[item.id] = item
#         self._log(f"Inventory item added: {item.id}")
#         return item

#     def delete_item(self, item_id: str) -> None:
#         if item_id not in self.inventory:
#             raise ValueError(f"Item ID {item_id} not found")
#         del self.inventory[item_id]
#         self._log(f"Inventory item deleted: {item_id}")

#     def update_item(self, item_id: str, **kwargs) -> InventoryItem:
#         item = self.inventory.get(item_id)
#         if not item:
#             raise ValueError(f"Item ID {item_id} not found")
        
#         for key, value in kwargs.items():
#             if hasattr(item, key):
#                 setattr(item, key, value)
#             else:
#                 raise AttributeError(f"Invalid attribute: {key}")
        
#         self._log(f"Inventory item updated: {item_id}")
#         return item

#     def get_item(self, item_id: str) -> Optional[InventoryItem]:
#         return self.inventory.get(item_id)

#     def list_items(self, category: Optional[str] = None) -> List[InventoryItem]:
#         return [item for item in self.inventory.values() 
#                 if not category or item.category == category]

#     def search_items(self, name_query: str) -> List[InventoryItem]:
#         return [item for item in self.inventory.values() 
#                 if name_query.lower() in item.name.lower()]

#     # Audit and Utility
#     def _log(self, message: str):
#         self.audit_log.append(message)

#     def get_audit_log(self) -> List[str]:
#         return self.audit_log

#     def agent_has_permission(self, agent_id: str, permission: str) -> bool:
#         agent = self.get_agent(agent_id)
#         return agent and agent.is_active and permission in agent.permissions

# # Initialize the inventory management system
# inventory_system = AgenticSystem()
# admin_agent = inventory_system.add_agent(
#     "Admin", 
#     "Administrator", 
#     ["manage_inventory", "manage_agents"]
# )

# # Create AI tools that connect to the inventory system
# @function_tool(name="add_inventory_item")
# async def add_inventory_item(name: str, category: str, quantity: int, price: float) -> str:
#     """Adds a new item to the inventory"""
#     item = inventory_system.add_item(name, category, quantity, price)
#     return f"Added item: {item.name} (ID: {item.id})"

# @function_tool(name="update_inventory_item")
# async def update_inventory_item(item_id: str, field: str, value: str) -> str:
#     """Updates an existing inventory item"""
#     try:
#         # Convert value to appropriate type
#         if field in ["quantity"]:
#             value = int(value)
#         elif field in ["price"]:
#             value = float(value)
            
#         inventory_system.update_item(item_id, **{field: value})
#         return f"Updated item {item_id}: {field} = {value}"
#     except Exception as e:
#         return f"Error: {str(e)}"

# @function_tool(name="list_inventory_items")
# async def list_inventory_items(category: Optional[str] = None) -> str:
#     """Lists all inventory items, optionally filtered by category"""
#     items = inventory_system.list_items(category)
#     if not items:
#         return "No items found"
    
#     result = ["Inventory Items:"]
#     for item in items:
#         result.append(f"- {item.name} ({item.category}): {item.quantity} in stock, ${item.price}")
#     return "\n".join(result)

# @function_tool(name="add_system_agent")
# async def add_system_agent(name: str, role: str) -> str:
#     """Adds a new system agent with default permissions"""
#     agent = inventory_system.add_agent(name, role, ["basic_access"])
#     return f"Added agent: {agent.name} (ID: {agent.id}, Role: {agent.role})"

# @function_tool(name="list_system_agents")
# async def list_system_agents() -> str:
#     """Lists all active system agents"""
#     agents = inventory_system.list_agents()
#     if not agents:
#         return "No active agents found"
    
#     result = ["Active System Agents:"]
#     for agent in agents:
#         result.append(f"- {agent.name} ({agent.role}, ID: {agent.id})")
#     return "\n".join(result)

# # Initialize Gemini client
# gemini_client = AsyncOpenAI(
#     base_url=BASE_URL,
#     api_key=GEMINI_API_KEY
# )

# gemini_model = OpenAIChatCompletionsModel(
#     model=GEMINI_MODEL,
#     client=gemini_client,
#     temperature=0.5
# )

# # Create AI agent with tools
# inventory_agent = AISDKAgent(
#     model=gemini_model,
#     tools=[
#         add_inventory_item,
#         update_inventory_item,
#         list_inventory_items,
#         add_system_agent,
#         list_system_agents
#     ],
#     system_prompt=(
#         "You are an AI inventory management assistant. "
#         "Use your tools to manage inventory and agents. "
#         "When asked to update items, always confirm the item ID first. "
#         "Be precise with numerical values. Report errors to users clearly."
#     )
# )

# # Create agent runner
# runner = Runner(inventory_agent)

# # Example interaction
# async def main():
#     # Add some initial data
#     inventory_system.add_item("Laptop", "Electronics", 50, 999.99)
#     inventory_system.add_item("Office Chair", "Furniture", 15, 199.50)
    
#     # Run queries
#     queries = [
#         "List all electronics in stock",
#         "Add 5 new standing desks to furniture category, price 299.99 each",
#         "Update the price of laptops to 899.99",
#         "Create a new agent named 'Procurement Bot' with role 'Purchasing'",
#         "List all active agents"
#     ]
    
#     for query in queries:
#         print(f"\n[USER]: {query}")
#         response = await runner.run(query)
#         print(f"[ASSISTANT]: {response}")
        
#         # Show current state
#         if "list" in query.lower():
#             print("\nCurrent State:")
#             print(await list_inventory_items())
#             print(await list_system_agents())

# if __name__ == "__main__":
#     asyncio.run(main())