
from dotenv import load_dotenv


load_dotenv()

from agno.agent import Agent
from agno.models.groq import Groq  #using Groq cloud to call LLM
from agno.tools.duckduckgo import DuckDuckGoTools # duck duck go to search the internet
from agno.team import Team



# Simulated inventory lookup tool in real life we can connect to a database iam giving type hints

class InventoryTool:

    name = "InventoryTool"
    description = "Check stock availability for a given product"

    def run(self, product_name: str) -> str:   #run is the method agno expects to call when agents decides
                                                #to use the tool it call tool.run(arg)
        inventory = {
            "iPhone 17": "In stock (Ships in 5 days),5 quantity of iphone 17  left ",
            "AirPods Pro": "Out of stock (Available in 2 weeks)",
            "MacBook Air M3": "Low stock (Only 3 left)",
        }
        return inventory.get(product_name, "Sorry, the product is not found in inventory")

# Agent 1: Handles customer FAQs and policy questions that will be asked  routed to dummy company
faq_agent = Agent(
    name="faq_agent",
    role="Answer customer questions using web search",
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[DuckDuckGoTools()],
    instructions="Answer e-commerce related queries using web search. Use Amazon.com if someone is asking about electronics. Include source if possible.",
    markdown=True,
    )

# Agent 2: Checks product stock availability from the inventory class created above
inventory_agent = Agent(
    name="Inventory Agent",
    role="Check inventory for a given product",
    model=Groq(id="openai/gpt-oss-120b"),
    tools=[InventoryTool()],
    instructions="Only respond with inventory status of the product",
    markdown=True,
    )


# Multi-agent team coordination ,I can add n number of agents to co  within each other,In Agno there are other mode like Route and collaboration ,
# Route is like sending it to departments specific
#but Agno new version deprecated those
support_team = Team(

    members=[faq_agent,inventory_agent],
    model=Groq(id="openai/gpt-oss-120b"),

    instructions=["Be polite Include product availability and any relevant polices,"],

    markdown=True,)


# Sample query
support_team.print_response(
    "Is the iPhone 17 in stock? How many quantity ? ",
    stream=True
)