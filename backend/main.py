from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
from tracing import init_tracer
from models import MagiRequest, AgentResponse
from orchestrator import run_magi_orchestrator
from agents.auditor import call_auditor, AuditorResponse

class MasterMagiResponse(BaseModel):
    consensus_status: str
    melchior: AgentResponse
    balthasar: AgentResponse
    caspar: AgentResponse
    auditor: AuditorResponse

init_tracer()

app = FastAPI(title="NERV MAGI System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"status": "MAGI System Online", "version": "1.0"}

@app.post("/api/evaluate", response_model=MasterMagiResponse)
async def evaluate_strategic_decision(request: MagiRequest):
    
    print(f"System Log: Initiating MAGI evaluation for query...")
    orchestrator_data = await run_magi_orchestrator(request)
    
    print(f"System Log: MAGI computation complete. Handing to Auditor...")
    auditor_data = await call_auditor(
        melchior=orchestrator_data.melchior,
        balthasar=orchestrator_data.balthasar,
        caspar=orchestrator_data.caspar
    )
    
    print(f"System Log: Evaluation complete. Sending payload to UI.")
    return MasterMagiResponse(
        consensus_status=auditor_data.consensus_status,
        melchior=orchestrator_data.melchior,
        balthasar=orchestrator_data.balthasar,
        caspar=orchestrator_data.caspar,
        auditor=auditor_data,
    )