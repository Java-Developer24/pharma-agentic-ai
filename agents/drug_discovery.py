
# import os
# from pydantic_ai import Agent
# from schemas import AgentResponse, AgentStep
# from utils.visuals import generate_dummy_chart


# os.environ["GEMINI_API_KEY"] = "AIzaSyBQ3KBPoDia7wJacppgwEHn027TwKYZD8k"

# drug_discovery_ai = Agent(model="gemini-2.5-flash")

# @drug_discovery_ai.run
# async def drug_discovery_agent(query: str) -> AgentResponse:
#     query_lower = query.lower()

#     if not any(word in query_lower for word in ["molecule", "compound", "structure", "drug"]):
#         return AgentResponse(
#             agent="Drug Discovery Agent",
#             query=query,
#             steps_taken=[AgentStep(description="Could not identify molecule in query")],
#             response=None,
#             visual=None,
#             follow_up="Which molecule or compound would you like me to analyze for discovery?"
#         )

#     chart = generate_dummy_chart(
#         "Molecule Binding Affinity",
#         ["Protein A", "Protein B", "Protein C"],
#         [0.8, 0.5, 0.3]
#     )

#     return AgentResponse(
#         agent="Drug Discovery Agent",
#         query=query,
#         steps_taken=[
#             AgentStep(description="Parsed molecular structure"),
#             AgentStep(description="Identified target proteins"),
#             AgentStep(description="Predicted drug-target interactions"),
#             AgentStep(description="Generated binding affinity chart")
#         ],
#         response="The compound shows potential binding affinity with target protein XYZ.",
#         visual=chart,
#         follow_up=None
#     )
import os
from pydantic_ai import Agent
from schemas import AgentResponse, AgentStep
from utils.visuals import generate_dummy_chart

os.environ["GEMINI_API_KEY"] = "AIzaSyBQ3KBPoDia7wJacppgwEHn027TwKYZD8k"

drug_discovery_ai = Agent(model="gemini-2.5-flash")

@drug_discovery_ai.run
async def drug_discovery_agent(query: str) -> AgentResponse:
    query_lower = query.lower()

    # If no molecule/compound detected, generate general chart
    if not any(word in query_lower for word in ["molecule", "compound", "structure", "drug"]):
        chart = generate_dummy_chart(
            "General Drug Info Overview",
            ["Prescription", "OTC", "Recreational", "Supplements"],
            [40, 30, 20, 10]
        )
        return AgentResponse(
            agent="Drug Discovery Agent",
            query=query,
            steps=[AgentStep(description="Generated general drug chart")],
            response="Here's a general overview of drug categories.",
            visuals=[chart],
            follow_up="Specify a compound or molecule for detailed analysis."
        )

    # Original detailed molecule logic
    chart = generate_dummy_chart(
        "Molecule Binding Affinity",
        ["Protein A", "Protein B", "Protein C"],
        [0.8, 0.5, 0.3]
    )

    return AgentResponse(
        agent="Drug Discovery Agent",
        query=query,
        steps=[
            AgentStep(description="Parsed molecular structure"),
            AgentStep(description="Identified target proteins"),
            AgentStep(description="Predicted drug-target interactions"),
            AgentStep(description="Generated binding affinity chart")
        ],
        response="The compound shows potential binding affinity with target protein XYZ.",
        visuals=[chart],
        follow_up=None
    )
