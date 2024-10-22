from fastapi import FastAPI
from pydantic import BaseModel
from rule_engine import create_rule, combine_rules, evaluate_rule
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; replace with your frontend's URL if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (e.g., GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

class RuleRequest(BaseModel):
    rule_string: str

class DataRequest(BaseModel):
    data: dict

rules = []

@app.post("/create_rule/")
def create_rule_endpoint(request: RuleRequest):
    new_rule = create_rule(request.rule_string)
    rules.append(new_rule)
    return {"message": "Rule created successfully"}

@app.post("/combine_rules/")
def combine_rules_endpoint():
    combined = combine_rules(rules, combine_op="OR")
    return {"message": "Rules combined successfully"}

@app.post("/evaluate_rule/")
def evaluate_rule_endpoint(request: DataRequest):
    if not rules:
        return {"message": "No rules defined"}

    result = evaluate_rule(rules[-1], request.data)
    return {"eligibility": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

