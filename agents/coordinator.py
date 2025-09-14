from .drug_discovery import drug_discovery_ai
from .clinical_trial import clinical_trial_ai
from .drug_interaction import drug_interaction_ai
from schemas import AgentResponse, AgentStep
from utils.visuals import generate_dummy_chart

async def coordinator_agent(query: str) -> AgentResponse:
    """
    Routes query to the correct specialized agent.
    If no specialized agent matches, returns a general overview with a visual.
    """
    query_lower = query.lower()

    if any(word in query_lower for word in ["discovery", "molecule", "compound", "drug"]):
        return await drug_discovery_ai.run(query)
    elif any(word in query_lower for word in ["trial", "cohort", "design", "patients"]):
        return await clinical_trial_ai.run(query)
    elif any(word in query_lower for word in ["interaction", "dosage", "metabolism"]):
        return await drug_interaction_ai.run(query)
    else:
        # Fallback for unrecognized/general queries
        chart = generate_dummy_chart(
            "General Drug Info Overview",
            ["Prescription", "OTC", "Recreational", "Supplements"],
            [40, 30, 20, 10]
        )
        return AgentResponse(
            agent="Coordinator",
            query=query,
            steps=[AgentStep(description="Provided general drug information")],
            response=(
                "The term 'drug' is very broad. "
                "Here is a general overview of drug categories."
            ),
            visuals=[chart],
            follow_up="Please specify the drug or topic you want detailed information on."
        )
