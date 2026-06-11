import requests
import time
import json

API_URL = "http://127.0.0.1:8000/api/evaluate"

TEST_CASES = [
    {
        "name": "The Ethical Dilemma (Balthasar vs. Caspar)",
        "payload": {
            "context": "We discovered a minor, harmless bug in our code that accidentally charged 1,000 customers an extra $1 last year. No one has noticed.",
            "query": "Should we silently refund the money and fix the bug, or publicly announce the error and risk a massive PR disaster?"
        }
    },
    {
        "name": "The Technical Debt (Melchior vs. Caspar)",
        "payload": {
            "context": "Our core API is written in outdated code that slows down development. Rewriting it will take 3 months of zero new features. A major competitor is launching a new product next month.",
            "query": "Do we freeze feature development to rewrite the API, or keep patching the old code to race the competitor?"
        }
    },
    {
        "name": "The Resource War (COMPLETE CLASH)",
        "payload": {
            "context": "We had an unexpected $5 Million surplus this quarter. The engineering team wants it for servers, HR wants it for employee bonuses to stop turnover, and the Board wants it paid out as dividends.",
            "query": "How do we allocate the $5 Million surplus?"
        }
    },
    {
        "name": "The Pivot Decision (Data vs Empathy)",
        "payload": {
            "context": "Our SaaS product has 500 loyal paying customers, but growth has been flat for 8 months. A new enterprise market opportunity has appeared that requires completely rebuilding the product and abandoning the current user base.",
            "query": "Do we abandon our current customers to pivot to enterprise, or stay the course with the existing product?"
        }
    },
    {
        "name": "The PR Crisis (Speed vs Caution)",
        "payload": {
            "context": "A viral tweet with 200,000 impressions falsely claims our product caused someone to lose their job. It is completely untrue but spreading fast.",
            "query": "Do we respond immediately and publicly, issue a quiet correction, or say nothing and let it die?"
        }
    }
]

def run_tests():
    print("🚀 Initiating Automated MAGI System Stress Test...")
    print("==================================================")
    
    for i, test in enumerate(TEST_CASES):
        print(f"\n[{i+1}/5] Executing: {test['name']}")
        print(f"Query: {test['payload']['query']}")
        
        try:
            response = requests.post(API_URL, json=test['payload'])
            
            if response.status_code == 200:
                data = response.json()
                auditor_data = data.get("auditor", {})
                
                print("\n✅ SUCCESS")
                print(f"STATUS: {data.get('consensus_status')}")
                print(f"DOMINANT MIND: {auditor_data.get('dominant_perspective')}")
                print(f"TRACE INSIGHT: {auditor_data.get('trace_insight')}")
                print(f"SOLUTION: {auditor_data.get('final_master_solution')}")
            else:
                print(f"\n❌ FAILED with Status Code: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"\n🚨 CRITICAL ERROR: {e}")
            
        if i < len(TEST_CASES) - 1:
            print("\n⏳ Waiting 25 seconds for Gemini API rate limits to reset...")
            time.sleep(25)
            
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    run_tests()