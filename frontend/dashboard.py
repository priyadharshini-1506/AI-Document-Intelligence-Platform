import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI-Powered Document Automation & Intelligence Solution",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# MODERN ENTERPRISE THEME (Corporate Blue & High-Contrast Black Text)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    :root {
        --primary: #0066cc;
        --primary-hover: #0052a3;
        --primary-soft: #eef6ff;
        --text-main: #000000;
        --text-muted: #000000;
        --bg-app: #f8fafc;
        --card-bg: #ffffff;
        --border-color: #cbd5e1;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
        --success: #10b981;
        --success-soft: #ecfdf5;
    }

    /* Global Body styling */
    .stApp {
        background-color: var(--bg-app);
        color: var(--text-main);
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header { background: transparent !important; }
    div[data-testid="stToolbar"] { visibility: hidden; }

    /* Typography styling - Forced to Black */
    h1, h2, h3, h4 { 
        color: var(--text-main) !important; 
        font-weight: 700 !important;
        letter-spacing: -0.02em !important; 
    }
    p, span, label, li { 
        color: var(--text-main) !important; 
    }

    /* Hero Banner (White text inside dark banner is retained for readability) */
    .hero-container {
        background: linear-gradient(135deg, #0066cc 0%, #002244 100%);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 32px;
        color: #ffffff;
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
    }
    .hero-container h1 {
        color: #ffffff !important;
        font-size: 32px !important;
        margin-bottom: 8px !important;
        font-weight: 800 !important;
    }
    .hero-container p, .hero-container span {
        color: rgba(255, 255, 255, 0.95) !important;
        font-size: 15px;
        margin: 0;
    }

    /* Section Titles */
    .section-title {
        font-size: 18px;
        font-weight: 700;
        margin: 24px 0 16px 0;
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--text-main) !important;
    }
    .section-title span {
        color: var(--primary) !important;
    }

    /* Sidebar Polishing */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid var(--border-color);
    }
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: var(--text-main) !important;
    }
    
    /* Document Cards in Sidebar */
    .doc-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-sm);
    }
    .doc-card:hover {
        border-color: var(--primary);
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.08);
    }
    .doc-card-active {
        background: var(--primary-soft);
        border: 2px solid var(--primary);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.08);
    }
    .doc-type-badge {
        display: inline-block;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--primary) !important;
        background: var(--primary-soft);
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 6px;
        margin-top: 6px;
    }

    /* Sidebar buttons overrides */
    section[data-testid="stSidebar"] .stButton>button {
        background: transparent !important;
        color: var(--text-main) !important;
        border: none !important;
        text-align: left !important;
        width: 100% !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 0 !important;
        box-shadow: none !important;
        transform: none !important;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        color: var(--primary) !important;
    }

    /* Primary Action Buttons */
    .stButton>button {
        background: var(--primary) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 24px !important;
        box-shadow: var(--shadow-sm) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton>button p, .stButton>button span {
        color: #ffffff !important;
    }
    .stButton>button:hover {
        background: var(--primary-hover) !important;
        box-shadow: 0 10px 15px -3px rgba(0, 102, 204, 0.3) !important;
        transform: translateY(-1px);
    }

    /* Metric Cards (KPI) - Forced to Black Text */
    div[data-testid="stMetric"] {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px !important;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: var(--primary);
        box-shadow: 0 10px 20px rgba(0,0,0,0.03);
    }
    div[data-testid="stMetricLabel"] { 
        color: var(--text-main) !important; 
        font-size: 13px !important; 
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetricValue"] { 
        color: var(--text-main) !important; 
        font-size: 20px !important; 
        font-weight: 800 !important;
        margin-top: 4px;
    }

    /* Custom Informational Cards */
    .custom-card {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--shadow-sm);
        margin-bottom: 16px;
    }
    .info-strip {
        background: #f8fafc;
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--primary);
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .info-strip div, .info-strip span, .info-strip strong {
        color: var(--text-main) !important;
    }

    /* File Uploader Container styling */
    [data-testid="stFileUploader"] {
        background: var(--card-bg);
        border: 2px dashed rgba(0, 102, 204, 0.35);
        border-radius: 16px;
        padding: 20px;
        transition: border-color 0.2s ease;
    }
    [data-testid="stFileUploader"]:hover { 
        border-color: var(--primary); 
    }
    [data-testid="stFileUploader"] p, [data-testid="stFileUploader"] span {
        color: var(--text-main) !important;
    }

    /* Chat bubble enhancements */
    div[data-testid="stChatMessage"] {
        border-radius: 16px !important;
        padding: 16px !important;
        border: 1px solid var(--border-color) !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] div {
        color: var(--text-main) !important;
    }

    /* Key-Value Tables for Invoices */
    .key-value-table {
        width: 100%;
        border-collapse: collapse;
    }
    .key-value-table tr {
        border-bottom: 1px solid var(--border-color);
    }
    .key-value-table tr:last-child {
        border-bottom: none;
    }
    .key-value-table td {
        padding: 12px 16px;
        font-size: 14px;
    }
    .key-value-key {
        font-weight: 700;
        color: var(--text-main) !important;
        width: 35%;
    }
    .key-value-val {
        color: var(--text-main) !important;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Hero Header
# -----------------------------
st.markdown(
    """
    <div class="hero-container">
        <h1>⚡ AI-Powered Document Automation & Intelligence Solution</h1>
        <p>Dynamic Schema Extraction &nbsp;•&nbsp; Structural Meta-Parsing &nbsp;•&nbsp; Context-Aware Semantic Search</p>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Session State
# -----------------------------
if "document_id" not in st.session_state:
    st.session_state.document_id = None

if "document_type" not in st.session_state:
    st.session_state.document_type = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "extracted" not in st.session_state:
    st.session_state.extracted = {}

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Sidebar History
# -----------------------------
st.sidebar.markdown(
    """
    <div style="padding: 10px 4px 20px 4px; border-bottom: 1px solid var(--border-color); margin-bottom: 20px;">
        <h2 style="margin:0; font-size:22px; font-weight:800; color:#000000 !important;">⚡ Doc<span style="color:var(--primary);">Automation</span></h2>
        <p style="font-size:11px; margin-top:4px; color:#000000 !important; line-height: 1.3;">AI-Powered Intelligence Suite</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown('<p style="font-size:11px; font-weight:800; color:#000000 !important; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:12px;">📚 Repository Index</p>', unsafe_allow_html=True)

try:
    docs = requests.get(f"{API_URL}/documents").json()

    if not docs:
        st.sidebar.caption("No files uploaded to repository.")

    for doc in docs:
        is_active = st.session_state.document_id == doc["id"]
        card_class = "doc-card-active" if is_active else "doc-card"
        
        with st.sidebar.container():
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            if st.button(doc["filename"], key=doc["id"]):
                st.session_state.document_id = doc["id"]
                st.session_state.document_name = doc["filename"]
                st.session_state.document_type = doc["type"]
                st.session_state.messages = []
                st.rerun()
            st.markdown(f'<div class="doc-type-badge">{doc["type"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.sidebar.error(f"Backend Link Offline: {e}")


# -----------------------------
# Upload Container
# -----------------------------
st.markdown('<div class="section-title"><span>📂</span> Ingestion Core</div>', unsafe_allow_html=True)

file = st.file_uploader(
    "Upload Document (PDF, DOCX, PNG, JPG)",
    type=["pdf", "docx", "png", "jpg", "jpeg"],
    label_visibility="collapsed"
)

if file:
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("🚀 Process & Extract", use_container_width=True):
            with st.spinner("Decoding layout schemas..."):
                response = requests.post(
                    f"{API_URL}/upload",
                    files={"file": (file.name, file.getvalue(), file.type)}
                )

                result = response.json()

                st.session_state.document_id = result.get("document_id")
                st.session_state.document_name = result.get("filename")
                st.session_state.document_type = result.get("document_type")
                st.session_state.extracted = result.get("extracted_information", {})
                st.session_state.messages = []

            st.success("Analysis Complete")
            st.rerun()


# -----------------------------
# Document Dashboard (KPI Metrics)
# -----------------------------
if st.session_state.document_id:
    st.divider()
    st.markdown('<div class="section-title"><span>📊</span> Intelligence Telemetry</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Processed Artifact", st.session_state.document_name)

    with col2:
        st.metric("Entity Classification", st.session_state.document_type)

    with col3:
        st.metric("Inference Engine", "Dynamic Schema Ready")


# -----------------------------
# Resume Intelligence Dashboard
# -----------------------------
if st.session_state.document_type == "Resume":
    data = st.session_state.extracted

    st.markdown('<div class="section-title"><span>👤</span> Talent Profile Intelligence</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="custom-card">
                <h3 style="margin-top:0; margin-bottom:16px; font-size:20px; color:#000000 !important;">Identity Index</h3>
                <div style="font-size:18px; font-weight:700; color:var(--primary); margin-bottom:12px;">{data.get("candidate_name", "-")}</div>
                <div style="margin-bottom:8px; display:flex; align-items:center; gap:8px; color:#000000 !important;">📧 <span style="color:#000000 !important; font-weight:600;">{data.get("email", "-")}</span></div>
                <div style="display:flex; align-items:center; gap:8px; color:#000000 !important;">📱 <span style="color:#000000 !important; font-weight:600;">{data.get("phone", "-")}</span></div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col2:
        st.markdown('<div class="custom-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top:0; margin-bottom:16px; font-size:20px; color:#000000 !important;">Skills & Capabilities</h3>', unsafe_allow_html=True)
        skills = data.get("skills", [])
        if skills:
            chips = "".join(
                f'<span style="display:inline-block; background:var(--primary-soft); '
                f'color:var(--primary); border:1px solid rgba(0, 102, 204, 0.25); '
                f'border-radius:8px; padding:6px 14px; margin:4px 6px 4px 0; '
                f'font-size:13px; font-weight:700;">{skill}</span>'
                for skill in skills
            )
            st.markdown(f'<div style="display: flex; flex-wrap: wrap;">{chips}</div>', unsafe_allow_html=True)
        else:
            st.caption("No specialized skills extracted.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title"><span>🎓</span> Education History</div>', unsafe_allow_html=True)
    for edu in data.get("education", []):
        st.markdown(
            f"""
            <div class="info-strip">
                <div style="font-weight:700; font-size:16px; color:#000000 !important;">{edu.get('degree')}</div>
                <div style="color:#000000 !important; font-size:14px; margin:4px 0;">Institution: <strong style="color:#000000 !important;">{edu.get('institution')}</strong></div>
                <div style="font-size:13px; color:#000000 !important; display:flex; gap:16px;">
                    <span>📅 {edu.get('duration')}</span>
                    <span>🎯 Scoring: <strong style="color:var(--primary);">{edu.get('cgpa', 'N/A')}</strong></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-title"><span>🚀</span> Engineered Projects</div>', unsafe_allow_html=True)
    for project in data.get("projects", []):
        with st.expander(project.get("name"), expanded=True):
            st.markdown(f'<div style="padding: 10px 0; font-size:14.5px; line-height:1.6; color:#000000 !important;">{project.get("description")}</div>', unsafe_allow_html=True)


# -----------------------------
# Certificate Verification Dashboard
# -----------------------------
elif st.session_state.document_type == "Certificate":
    data = st.session_state.extracted

    st.markdown('<div class="section-title"><span>🏆</span> Credential Ledger</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="custom-card" style="border-left: 5px solid var(--success);">
            <div style="color: var(--success); font-weight: 800; font-size: 12px; text-transform: uppercase; letter-spacing:0.05em; margin-bottom: 8px;">Metadata Integrity Verified</div>
            <h2 style="margin-top:0; font-size:24px; color:#000000 !important;">{data.get('course')}</h2>
            <p style="font-size:15px; margin: 12px 0; color:#000000 !important;">Recipient: <strong style="color:#000000 !important; font-size:16px;">{data.get('candidate_name')}</strong></p>
            <hr style="border-color:var(--border-color); margin: 16px 0;" />
            <div style="display:flex; justify-content: space-between; font-size:13px; color:#000000 !important;">
                <span>Issuing Body: <strong style="color:#000000 !important;">{data.get('organization')}</strong></span>
                <span>Date of Issue: <strong style="color:#000000 !important;">{data.get('date')}</strong></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# Invoice Intelligence Dashboard
# -----------------------------
elif st.session_state.document_type == "Invoice":
    data = st.session_state.extracted

    st.markdown('<div class="section-title"><span>💰</span> Transaction Intelligence</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="custom-card" style="padding:0; overflow:hidden;">', unsafe_allow_html=True)
        
        table_html = '<table class="key-value-table">'
        for k, v in data.items():
            formatted_key = k.replace('_', ' ').title()
            table_html += f"""
            <tr>
                <td class="key-value-key">{formatted_key}</td>
                <td class="key-value-val">{v}</td>
            </tr>
            """
        table_html += '</table>'
        
        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Chat Interface (Contextual RAG)
# -----------------------------
if st.session_state.document_id:
    st.divider()
    st.markdown('<div class="section-title"><span>💬</span> Contextual Semantic Query Tool</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(f'<div style="font-size: 15px; line-height:1.6; color:#000000 !important;">{msg["content"]}</div>', unsafe_allow_html=True)

    question = st.chat_input("Ask a question regarding the current active document...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        response = requests.post(
            f"{API_URL}/search",
            params={"question": question, "doc_id": st.session_state.document_id}
        )

        answer = response.json().get("answer", "No answer resolved from context.")

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()