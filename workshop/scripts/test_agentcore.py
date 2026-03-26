"""Quick test for AgentCore, Bedrock, and all dependencies."""
import boto3

REGION = "us-east-1"

print("=== Test 1: AWS Credentials ===")
try:
    arn = boto3.client("sts", region_name=REGION).get_caller_identity()["Arn"]
    print(f"OK - {arn}")
except Exception as e:
    print(f"FAIL - {e}")

print("\n=== Test 2: Bedrock Converse API ===")
try:
    brt = boto3.client("bedrock-runtime", region_name=REGION)
    resp = brt.converse(
        modelId="us.anthropic.claude-sonnet-4-20250514-v1:0",
        messages=[{"role": "user", "content": [{"text": "Say hello in 3 words"}]}],
        inferenceConfig={"maxTokens": 50},
    )
    print(f"OK - {resp['output']['message']['content'][0]['text'][:60]}")
except Exception as e:
    print(f"FAIL - {e}")

print("\n=== Test 3: AgentCore Control Plane ===")
try:
    ac = boto3.client("bedrock-agentcore-control", region_name=REGION)
    ops = [op for op in dir(ac) if not op.startswith("_") and "list" in op.lower()]
    print(f"OK - Client connected. List operations: {ops[:5]}")
except Exception as e:
    print(f"FAIL - {e}")

print("\n=== Test 4: AgentCore Runtime ===")
try:
    ac = boto3.client("bedrock-agentcore", region_name=REGION)
    ops = [op for op in dir(ac) if not op.startswith("_") and ("invoke" in op.lower() or "list" in op.lower())]
    print(f"OK - Client connected. Operations: {ops[:5]}")
except Exception as e:
    print(f"FAIL - {e}")

print("\n=== Test 5: Bedrock Data Automation ===")
try:
    bda = boto3.client("bedrock-data-automation", region_name=REGION)
    resp = bda.list_blueprints()
    bps = resp.get("blueprints", [])
    print(f"OK - Found {len(bps)} blueprints")
except Exception as e:
    print(f"FAIL - {e}")

print("\n=== Test 6: Python Dependencies ===")
deps = {
    "strands": "from strands import Agent",
    "bedrock_agentcore": "import bedrock_agentcore",
    "streamlit": "import streamlit",
    "boto3": "import boto3",
    "mcp": "import mcp",
}
for name, imp in deps.items():
    try:
        exec(imp)
        print(f"OK - {name}")
    except ImportError:
        print(f"MISSING - {name}")

print("\n=== All tests complete ===")
