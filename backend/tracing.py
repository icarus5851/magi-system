import os
import atexit
from dotenv import load_dotenv
from phoenix.otel import register
import urllib.request

def init_tracer():
    load_dotenv()
    
    if not os.getenv("PHOENIX_API_KEY"):
        raise ValueError("CRITICAL: PHOENIX_API_KEY is missing from .env")

    tracer_provider = register(
        project_name="magi-system",
        auto_instrument=True,
        batch = True 
    )

    atexit.register(tracer_provider.shutdown)
    
    print("System Log: Arize Phoenix Telemetry Online (Official Config).")
    return tracer_provider


try:
    urllib.request.urlopen("https://app.phoenix.arize.com/s/praveensharma2709", timeout=5)
    print("NETWORK CHECK: Phoenix reachable")
except Exception as e:
    print(f"NETWORK CHECK FAILED: {e}")
