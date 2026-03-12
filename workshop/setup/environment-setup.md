# Environment Setup Guide

This guide walks you through setting up your development environment for the IDP Pharma Workshop. Complete all steps below before starting the workshop exercises.

## Prerequisites

- **Python 3.10+** — verify with `python --version`
- **AWS Account** with Amazon Bedrock access enabled in your target region
- **Kiro IDE** installed and running

---

## 1. Install Kiro Powers

The workshop uses three Kiro Powers that provide IDE-integrated capabilities for building, deploying, and monitoring the IDP Agent.

### Installation Steps

1. Open Kiro
2. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
3. Search for **"Configure Powers"** and select it
4. Install each of the following powers:

### AWS AgentCore Power

Provides capabilities for building, deploying, and managing the IDP Agent via Amazon Bedrock AgentCore. You will use this power to deploy and operate the agent runtime during the workshop.

### Strands Power

Provides capabilities for building and iterating on agents using the Strands Agents SDK. You will use this power to develop and test the IDP Agent's document processing logic.

### AWS Observability Power

Provides capabilities for monitoring, logging, and troubleshooting the IDP Agent. You will use this power to inspect agent behavior, review CloudWatch logs, and diagnose issues during workshop exercises.

---

## 2. Configure the MCP Server

The IDP Agent communicates with the Amazon Bedrock Data Automation (BDA) service through an MCP server. You need to configure this connection.

### Configuration Template

A ready-to-use MCP configuration template is provided at:

```
workshop/setup/mcp-config.json
```

The template looks like this:

```json
{
  "mcpServers": {
    "bda": {
      "command": "python",
      "args": ["-m", "bda_mcp_server"],
      "env": {
        "AWS_REGION": "${AWS_REGION}",
        "BDA_PROJECT_ARN": "${BDA_PROJECT_ARN}"
      }
    }
  }
}
```

### Filling In Your Values

Replace the placeholder values with your environment-specific settings:

- **`AWS_REGION`** — The AWS region where Bedrock and BDA are enabled (e.g., `us-east-1`, `us-west-2`)
- **`BDA_PROJECT_ARN`** — The ARN of your Bedrock Data Automation project. You can find this in the AWS Console under Amazon Bedrock → Data Automation → Projects.

### Placing the Configuration

Copy your completed configuration to the Kiro settings directory:

```
.kiro/settings/mcp.json
```

This is where Kiro reads MCP server configurations from. You can copy the template and edit it in place:

```bash
mkdir -p .kiro/settings
cp workshop/setup/mcp-config.json .kiro/settings/mcp.json
```

Then open `.kiro/settings/mcp.json` and replace the `${AWS_REGION}` and `${BDA_PROJECT_ARN}` placeholders with your actual values.

---

## 3. Install Python Dependencies

Install the required Python packages using the provided requirements file:

```bash
pip install -r workshop/setup/requirements.txt
```

This installs the following packages:

| Package | Purpose |
|---------|---------|
| `strands-agents` | Strands Agents SDK — the agent framework powering the IDP Agent |
| `strands-agents-tools` | Tool integrations for the Strands Agent |
| `streamlit` | Web UI framework for the workshop chat interface |
| `boto3` | AWS SDK for Python — used for AWS service access and credential management |

---

## 4. Configure AWS Credentials

The workshop requires AWS credentials with access to Amazon Bedrock and S3 (for document storage).

### Option A: AWS CLI Configuration

```bash
aws configure
```

Enter your AWS Access Key ID, Secret Access Key, default region, and output format when prompted.

### Option B: Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_DEFAULT_REGION=your-region
```

### Required Permissions

Your AWS credentials must have access to:

- **Amazon Bedrock** — invoke foundation models and access Bedrock Data Automation
- **Amazon S3** — read/write access to the S3 bucket used for document storage

---

## 5. Pre-flight Verification

Run the verification script to confirm everything is set up correctly:

```bash
python workshop/setup/verify-setup.py
```

### What It Checks

| Check | What It Verifies |
|-------|-----------------|
| Python: strands-agents | `strands_agents` module is importable |
| Python: streamlit | `streamlit` module is importable |
| Python: boto3 | `boto3` module is importable |
| AWS Credentials | Valid credentials found via `boto3.Session().get_credentials()` |
| MCP Configuration | `workshop/setup/mcp-config.json` exists and contains valid JSON with an `mcpServers` entry |

### Interpreting Results

- **[PASS]** — The component is correctly configured
- **[FAIL]** — The component needs attention. Each failure includes a remediation message explaining how to fix it.

The script exits with code `0` if all checks pass, or `1` if any check fails.

> **Note:** Kiro Powers (IDE extensions) cannot be verified programmatically. The script will remind you to confirm they are installed manually.

---

## 6. Launch the Workshop

Once all checks pass, start the workshop chat interface:

```bash
streamlit run workshop/app.py
```

This opens the Streamlit-based chat UI in your browser where you can upload handwritten documents and interact with the IDP Agent.
