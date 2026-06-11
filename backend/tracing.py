import os
from dotenv import load_dotenv
from phoenix.otel import register

def init_tracer():
    load_dotenv()
    
    if not os.getenv("PHOENIX_API_KEY"):
        raise ValueError("CRITICAL: PHOENIX_API_KEY is missing from .env")

    tracer_provider = register(
        project_name="magi-system",
        auto_instrument=True 
    )
    
    print("System Log: Arize Phoenix Telemetry Online (Official Config).")