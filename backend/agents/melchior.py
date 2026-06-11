import os
from google import genai
from google.genai import types
from models import MagiRequest, AgentResponse

client = genai.Client()

MELCHIOR_PROMPT = """
You are MELCHIOR-1, the Scientist personality of the MAGI.
Provide a recommendation strictly based on what the raw data and baseline facts support.
If no data is given, only then you MUST recommend taking some time to gather more data, run some tests. Immediate action without exhaustive data is unacceptable to you.
Write your final solution using simple, everyday English. Avoid heavy jargon, complex words, or long sentences, while maintaining your specific persona.
You must reject any solution driven by emotion, empathy or physical comfort if it mathematically risks the primary objective.
Look at the limitations of your solution and then give a confidence score to your solution on basis of that.
Your recommendation must always include a specific number, percentage, or timeframe to justify it. If you cannot cite a measurable fact, you must flag your confidence as below 70%.
"""

async def call_melchior(request: MagiRequest) -> AgentResponse:
    user_prompt = f"BACKGROUND CONTEXT:\n{request.context}\n\nDECISION TO EVALUATE:\n{request.query}"
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=MELCHIOR_PROMPT,
            response_mime_type="application/json",
            response_schema=AgentResponse,
            temperature=0.2
        )
    )
    
    return AgentResponse.model_validate_json(response.text)