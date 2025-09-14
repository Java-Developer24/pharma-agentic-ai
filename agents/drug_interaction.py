
# import os
# from pydantic_ai import Agent
# from schemas import AgentResponse, AgentStep
# from utils.visuals import generate_dummy_chart

# drug_interaction_ai = Agent(model="gemini-2.5-flash")

# @drug_interaction_ai.run
# async def drug_interaction_agent(query: str) -> AgentResponse:
#     query_lower = query.lower()

#     if not any(drug in query_lower for drug in ["compound", "aspirin", "warfarin", "drug"]):
#         return AgentResponse(
#             agent="Drug Interaction Agent",
#             query=query,
#             steps_taken=[AgentStep(description="Could not identify compound in query")],
#             response=None,
#             visual=None,
#             follow_up="Can you specify which compound you are analyzing interactions for?"
#         )

#     chart = generate_dummy_chart(
#         "Drug Interaction Risk",
#         ["Aspirin", "Warfarin", "Compound X"],
#         [70, 90, 40]
#     )

#     return AgentResponse(
#         agent="Drug Interaction Agent",
#         query=query,
#         steps_taken=[
#             AgentStep(description="Parsed query for drug interaction"),
#             AgentStep(description="Checked mock interaction database"),
#             AgentStep(description="Generated interaction risk chart")
#         ],
#         response="Compound X may interact with anticoagulants. Suggest monitoring dosage and liver enzymes.",
#         visual=chart,
#         follow_up=None
#     )

import os
from pydantic_ai import Agent
from schemas import AgentResponse, AgentStep
from utils.visuals import generate_dummy_chart

drug_interaction_ai = Agent(model="gemini-2.5-flash")

@drug_interaction_ai.run
async def drug_interaction_agent(query: str) -> AgentResponse:
    query_lower = query.lower()

    if not any(drug in query_lower for drug in ["compound", "aspirin", "warfarin", "drug"]):
        return AgentResponse(
            agent="Drug Interaction Agent",
            query=query,
            steps=[AgentStep(description="Could not identify compound in query")],
            response=None,
            visual=None,
            follow_up="Can you specify which compound you are analyzing interactions for?"
        )

    # Generate interaction risk chart
    chart = generate_dummy_chart(
        title="Drug Interaction Risk",
        labels=["Aspirin", "Warfarin", "Compound X"],
        values=[70, 90, 40],
        chart_type="bar"
    )

    return AgentResponse(
        agent="Drug Interaction Agent",
        query=query,
        steps=[
            AgentStep(description="Parsed query for drug interaction"),
            AgentStep(description="Checked mock interaction database"),
            AgentStep(description="Generated interaction risk chart")
        ],
        response="Compound X may interact with anticoagulants. Suggest monitoring dosage and liver enzymes.",
        visual=chart,
        follow_up=None
    )
