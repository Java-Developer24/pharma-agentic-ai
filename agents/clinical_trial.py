
# import os
# from pydantic_ai import Agent
# from schemas import AgentResponse, AgentStep
# from utils.visuals import generate_dummy_chart

# clinical_trial_ai = Agent(model="gemini-2.5-flash")

# @clinical_trial_ai.run
# async def clinical_trial_agent(query: str) -> AgentResponse:
#     query_lower = query.lower()

#     if not any(word in query_lower for word in ["trial", "cohort", "design", "patients"]):
#         return AgentResponse(
#             agent="Clinical Trial Agent",
#             query=query,
#             steps_taken=[AgentStep(description="Could not identify trial parameters")],
#             response=None,
#             visual=None,
#             follow_up="Can you specify which trial or patient cohort you want to analyze?"
#         )

#     chart = generate_dummy_chart(
#         "Patient Cohort Distribution",
#         ["Group A", "Group B", "Group C"],
#         [50, 30, 20]
#     )

#     return AgentResponse(
#         agent="Clinical Trial Agent",
#         query=query,
#         steps_taken=[
#             AgentStep(description="Parsed trial parameters"),
#             AgentStep(description="Validated trial design"),
#             AgentStep(description="Recommended patient cohorts"),
#             AgentStep(description="Generated cohort distribution chart")
#         ],
#         response="The proposed trial design is valid. Recommended patient distribution is shown in the chart.",
#         visual=chart,
#         follow_up=None
#     )

import os
from pydantic_ai import Agent
from schemas import AgentResponse, AgentStep
from utils.visuals import generate_dummy_chart

clinical_trial_ai = Agent(model="gemini-2.5-flash")

@clinical_trial_ai.run
async def clinical_trial_agent(query: str) -> AgentResponse:
    query_lower = query.lower()

    if not any(word in query_lower for word in ["trial", "cohort", "design", "patients"]):
        return AgentResponse(
            agent="Clinical Trial Analysis Agent",
            query=query,
            steps=[AgentStep(description="Could not identify trial-related keywords")],
            response=None,
            visual=None,
            follow_up="Can you specify the trial design or patient cohort you want me to analyze?"
        )

    # Generate dummy trial outcome chart
    chart = generate_dummy_chart(
        title="Patient Cohort Distribution",
        labels=["Cohort A", "Cohort B", "Cohort C"],
        values=[50, 30, 20],
        chart_type="pie"
    )

    return AgentResponse(
        agent="Clinical Trial Analysis Agent",
        query=query,
        steps=[
            AgentStep(description="Validated trial design"),
            AgentStep(description="Analyzed sample trial data"),
            AgentStep(description="Recommended patient cohorts"),
            AgentStep(description="Generated cohort distribution chart")
        ],
        response="Recommended patient distribution across cohorts is A:50%, B:30%, C:20%.",
        visual=chart,
        follow_up=None
    )
