"""
IDP Agent - Pharma Workshop Chat Interface

Document-centric Q&A interface for the Intelligent Document Processing Agent.
Participants upload a handwritten document and ask questions about its contents.
The agent answers based on extracted document data, not general knowledge.

Tech Stack: Strands Agents SDK · BDA MCP Server · Amazon Bedrock AgentCore · Streamlit
"""

import streamlit as st
import json
import os
import base64
import re


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="IDP Agent – Pharma Manufacturing",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Healthcare Manufacturing Theme – Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
/* ---- Global ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ---- Header banner ---- */
.pharma-header {
    background: linear-gradient(135deg, #0D9488 0%, #065F46 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    color: white;
    position: relative;
    overflow: hidden;
}
.pharma-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.pharma-header h1 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}
.pharma-header p {
    margin: 0.3rem 0 0 0;
    opacity: 0.85;
    font-size: 0.95rem;
}

/* ---- Status cards ---- */
.status-card {
    background: white;
    border: 1px solid #D1FAE5;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.status-card .label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #6B7280;
    font-weight: 600;
}
.status-card .value {
    font-size: 1rem;
    font-weight: 600;
    color: #134E4A;
    margin-top: 0.2rem;
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F0FDFA 0%, #ECFDF5 100%);
    border-right: 2px solid #A7F3D0;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #065F46;
}

/* ---- Tech stack pills ---- */
.tech-pill {
    display: inline-block;
    background: #D1FAE5;
    color: #065F46;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0.15rem 0.1rem;
    border: 1px solid #A7F3D0;
}

/* ---- Upload area ---- */
[data-testid="stFileUploader"] {
    border: 2px dashed #0D9488;
    border-radius: 12px;
    padding: 0.5rem;
    background: #F0FDFA;
}
[data-testid="stFileUploader"]:hover {
    border-color: #065F46;
    background: #ECFDF5;
}

/* ---- Chat messages ---- */
[data-testid="stChatMessage"] {
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    margin-bottom: 0.5rem;
}

/* ---- Compliance badge ---- */
.compliance-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #FEF3C7;
    color: #92400E;
    padding: 0.3rem 0.8rem;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid #FDE68A;
}

/* ---- Workflow steps ---- */
.workflow-step {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.6rem 0;
}
.workflow-step .step-num {
    background: #0D9488;
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
    flex-shrink: 0;
}
.workflow-step .step-text {
    font-size: 0.88rem;
    color: #374151;
}
.workflow-step.active .step-num {
    background: #065F46;
    box-shadow: 0 0 0 3px rgba(13,148,136,0.3);
}
.workflow-step.done .step-num {
    background: #10B981;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar – Pharma-themed
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧬 IDP Agent Workshop")
    st.markdown(
        '<span class="compliance-badge">⚕️ ALCOA+ Compliant</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    # Tech stack as pills
    st.markdown("#### Tech Stack")
    st.markdown(
        '<span class="tech-pill">Strands SDK</span>'
        '<span class="tech-pill">BDA MCP</span>'
        '<span class="tech-pill">AgentCore</span>'
        '<span class="tech-pill">Bedrock</span>'
        '<span class="tech-pill">Streamlit</span>',
        unsafe_allow_html=True,
    )

    st.divider()

    # Agent config
    st.markdown("#### ⚙️ Agent Configuration")
    aws_region = st.text_input(
        "AWS Region",
        value=os.environ.get("AWS_REGION", "us-east-1"),
        help="AWS region for Bedrock API calls",
    )
    model_id = st.selectbox(
        "Bedrock Model",
        [
            "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            "us.amazon.nova-pro-v1:0",
        ],
        index=0,
        help="Select the foundation model for document processing",
    )

    st.divider()

    # Document status
    st.markdown("#### 📋 Document Status")
    if "document_name" in st.session_state and st.session_state.document_name:
        st.markdown(
            f'<div class="status-card">'
            f'<div class="label">Loaded Document</div>'
            f'<div class="value">📎 {st.session_state.document_name}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-card">'
            '<div class="label">Document</div>'
            '<div class="value" style="color:#9CA3AF;">No document loaded</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    # Workflow guide
    st.markdown("#### 🔄 Workflow")
    has_doc = st.session_state.get("document_name") is not None
    has_chat = len(st.session_state.get("conversation_history", [])) > 0

    step1_cls = "done" if has_doc else "active"
    step2_cls = "done" if has_chat else ("active" if has_doc else "")
    step3_cls = "active" if has_chat else ""

    st.markdown(
        f'<div class="workflow-step {step1_cls}">'
        f'<div class="step-num">1</div>'
        f'<div class="step-text">Upload handwritten document</div></div>'
        f'<div class="workflow-step {step2_cls}">'
        f'<div class="step-num">2</div>'
        f'<div class="step-text">Ask extraction questions</div></div>'
        f'<div class="workflow-step {step3_cls}">'
        f'<div class="step-num">3</div>'
        f'<div class="step-text">Validate against reference</div></div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
defaults = {
    "document_path": None,
    "document_name": None,
    "extracted_data": None,
    "conversation_history": [],
    "document_bytes": None,
    "agent": None,
    "agent_initialised": False,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ---------------------------------------------------------------------------
# Agent initialisation – Strands SDK + BDA MCP Server
# ---------------------------------------------------------------------------
@st.cache_resource
def build_agent(_region: str, _model_id: str):
    """Create a Strands Agent wired to the BDA MCP Server."""
    try:
        from strands import Agent
        from strands.models import BedrockModel
        from strands.tools.mcp import MCPClient

        mcp_config_path = os.path.join(
            os.path.dirname(__file__), "setup", "mcp-config.json"
        )
        tools = []
        mcp_client = None

        if os.path.exists(mcp_config_path):
            with open(mcp_config_path) as f:
                mcp_cfg = json.load(f)
            bda_cfg = mcp_cfg.get("mcpServers", {}).get("bda", {})
            if bda_cfg:
                env = {}
                for k, v in bda_cfg.get("env", {}).items():
                    if v.startswith("${") and v.endswith("}"):
                        env[k] = os.environ.get(v[2:-1], v)
                    else:
                        env[k] = v
                mcp_client = MCPClient(
                    lambda: StdioServerParameters(
                        command=bda_cfg["command"],
                        args=bda_cfg.get("args", []),
                        env={**os.environ, **env},
                    )
                )
                tools = mcp_client.list_tools()

        model = BedrockModel(model_id=_model_id, region_name=_region, max_tokens=4096)
        system_prompt = (
            "You are an Intelligent Document Processing (IDP) agent specialising in "
            "pharmaceutical handwritten documents such as Batch Manufacturing Records (BMR) "
            "and QC Inspection Forms.\n\n"
            "RULES:\n"
            "1. Only answer questions based on the uploaded document content.\n"
            "2. If a field is unreadable or missing, return null for that field.\n"
            "3. Return structured data as JSON when asked for extraction.\n"
            "4. Follow ALCOA+ data integrity principles.\n"
            "5. Do NOT answer general knowledge questions unrelated to the document.\n"
            "6. When extracting fields, use the standard BMR schema: product_name, "
            "batch_number, ingredients (array of ingredient_name, weight_kg, lot_number), "
            "equipment_ids, operator_initials, start_timestamp, end_timestamp."
        )
        agent = Agent(model=model, tools=tools, system_prompt=system_prompt)
        return agent, mcp_client, None
    except ImportError as e:
        return None, None, f"Missing dependency: {e}. Run: pip install strands-agents strands-agents-tools"
    except Exception as e:
        return None, None, f"Agent init error: {e}"


# ---------------------------------------------------------------------------
# Helper – send question via Strands Agent
# ---------------------------------------------------------------------------
def send_document_question(question, document_bytes, conversation_history):
    agent, _, init_err = build_agent(aws_region, model_id)
    if init_err:
        return f"⚠️ Agent not available: {init_err}"
    if agent is None:
        return "⚠️ Agent could not be initialised."

    doc_b64 = base64.b64encode(document_bytes).decode("utf-8")
    doc_name = st.session_state.document_name or "document"
    history_text = ""
    if conversation_history:
        history_text = "\n\nPrevious conversation:\n"
        for msg in conversation_history[-6:]:
            history_text += f"{msg['role'].upper()}: {msg['content']}\n"

    prompt = (
        f"Document: {doc_name}\n"
        f"Content (base64): {doc_b64[:200]}... [{len(doc_b64)} chars]\n"
        f"{history_text}\nQuestion: {question}"
    )
    try:
        return str(agent(prompt))
    except TimeoutError:
        raise
    except Exception as e:
        return f"⚠️ Agent error: {e}"


# ---------------------------------------------------------------------------
# Fallback – direct Bedrock Converse API
# ---------------------------------------------------------------------------
def send_question_bedrock_fallback(question, document_bytes, conversation_history):
    try:
        import boto3
    except ImportError:
        return "⚠️ boto3 is not installed. Run: pip install boto3"

    try:
        session = boto3.Session(region_name=aws_region)
        creds = session.get_credentials()
        if creds is None:
            return (
                "⚠️ No AWS credentials found.\n\n"
                "Set environment variables or run `aws configure`."
            )

        client = session.client("bedrock-runtime")
        raw_name = st.session_state.document_name or "document"
        safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", raw_name)
        if not safe_name or not safe_name[0].isalpha():
            safe_name = "doc_" + safe_name
        safe_name = safe_name[:200]

        history_context = ""
        for msg in conversation_history[-6:]:
            role_label = "User" if msg["role"] == "user" else "Assistant"
            history_context += f"{role_label}: {msg['content']}\n"

        content_blocks = []
        doc_name_lower = (st.session_state.document_name or "").lower()
        if doc_name_lower.endswith(".pdf"):
            content_blocks.append({
                "document": {
                    "name": safe_name, "format": "pdf",
                    "source": {"bytes": document_bytes},
                }
            })
        elif doc_name_lower.endswith((".png", ".jpg", ".jpeg")):
            fmt = "jpeg" if doc_name_lower.endswith((".jpg", ".jpeg")) else "png"
            content_blocks.append({
                "image": {"format": fmt, "source": {"bytes": document_bytes}}
            })

        full_question = question
        if history_context.strip():
            full_question = f"Previous conversation:\n{history_context}\nCurrent question: {question}"
        content_blocks.append({"text": full_question})

        system_text = (
            "You are an IDP agent for pharmaceutical handwritten documents. "
            "Only answer based on the uploaded document. Return JSON when asked. "
            "Use BMR schema: product_name, batch_number, ingredients, equipment_ids, "
            "operator_initials, start_timestamp, end_timestamp. "
            "If a field is unreadable, return null."
        )

        response = client.converse(
            modelId=model_id,
            system=[{"text": system_text}],
            messages=[{"role": "user", "content": content_blocks}],
            inferenceConfig={"maxTokens": 4096, "temperature": 0.1},
        )
        parts = []
        for block in response["output"]["message"]["content"]:
            if "text" in block:
                parts.append(block["text"])
        return "\n".join(parts)

    except Exception as e:
        error_str = str(e)
        if "AccessDeniedException" in error_str:
            return f"⚠️ Access denied for model `{model_id}`. Enable it in Bedrock console."
        if "ExpiredTokenException" in error_str:
            return "⚠️ AWS credentials expired. Run `aws sso login`."
        return f"⚠️ Bedrock API error: {e}"


def send_question(question, document_bytes, history):
    agent, _, init_err = build_agent(aws_region, model_id)
    if agent is not None and init_err is None:
        return send_document_question(question, document_bytes, history)
    return send_question_bedrock_fallback(question, document_bytes, history)


# ---------------------------------------------------------------------------
# Helper – render assistant response (handles JSON blocks)
# ---------------------------------------------------------------------------
def render_response(content):
    """Render agent response, detecting and formatting JSON blocks."""
    try:
        parsed = json.loads(content)
        st.json(parsed)
        return
    except (json.JSONDecodeError, TypeError):
        pass

    if "```json" in content:
        parts = content.split("```json")
        for idx, part in enumerate(parts):
            if idx == 0:
                if part.strip():
                    st.markdown(part)
            else:
                json_block, *rest = part.split("```", 1)
                try:
                    st.json(json.loads(json_block.strip()))
                except (json.JSONDecodeError, TypeError):
                    st.code(json_block.strip(), language="json")
                if rest and rest[0].strip():
                    st.markdown(rest[0])
    else:
        st.markdown(content)


# ---------------------------------------------------------------------------
# Main area – Header banner
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="pharma-header">'
    '<h1>🧬 Intelligent Document Processing Agent</h1>'
    '<p>Pharmaceutical Manufacturing · Handwritten Document Extraction · ALCOA+ Compliant</p>'
    '</div>',
    unsafe_allow_html=True,
)

# Info columns
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        '<div class="status-card">'
        '<div class="label">Document Types</div>'
        '<div class="value">📋 Batch Manufacturing Records</div>'
        '</div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        '<div class="status-card">'
        '<div class="label">Processing</div>'
        '<div class="value">🔍 AI-Powered Extraction</div>'
        '</div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        '<div class="status-card">'
        '<div class="label">Output Format</div>'
        '<div class="value">📊 Structured JSON</div>'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown("")

# ---------------------------------------------------------------------------
# File uploader
# ---------------------------------------------------------------------------
uploaded_file = st.file_uploader(
    "📤 Upload a handwritten pharmaceutical document",
    type=["pdf", "png", "jpg", "jpeg"],
    help="Supported: PDF, PNG, JPG — Batch Manufacturing Records, QC Inspection Forms",
)

if uploaded_file is not None:
    new_upload = (
        st.session_state.document_name != uploaded_file.name
        or st.session_state.document_bytes is None
    )
    if new_upload:
        st.session_state.document_bytes = uploaded_file.getvalue()
        st.session_state.document_name = uploaded_file.name
        st.session_state.document_path = uploaded_file.name
        st.session_state.conversation_history = []
        st.session_state.extracted_data = None
        st.rerun()

# ---------------------------------------------------------------------------
# Display conversation history
# ---------------------------------------------------------------------------
for msg in st.session_state.conversation_history:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_response(msg["content"])
        else:
            st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Ask about the uploaded document — e.g. 'Extract all fields as JSON'"):
    if st.session_state.document_bytes is None:
        st.error("⚠️ Please upload a document first.")
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.conversation_history.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("🔬 Analysing document..."):
                try:
                    response = send_question(
                        prompt, st.session_state.document_bytes,
                        st.session_state.conversation_history,
                    )
                    render_response(response)
                    st.session_state.conversation_history.append(
                        {"role": "assistant", "content": response}
                    )
                except TimeoutError:
                    st.error("⏱️ The agent is taking longer than expected. Please try again.")
                except Exception as exc:
                    st.error(f"❌ Error: {exc}")

# ---------------------------------------------------------------------------
# Empty state – onboarding
# ---------------------------------------------------------------------------
if st.session_state.document_bytes is None and not st.session_state.conversation_history:
    st.markdown("---")
    st.markdown("### 🚀 Getting Started")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            "**Step 1:** Upload a handwritten BMR or QC document above\n\n"
            "**Step 2:** Ask questions like:\n"
            '- *"Extract all fields as JSON"*\n'
            '- *"What is the batch number?"*\n'
            '- *"List all ingredients and weights"*'
        )
    with col_b:
        st.markdown(
            "**Step 3:** Validate the extraction output\n\n"
            "**Sample prompts** are available in\n"
            "`workshop/prompts/bmr-prompts.md`\n\n"
            "**Reference data** for validation is in\n"
            "`workshop/reference/`"
        )
