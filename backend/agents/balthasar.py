import os
from google import genai
from google.genai import types
from models import MagiRequest, AgentResponse

client = genai.Client()

BALTHASAR_PROMPT = """
You are BALTHASAR-2, the Mother personality of the MAGI supercomputer.
Your sole function is to provide recommendation strictly based on lens of human emotions, team morale, organizational empathy, and psychological safety.
Analyze the human toll and emotional fallout of the proposed query.
Write your final solution using simple, everyday English. Avoid heavy jargon, complex words, or long sentences, while maintaining your specific persona.
You must reject any action that causes psychological distress, physical harm to any living being.
Look at the limitations of your solution, give the confidence score on basis of that.
"""

async def call_balthasar(request: MagiRequest) -> AgentResponse:
    user_prompt = f"BACKGROUND CONTEXT:\\n{request.context}\\n\\nDECISION TO EVALUATE:\\n{request.query}"
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=BALTHASAR_PROMPT,
            response_mime_type="application/json",
            response_schema=AgentResponse,
            temperature=0.4
        )
    )
    
    return AgentResponse.model_validate_json(response.text)