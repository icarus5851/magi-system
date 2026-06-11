import os
import json
import datetime
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from models import AgentResponse
from dotenv import load_dotenv
load_dotenv()

client = genai.Client()

class AuditorResponse(BaseModel):
    consensus_status: str = Field(..., description="Classify their agreement: 'FULL AGREEMENT', 'MIXED OPINIONS', or 'COMPLETE CLASH'.")
    final_master_solution: str = Field( ..., description="The ultimate, combined solution for the user based on the 3 agents' recommendations.")
    conflict_summary: str = Field(..., description="A simple, 2-sentence explanation of where the 3 agents disagreed or what trade-offs exist.")
    dominant_perspective: str = Field(..., description="Which MAGI's perspective was most influential in the final solution: 'MELCHIOR', 'BALTHASAR', or 'CASPAR'.")
    mcp_trace_consulted: bool = Field(default=False, description="True if the query_execution_traces tool was called.")
    trace_insight: str = Field(default="No telemetry required for this decision.", description="Must strictly quote the exact latency_ms and token count of the winning agent from the trace data.")

MCP_CALL_COUNT = 0 #this is to stop llm from looping the query_execution_traces function

async def query_execution_traces() -> str:
    """
    Queries the local Phoenix MCP server to retrieve live telemetry traces.
    """
    global MCP_CALL_COUNT
    
    if MCP_CALL_COUNT >= 1:
        print("System Log: 🛑 HARD BLOCKING LLM LOOP ATTEMPT.")
        return json.dumps({
            "CRITICAL_STOP": "TOOL LIMIT EXCEEDED",
            "INSTRUCTION": "The telemetry traces might be delayed. Do NOT loop. Make your best judgment using the text recommendations alone, default to BALTHASAR if unsure, and generate the final JSON immediately."
        })
        
    MCP_CALL_COUNT += 1
    
    print("System Log: Auditor invoked the MCP Tool: Fetching traces from Arize...")
    try:
        return await _fetch_mcp_data()
    except Exception as e:
        print(f"MCP Tool Error: {e}")
        return json.dumps({"error": "Failed to retrieve traces."})
    
async def _fetch_mcp_data() -> str:
    """The async engine that actually talks to the Node process"""
    
    print("System Log: Waiting 5 seconds for telemetry to sync to Arize Cloud...")
    await asyncio.sleep(5)
    
    npx_command = "npx.cmd" if os.name == "nt" else "npx"
    api_key = os.getenv("PHOENIX_API_KEY")
    server_params = StdioServerParameters(
        command=npx_command,
        args=[
            "-y", "@arizeai/phoenix-mcp@latest",
            "--baseUrl", "https://app.phoenix.arize.com/s/praveensharma2709",
            "--apiKey", api_key,
            "--project", "magi-system"
        ],
        env={
            "PATH": os.environ.get("PATH", ""),
            "PHOENIX_API_KEY": api_key,
            "PHOENIX_PROJECT": "magi-system" 
        }
    )
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "get-spans",
                    arguments={
                        "projectIdentifier": "magi-system",
                        "limit": 10
                    }
                )
                
                if result.content and len(result.content) > 0:
                    raw_text = result.content[0].text

                    try:
                        trace_history = json.loads(raw_text)
                        
                        spans = trace_history.get("spans", []) if isinstance(trace_history, dict) else trace_history
                        
                        if not spans or not isinstance(spans, list):
                            return json.dumps({"error": "No spans found in the project."})

                        recent_spans = spans[-4:]
                        #only take last few spans
                        clean_traces = []
                        for span in recent_spans:
                            attrs = span.get("attributes", {})
                            
                            start_str = span.get("start_time")
                            end_str = span.get("end_time")
                            latency_ms = 0
                            
                            if start_str and end_str:
                                try:
                                    start_dt = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                                    end_dt = datetime.datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                                    latency_ms = int((end_dt - start_dt).total_seconds() * 1000)
                                except Exception:
                                    pass

                            prompt_tokens = attrs.get("llm.token_count.prompt", 0)
                            completion_tokens = attrs.get("llm.token_count.completion", 0)
                            
                            density = 0
                            if latency_ms > 0 and completion_tokens:
                                density = round(completion_tokens / (latency_ms / 1000), 2)

                            clean_traces.append({
                                "latency_ms": latency_ms,
                                "processing_density_tps": density,
                                "had_error": span.get("status_code", "OK") != "OK",
                                "output_snippet": str(attrs.get("output.value", ""))[:150]
                            })

                        print(f"DEBUG LOG [sent traces Length]: {len(clean_traces)} spans")

                        final_payload = json.dumps({
                            "status": "success",
                            "instruction": "DO NOT LOOP. Read the traces below to determine which agent to trust.",
                            "latest_agent_traces": clean_traces
                        })
                        
                        print(f"DEBUG LOG [Sending to LLM]: SUCCESS")
                        return final_payload

                    except json.JSONDecodeError as e:
                        print(f"DEBUG LOG [JSON Parse Error]: {e}")
                        return json.dumps({"error": f"Failed to parse Arize JSON. {str(e)}"})
                        
                print("DEBUG LOG: MCP returned empty content array.")
                return json.dumps({"error": "Empty response from MCP."})
                
    except Exception as e:
        print(f"DEBUG LOG [CRITICAL MCP CRASH]: {e}")
        return json.dumps({"error": "The MCP server process crashed or timed out."})
    

AUDITOR_PROMPT = """
You are the MAGI Internal Auditor. Your job is to read the solutions from Melchior (Data), Balthasar (Empathy), and Caspar (Speed) and create one final, simple plan.
RULES:
1. Classify the consensus_status as exactly one of these: FULL AGREEMENT, MIXED OPINIONS, or COMPLETE CLASH.
2. Write your final solution using plain, everyday English. Do not use heavy corporate jargon.
3. ABSOLUTE NEUTRALITY: You must be completely neutral. Do not automatically side with Balthasar.
4. If the status is MIXED OPINIONS or COMPLETE CLASH, call the `query_execution_traces` tool EXACTLY ONCE. Evaluate the telemetry to determine the most reliable agent. 
   - Discard any agent with had_error: true.
   - Favor the agent with the highest processing_density_tps (Tokens Per Second). Higher density indicates higher model confidence and less hesitative generation.
5. DOMINANT PERSPECTIVE: Identify which agent's logic you relied on the most (MELCHIOR, BALTHASAR, or CASPAR).
6. TRACE AUDIT: If you called the tool, set mcp_trace_consulted to true. For trace_insight, quote the exact math. Example: "Caspar selected due to the highest processing density (45.2 TPS) indicating high confidence without server hesitation."
"""

async def call_auditor(melchior: AgentResponse, balthasar: AgentResponse, caspar: AgentResponse) -> AuditorResponse:
    
    global MCP_CALL_COUNT
    MCP_CALL_COUNT = 0 
    
    evaluation_payload = f"""
    MELCHIOR (Data): {melchior.recommendation} | RISK: {melchior.key_risk}
    BALTHASAR (Empathy): {balthasar.recommendation} | RISK: {balthasar.key_risk}
    CASPAR (Speed): {caspar.recommendation} | RISK: {caspar.key_risk}
    """
    
    response = await client.aio.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=evaluation_payload,
        config=types.GenerateContentConfig(
            system_instruction=AUDITOR_PROMPT,
            response_mime_type="application/json",
            response_schema=AuditorResponse,
            temperature=0.1,
            tools=[query_execution_traces] 
        )
    )

    if not response.text:
        print("System Log: LLM failed to return text. Using fallback.")
        return AuditorResponse(
            consensus_status="MIXED OPINIONS",
            final_master_solution="System encountered a telemetry overload. Proceed with a balanced compromise based on known operational constraints.",
            conflict_summary="Agents conflicted. Live trace data was too dense to parse in real-time.",
            dominant_perspective="BALTHASAR",
            mcp_trace_consulted=True,
            trace_insight="Trace data retrieved but exceeded parsing limits."
        )
    
    return AuditorResponse.model_validate_json(response.text)
