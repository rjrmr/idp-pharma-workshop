# 🧬 IDP Agent – Pharma Manufacturing Workshop

Intelligent Document Processing (IDP) workshop for extracting structured data from handwritten pharmaceutical documents using AI agents.

Built on the [amazon-bedrock-agents-healthcare-lifesciences](https://github.com/aws-samples/amazon-bedrock-agents-healthcare-lifesciences) reference architecture.

## What This Is

A guided workshop package for pharma, lifesciences, and manufacturing professionals to learn how AI agents can digitize handwritten Batch Manufacturing Records (BMR). Participants upload scanned documents and use natural language to extract structured data — product names, batch numbers, ingredients, equipment IDs, timestamps — all following ALCOA+ data integrity principles.

## Tech Stack

| Component | Purpose |
|-----------|---------|
| **Strands Agents SDK** | Agent orchestration framework |
| **BDA MCP Server** | Document extraction via Model Context Protocol |
| **Amazon Bedrock** | Foundation models (Claude Sonnet) |
| **AgentCore Runtime** | Managed agent deployment |
| **Streamlit** | Interactive chat UI |

## Quick Start

```bash
# Install dependencies
pip install -r workshop/setup/requirements.txt

# Configure AWS credentials
aws configure  # or set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

# Run the app
streamlit run workshop/app.py
```

Then open http://localhost:8501, upload a BMR PDF from `workshop/test-data/bmr/`, and start asking questions.

## Project Structure

```
workshop/
├── app.py                          # Streamlit chat interface
├── .streamlit/config.toml          # Theme configuration
├── guide/workshop-guide.md         # Step-by-step workshop instructions
├── scenarios/bmr-scenario.md       # BMR use case context
├── test-data/
│   ├── bmr/                        # Sample BMR PDFs (clean, messy, partial)
│   └── test-data-manifest.json     # Test data index
├── prompts/bmr-prompts.md          # Copy-paste ready prompts
├── examples/                       # Worked examples with expected outputs
├── reference/                      # Expected JSON outputs for validation
├── scripts/validate_output.py      # Output comparison tool
└── setup/
    ├── environment-setup.md        # Setup guide
    ├── requirements.txt            # Python dependencies
    ├── mcp-config.json             # MCP server config template
    └── verify-setup.py             # Pre-flight checks
```

## Workshop Exercises

The workshop guide (`workshop/guide/workshop-guide.md`) includes 6 exercises covering:

1. **Environment Setup** — Verify dependencies, credentials, MCP config
2. **Basic BMR Extraction** — Upload clean document, extract all fields
3. **Targeted Extraction** — Extract specific fields (batch number, ingredients)
4. **Handling Messy Documents** — Process documents with corrections and smudges
5. **Partial Documents** — Handle missing/blank fields gracefully
6. **Multi-turn Conversation** — Follow-up questions about the same document

## Sample Prompts

```
Extract all fields from this batch manufacturing record as JSON
```
```
What is the batch number and product name?
```
```
List all ingredients with their weights and lot numbers
```

See `workshop/prompts/bmr-prompts.md` for the full prompt library.

## Validation

Compare agent output against reference data:

```bash
python workshop/scripts/validate_output.py \
  --actual output.json \
  --expected workshop/reference/bmr-sample-01-clean-expected.json
```

## Prerequisites

- Python 3.10+
- AWS account with Bedrock model access (Claude Sonnet)
- AWS credentials configured

## Why This Matters

- **58% of FDA 483 observations** cite data integrity issues in manufacturing records
- **Over 60% of pharma manufacturers** still rely on paper-based batch records
- Manual transcription errors cost the industry **$50B+ annually** in rework and recalls

## License

This project is provided for workshop and educational purposes.
