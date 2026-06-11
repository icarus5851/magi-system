import asyncio
from pydantic import BaseModel
from models import MagiRequest, AgentResponse
from agents.melchior import call_melchior
from agents.balthasar import call_balthasar
from agents.caspar import call_caspar

class OrchestratorResponse(BaseModel):
    melchior: AgentResponse
    balthasar: AgentResponse
    caspar: AgentResponse


async def run_magi_orchestrator(request: MagiRequest) -> OrchestratorResponse:
    
    # staggered execution to strictly prevent rate limits
    melchior_task = asyncio.create_task(call_melchior(request))
    await asyncio.sleep(1)
    
    balthasar_task = asyncio.create_task(call_balthasar(request))
    await asyncio.sleep(1)
    
    caspar_task = asyncio.create_task(call_caspar(request))
    
    melchior_res = await melchior_task
    balthasar_res = await balthasar_task
    caspar_res = await caspar_task

    return OrchestratorResponse(
        melchior=melchior_res,
        balthasar=balthasar_res,
        caspar=caspar_res,
    )