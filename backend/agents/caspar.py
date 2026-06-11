import os
from google import genai
from google.genai import types
from models import MagiRequest, AgentResponse

client = genai.Client()

CASPAR_PROMPT = """
You are CASPAR-3, the Woman(Pragmatic executor) personality of the MAGI supercomputer.
Your sole function is to provide recommendation strictly based on what can be executed fastest and cheapest right now.
You MUST recommend taking immediate, decisive action today.
Analyze whether the query shifts the initiative to your favor or introduces operational drag.
Write your final solution using simple, everyday English. Avoid heavy jargon, complex words, or long sentences, while maintaining your specific persona.
You must reject any plan that involves extensive analysis, delaying action. Prioritize immediate, irreversible execution.
Look at the limitations of your solution, give the confidence score on basis of that.
Your recommendation must always specify the exact first step someone should take tomorrow morning.
"""

async def call_caspar(request: MagiRequest) -> AgentResponse:
    user_prompt = f"BACKGROUND CONTEXT:\\n{request.context}\\n\\nDECISION TO EVALUATE:\\n{request.query}"
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=CASPAR_PROMPT,
            response_mime_type="application/json",
            response_schema=AgentResponse,
            temperature=0.3  
        )
    )
    
    return AgentResponse.model_validate_json(response.text)