# IDP Pharma Workshop Guide

## Workshop Overview

**Duration:** ~3 hours 10 minutes (well within the 4-hour limit)

### What You Will Learn

In this workshop, you will use the Intelligent Document Processing (IDP) Agent to extract structured data from handwritten pharmaceutical Batch Manufacturing Records (BMRs). By the end of the workshop, you will be able to:

- Upload handwritten documents and interact with the IDP Agent through a conversational chat interface
- Extract structured JSON data from clean, messy, and partially filled batch records
- Perform targeted extraction of specific fields from handwritten documents
- Validate extracted data against reference values
- Understand how the agent handles real-world document imperfections (illegible handwriting, missing fields, corrections)

### Technology Stack

| Technology | Role |
|------------|------|
| **Streamlit** | Python-based web UI for the interactive chat interface |
| **Amazon Bedrock AgentCore** | Managed runtime for deploying and operating the IDP Agent |
| **Strands Agents SDK** | Agent framework providing orchestration, tool use, and reasoning |
| **BDA MCP Server** | Amazon Bedrock Data Automation server for document extraction via MCP |
| **Model Context Protocol (MCP)** | Open protocol connecting the Strands Agent to the BDA server |
| **Amazon Bedrock** | Foundation model provider powering the agent's reasoning |

### Workshop Structure

| Section | Duration | Description |
|---------|----------|-------------|
| Workshop Overview | ~5 min | Introduction and orientation |
| Architecture Overview | ~10 min | System architecture and data flow |
| Prerequisites | ~15 min | Environment verification and setup |
| Exercise 1: Basic BMR Extraction | ~30 min | Full-field extraction from a clean document |
| Exercise 2: Targeted BMR Extraction | ~20 min | Extract specific fields only |
| Exercise 3: Multi-Turn Document Q&A | ~25 min | Follow-up questions about the same document |
| Exercise 4: Validation | ~20 min | Compare extracted data against reference values |
| Exercise 5: Handling Messy Documents | ~25 min | Process a document with difficult handwriting |
| Exercise 6: Handling Partial Documents | ~25 min | Process a document with missing fields |
| Wrap-Up and Discussion | ~15 min | Key takeaways and Q&A |
| **Total** | **~190 min** | |

---

## Architecture Overview

The IDP Agent processes handwritten documents through a multi-layer architecture. Understanding this flow helps you interpret what happens when you submit a prompt in the chat interface.

### Data Flow

```
Streamlit Chat UI → AgentCore Runtime → Strands Agent → BDA MCP Server → Extract Data → Cache → Return JSON
```

### Component Roles

**Streamlit Chat UI** — The web-based interface where you upload documents and ask questions. It displays the agent's responses in a conversational thread and renders JSON output in a formatted view. The UI maintains session state so you can ask follow-up questions about the same document.

**AgentCore Runtime** — The Amazon Bedrock AgentCore managed runtime that hosts and operates the IDP Agent. It receives requests from the chat UI, invokes the Strands Agent, and returns responses. AgentCore handles scaling, availability, and lifecycle management.

**Strands Agent** — The core agent built with the Strands Agents SDK. It receives your question along with the document reference, reasons about what tools to call, invokes the BDA MCP Server to extract data, and formulates a structured response. The agent uses an Amazon Bedrock foundation model for reasoning and natural language understanding.

**BDA MCP Server** — The Amazon Bedrock Data Automation MCP Server. It receives extraction requests from the Strands Agent via the Model Context Protocol, processes the handwritten document using Bedrock Data Automation, and returns the extracted fields as structured data. This is where the actual OCR and handwriting recognition happens.

### How MCP Connects the Agent to BDA

The Model Context Protocol (MCP) is an open standard that defines how agents communicate with external tools. In this architecture:

1. The Strands Agent discovers available tools by sending a `list_tools` request to the BDA MCP Server
2. When the agent needs to extract data from a document, it sends an `extract_document` request via MCP
3. The BDA MCP Server processes the document and returns the extracted fields as JSON
4. The agent reasons over the extracted data to answer your question

The MCP configuration (`mcp-config.json`) defines the server endpoint, authentication, and environment variables. You configured this during environment setup.

---

## Prerequisites

**Estimated time:** ~15 minutes

Before starting the exercises, verify that your environment is fully configured.

### Step 1: Review Environment Setup

If you haven't completed the environment setup, follow the instructions in:

```
workshop/setup/environment-setup.md
```

This covers installing Kiro Powers, configuring the MCP server, installing Python dependencies, and setting up AWS credentials.

### Step 2: Run the Pre-flight Verification Script

```bash
python workshop/setup/verify-setup.py
```

All checks should report `[PASS]`. If any check fails, follow the remediation instructions in the output. Do not proceed to the exercises until all checks pass.

### Step 3: Launch the Chat Interface

```bash
streamlit run workshop/app.py
```

The Streamlit chat interface opens in your browser. Confirm that:

- The sidebar displays the technology stack (Strands SDK, BDA MCP, AgentCore)
- The file uploader is visible in the sidebar
- No error messages appear on load

You are now ready to begin the exercises.

---

## Exercise 1: Basic BMR Extraction

**Duration:** ~30 minutes
**Goal:** Extract all handwritten fields from a clean Batch Manufacturing Record and receive a complete JSON response.

### Prerequisites

- Environment verified (all pre-flight checks pass)
- Chat interface running (`streamlit run workshop/app.py`)

### Test Data

**File:** `workshop/test-data/bmr/bmr-sample-01-clean.pdf`
**Difficulty:** Clean — neat handwriting, all fields filled, no corrections
**Product:** Amoxicillin 500mg Capsules
**Batch:** BMR-2024-0847

### Instructions

**1. Upload the document**

In the Streamlit sidebar, use the file uploader to select `bmr-sample-01-clean.pdf` from the `workshop/test-data/bmr/` directory. The interface will confirm the document is loaded.

**2. Submit the basic extraction prompt**

Copy and paste the following prompt into the chat input:

```
I've uploaded the batch manufacturing record bmr-sample-01-clean.pdf. Please extract all handwritten fields from this document and return the results as structured JSON, including product name, batch number, ingredient names, weights, lot numbers, equipment IDs, operator initials, and timestamps.
```

**3. Review the response**

The agent should return a complete JSON object with all BMR fields populated:

- `product_name` — the drug product name
- `batch_number` — the unique batch identifier
- `ingredients` — an array of objects, each with `ingredient_name`, `weight_kg`, and `lot_number`
- `equipment_ids` — an array of equipment identifier strings
- `operator_initials` — the operator's initials
- `start_timestamp` and `end_timestamp` — ISO 8601 timestamps

### Expected Outcome

A complete JSON object with all BMR fields populated. No fields should be `null` — this is a clean document with all entries filled in.

Example of the expected JSON structure:

```json
{
  "product_name": "Amoxicillin 500mg Capsules",
  "batch_number": "BMR-2024-0847",
  "ingredients": [
    {
      "ingredient_name": "Amoxicillin Trihydrate",
      "weight_kg": 25.00,
      "lot_number": "LOT-AM-20240115"
    },
    {
      "ingredient_name": "Magnesium Stearate",
      "weight_kg": 0.75,
      "lot_number": "LOT-MG-20240203"
    },
    {
      "ingredient_name": "Microcrystalline Cellulose",
      "weight_kg": 12.50,
      "lot_number": "LOT-MC-20240118"
    }
  ],
  "equipment_ids": ["MIX-401", "GRAN-205", "PRESS-112"],
  "operator_initials": "JKL",
  "start_timestamp": "2024-03-15T06:30:00",
  "end_timestamp": "2024-03-15T14:45:00"
}
```

### Reference

For a complete step-by-step walkthrough with validation, see: `workshop/examples/bmr-basic-example.md`

---

## Exercise 2: Targeted BMR Extraction

**Duration:** ~20 minutes
**Goal:** Extract only specific fields from a document, demonstrating that the agent can focus on a subset of the data.

### Prerequisites

- Exercise 1 completed successfully

### Test Data

**File:** `workshop/test-data/bmr/bmr-sample-01-clean.pdf` (same document as Exercise 1)

### Instructions

**1. Ensure the document is still loaded**

If you are continuing from Exercise 1 in the same session, the document is already loaded. If you started a new session, re-upload `bmr-sample-01-clean.pdf`.

**2. Submit the targeted extraction prompt**

Copy and paste the following prompt into the chat input:

```
From the uploaded batch record bmr-sample-01-clean.pdf, extract only the ingredient names and their corresponding weights in kg. Return the results as a JSON array of objects with 'ingredient_name' and 'weight_kg' fields.
```

**3. Review the response**

The agent should return a focused JSON array containing only the requested fields — ingredient names and weights. No other BMR fields should be included.

### Expected Outcome

A JSON array of objects with only `ingredient_name` and `weight_kg` fields:

```json
[
  {"ingredient_name": "Amoxicillin Trihydrate", "weight_kg": 25.00},
  {"ingredient_name": "Magnesium Stearate", "weight_kg": 0.75},
  {"ingredient_name": "Microcrystalline Cellulose", "weight_kg": 12.50}
]
```

### Discussion Points

- How does the agent's response differ from the full extraction in Exercise 1?
- What are the practical use cases for targeted extraction? (e.g., ingredient reconciliation, weight verification)
- Could you use targeted extraction to build automated compliance checks?

---

## Exercise 3: Multi-Turn Document Q&A

**Duration:** ~25 minutes
**Goal:** Demonstrate multi-turn conversation about the same document, asking follow-up questions without re-uploading.

### Prerequisites

- Exercise 1 completed successfully

### Test Data

**File:** `workshop/test-data/bmr/bmr-sample-01-clean.pdf`

### Instructions

This exercise involves a three-turn conversation. Each turn builds on the previous one, and all questions reference the same uploaded document.

**Turn 1 — Full Extraction**

If starting a new session, upload `bmr-sample-01-clean.pdf` first. Then submit the basic extraction prompt:

```
I've uploaded the batch manufacturing record bmr-sample-01-clean.pdf. Please extract all handwritten fields from this document and return the results as structured JSON, including product name, batch number, ingredient names, weights, lot numbers, equipment IDs, operator initials, and timestamps.
```

The agent returns the complete JSON extraction (same as Exercise 1).

**Turn 2 — Ask about the batch number**

Without re-uploading the document, ask:

```
What is the batch number?
```

The agent should answer from the already-extracted data: **BMR-2024-0847**.

**Turn 3 — Ask for ingredients and weights**

Continue the conversation:

```
List all ingredients and their weights
```

The agent should return the ingredient list, potentially as a table or structured list.

### Expected Outcome

- Turn 1: Complete JSON with all BMR fields
- Turn 2: The batch number `BMR-2024-0847` (plain text answer)
- Turn 3: A list of ingredients with weights (table or structured format)

The key observation is that the agent maintains context across turns — you don't need to re-upload or re-specify the document for follow-up questions.

### Reference

For the complete conversation flow with expected responses, see: `workshop/examples/multi-turn-example.md`

---

## Exercise 4: Validation

**Duration:** ~20 minutes
**Goal:** Extract specific fields and validate them against known expected values, then run the validation script against the reference JSON.

### Prerequisites

- Exercise 1 completed successfully

### Test Data

**File:** `workshop/test-data/bmr/bmr-sample-01-clean.pdf`

### Instructions

**1. Submit the validation prompt**

Ensure `bmr-sample-01-clean.pdf` is loaded, then copy and paste the following prompt:

```
Extract the batch number and operator initials from bmr-sample-01-clean.pdf. The expected batch number is 'BMR-2024-0847' and the expected operator initials are 'JKL'. Compare your extracted values against these expected values and report whether each field matches.
```

**2. Review the agent's validation response**

The agent should extract the two fields, compare them against the expected values, and report whether each field matches:

```json
{
  "validation_results": [
    {
      "field": "batch_number",
      "extracted": "BMR-2024-0847",
      "expected": "BMR-2024-0847",
      "match": true
    },
    {
      "field": "operator_initials",
      "extracted": "JKL",
      "expected": "JKL",
      "match": true
    }
  ],
  "overall_match": true
}
```

**3. Run the validation script**

Save the full extraction output from Exercise 1 to a file (e.g., `output.json`), then run the validation script to compare it against the reference:

```bash
python workshop/scripts/validate_output.py \
  --actual output.json \
  --expected workshop/reference/bmr-sample-01-clean-expected.json
```

The script produces a field-level comparison report showing each field's expected value, actual value, and match status. All fields should match for the clean document.

### Expected Outcome

- The agent correctly identifies that both the batch number and operator initials match the expected values
- The validation script reports all fields as matching with a `PASS` result

### Reference

The reference JSON for this document is at: `workshop/reference/bmr-sample-01-clean-expected.json`

### Discussion Points

- Why is field-level validation important in pharmaceutical manufacturing?
- How could automated validation be integrated into a batch release workflow?
- What happens when a field doesn't match? (You'll explore this in Exercise 5)

---

## Exercise 5: Handling Messy Documents

**Duration:** ~25 minutes
**Goal:** Process a document with difficult handwriting and corrections, and compare the results with the clean document extraction.

### Test Data

**File:** `workshop/test-data/bmr/bmr-sample-02-messy.pdf`
**Difficulty:** Messy — difficult handwriting, crossed-out corrections, ink smudges
**Product:** Metformin HCl 850mg Tablets
**Batch:** BMR-2024-1203

### Instructions

**1. Upload the messy document**

Upload `bmr-sample-02-messy.pdf` via the sidebar file uploader. This replaces the previous document context — the agent will now answer questions about this document.

**2. Submit the basic extraction prompt**

Copy and paste the following prompt:

```
I've uploaded the batch manufacturing record bmr-sample-02-messy.pdf. Please extract all handwritten fields from this document and return the results as structured JSON, including product name, batch number, ingredient names, weights, lot numbers, equipment IDs, operator initials, and timestamps.
```

**3. Review the extraction results**

Examine the JSON output. Compare it with the reference values:

| Field | Expected Value |
|-------|---------------|
| Product Name | Metformin HCl 850mg Tablets |
| Batch Number | BMR-2024-1203 |
| Ingredients | Metformin Hydrochloride (42.50 kg), Povidone K30 (3.20 kg), Stearic Acid (1.10 kg) |
| Equipment IDs | MIX-402, DRY-108, PRESS-115 |
| Operator Initials | RMP |
| Start Timestamp | 2024-04-02T07:15:00 |
| End Timestamp | 2024-04-02T16:30:00 |

**4. Compare with the clean document extraction**

Think about the differences between this extraction and the clean document from Exercise 1:

- Were all fields extracted successfully despite the messy handwriting?
- Did the agent misread any values due to handwriting quality?
- How did the agent handle crossed-out corrections?

### Expected Outcome

A complete JSON object with all BMR fields populated. The agent should extract the data correctly despite the handwriting challenges, though some fields may show minor discrepancies due to handwriting legibility.

### Discussion Points

- What types of handwriting are most challenging for automated extraction?
- How do crossed-out corrections affect extraction accuracy?
- In a production environment, how would you handle cases where the agent is uncertain about a value?
- What is the cost of a misread value in pharmaceutical manufacturing? (Recall: a single transcription error can trigger a $10,000–$50,000 deviation investigation)

---

## Exercise 6: Handling Partial Documents

**Duration:** ~25 minutes
**Goal:** Process a document with missing fields and observe how the agent reports incomplete data using `null` values.

### Test Data

**File:** `workshop/test-data/bmr/bmr-sample-03-partial.pdf`
**Difficulty:** Partial — some fields left blank, incomplete entries
**Product:** Ibuprofen 200mg Tablets
**Batch:** BMR-2024-0592

### Instructions

**1. Upload the partial document**

Upload `bmr-sample-03-partial.pdf` via the sidebar file uploader.

**2. Submit the basic extraction prompt**

Copy and paste the following prompt:

```
I've uploaded the batch manufacturing record bmr-sample-03-partial.pdf. Please extract all handwritten fields from this document and return the results as structured JSON, including product name, batch number, ingredient names, weights, lot numbers, equipment IDs, operator initials, and timestamps.
```

**3. Review the JSON output with null values**

The agent should return a JSON object where missing or unreadable fields are represented as `null`:

```json
{
  "product_name": "Ibuprofen 200mg Tablets",
  "batch_number": "BMR-2024-0592",
  "ingredients": [
    {
      "ingredient_name": "Ibuprofen",
      "weight_kg": 20.00,
      "lot_number": "LOT-IB-20240410"
    },
    {
      "ingredient_name": "Croscarmellose Sodium",
      "weight_kg": null,
      "lot_number": "LOT-CS-20240405"
    }
  ],
  "equipment_ids": null,
  "operator_initials": "TNB",
  "start_timestamp": null,
  "end_timestamp": null
}
```

**4. Identify the missing fields**

Review the output and identify which fields are `null`:

| Field | Value | Status |
|-------|-------|--------|
| `product_name` | Ibuprofen 200mg Tablets | Present |
| `batch_number` | BMR-2024-0592 | Present |
| `ingredients[0].weight_kg` | 20.00 | Present |
| `ingredients[1].weight_kg` | `null` | Missing — weight field was blank |
| `equipment_ids` | `null` | Missing — entire section was blank |
| `operator_initials` | TNB | Present |
| `start_timestamp` | `null` | Missing — timestamp field was blank |
| `end_timestamp` | `null` | Missing — timestamp field was blank |

### Expected Outcome

A JSON object with `null` values for fields that were missing or unreadable in the source document. The agent does not guess or fabricate values — it reports `null` to clearly indicate missing data.

### Reference

For a detailed walkthrough of partial document handling, see: `workshop/examples/error-handling-example.md`

The reference JSON for this document is at: `workshop/reference/bmr-sample-03-partial-expected.json`

### Discussion Points

- Why is returning `null` for missing fields preferable to guessing in pharmaceutical manufacturing?
- How does this behavior align with ALCOA+ data integrity principles?
- In a production workflow, what would happen when the system detects `null` values? (e.g., trigger a review, flag for manual data entry)
- How would you build an automated alert for incomplete batch records?

---

## Wrap-Up and Discussion

**Duration:** ~15 minutes

### Key Takeaways

1. **Structured extraction from handwriting**: The IDP Agent converts handwritten pharmaceutical documents into structured JSON data, eliminating manual transcription and reducing data entry errors.

2. **Flexible querying**: You can perform full extraction, targeted extraction of specific fields, or validation against expected values — all through natural language prompts.

3. **Multi-turn conversation**: The agent maintains document context across conversation turns, allowing follow-up questions without re-uploading or re-processing the document.

4. **Graceful handling of imperfect documents**: The agent processes messy handwriting and partial documents, using `null` values to clearly indicate missing data rather than guessing.

5. **Compliance-ready output**: The structured JSON output, combined with field-level validation, supports FDA 21 CFR Part 11 compliance and ALCOA+ data integrity principles.

### Real-World Deployment Considerations

- **Scale**: In production, the AgentCore runtime handles scaling automatically. A single deployment can process thousands of batch records per day.
- **Accuracy monitoring**: Implement ongoing validation by comparing agent output against manually verified records. Track extraction accuracy metrics over time.
- **Human-in-the-loop**: For high-stakes fields (e.g., ingredient weights, batch numbers), consider a review workflow where extracted values are flagged for human verification before entering the system of record.
- **Document variability**: Real-world documents vary more than workshop samples. Consider building a feedback loop where extraction errors are used to improve the agent's performance over time.
- **Audit trail**: Log all extraction requests and responses for regulatory audit purposes. The AgentCore runtime and AWS Observability Power support this through CloudWatch integration.

### Q&A

Open the floor for questions. Common topics include:

- How does the BDA MCP Server handle different document layouts?
- Can the agent process multi-page documents?
- How would you integrate this into an existing batch record management system?
- What are the costs associated with running this in production?
- How does the agent handle non-English handwriting?

---

## Troubleshooting

### MCP Connection Failures

**Symptom:** The agent returns an error about being unable to connect to the document processing service, or the chat interface shows "Document processing service is unavailable."

**Resolution:**
1. Verify your MCP configuration file exists at `.kiro/settings/mcp.json`
2. Open the file and confirm the `BDA_PROJECT_ARN` value is correct — it should be the full ARN of your Bedrock Data Automation project
3. Confirm the `AWS_REGION` matches the region where your BDA project is deployed
4. Restart the MCP server by reloading Kiro (Command Palette → "Reload Window")

### Missing AWS Credentials

**Symptom:** The pre-flight check reports `[FAIL]` for AWS Credentials, or the agent returns authentication errors.

**Resolution:**
1. Run `aws configure` and enter your AWS Access Key ID, Secret Access Key, and default region
2. Alternatively, set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=your-access-key-id
   export AWS_SECRET_ACCESS_KEY=your-secret-access-key
   export AWS_DEFAULT_REGION=your-region
   ```
3. Verify credentials are working: `aws sts get-caller-identity`

### Timeout Errors

**Symptom:** The chat interface shows "The agent is taking longer than expected" or the request hangs without a response.

**Resolution:**
1. Check your network connection — the agent requires internet access to reach AWS services
2. Verify the BDA MCP Server is running (check Kiro's MCP server status)
3. Try a simpler prompt first to confirm basic connectivity
4. If timeouts persist, check the AWS region — some regions may have higher latency

### File Upload Issues

**Symptom:** The file uploader rejects the file, or the agent cannot process the uploaded document.

**Resolution:**
1. Verify the file format is supported: PDF, PNG, or JPG
2. Check the file size — the maximum upload size is 10MB
3. Ensure the file is not corrupted — try opening it in a PDF viewer first
4. If using a scanned image, ensure it is at least 300 DPI for reliable extraction

### Agent Returns Empty Response

**Symptom:** The agent responds but the JSON output is empty or contains no extracted fields.

**Resolution:**
1. Verify the MCP server is running — check Kiro's MCP server status in the sidebar
2. Confirm the BDA project ARN is correct in your MCP configuration
3. Try re-uploading the document and submitting the prompt again
4. Check the Streamlit console output for error messages (the terminal where you ran `streamlit run`)
5. Use the AWS Observability Power to check CloudWatch logs for agent processing errors
