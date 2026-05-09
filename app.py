"""
Auto-Méca Expert - Interface Streamlit
"""

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv(override=True)


# ──────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Auto-Méca Expert",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────
# CUSTOM CSS - Industrial / Utilitarian Dark Theme
# ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');

  :root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-card: #1c2333;
    --accent-red: #ff4444;
    --accent-orange: #ff8c00;
    --accent-green: #00d67e;
    --accent-blue: #58a6ff;
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --border: #30363d;
    --mono: 'Share Tech Mono', monospace;
    --heading: 'Rajdhani', sans-serif;
    --body: 'Inter', sans-serif;
  }

  html, body, .stApp {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: var(--body) !important;
  }

  /* Hide default streamlit elements */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem !important; max-width: 1200px; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
  }
  [data-testid="stSidebar"] * { color: var(--text-primary) !important; }

  /* Header */
  .app-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 0 16px;
    border-bottom: 2px solid var(--accent-red);
    margin-bottom: 24px;
  }
  .app-header-icon { font-size: 2.5rem; }
  .app-title {
    font-family: var(--heading);
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 2px;
    text-transform: uppercase;
    line-height: 1;
  }
  .app-subtitle {
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--accent-orange);
    letter-spacing: 1px;
    margin-top: 4px;
  }

  /* Status badges */
  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 4px;
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  .badge-online { background: rgba(0,214,126,0.15); color: var(--accent-green); border: 1px solid rgba(0,214,126,0.3); }
  .badge-model { background: rgba(88,166,255,0.12); color: var(--accent-blue); border: 1px solid rgba(88,166,255,0.25); }
  .badge-rag { background: rgba(255,140,0,0.12); color: var(--accent-orange); border: 1px solid rgba(255,140,0,0.25); }

  /* Chat messages */
  .chat-msg {
    padding: 14px 18px;
    margin: 10px 0;
    border-radius: 6px;
    font-size: 0.92rem;
    line-height: 1.65;
    position: relative;
    animation: fadeIn 0.25s ease;
  }
  .chat-user {
    background: rgba(88,166,255,0.08);
    border: 1px solid rgba(88,166,255,0.2);
    border-left: 3px solid var(--accent-blue);
    margin-left: 60px;
  }
  .chat-user .msg-label {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--accent-blue);
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .chat-agent {
    background: rgba(28,35,51,0.9);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-orange);
    margin-right: 60px;
  }
  .chat-agent .msg-label {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--accent-orange);
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .model-tag {
    float: right;
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--text-secondary);
    background: rgba(255,255,255,0.05);
    padding: 2px 7px;
    border-radius: 3px;
  }

  /* System message */
  .sys-msg {
    text-align: center;
    padding: 8px;
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--text-secondary);
    border: 1px dashed var(--border);
    border-radius: 4px;
    margin: 8px 0;
  }

  /* Input area */
  .stTextArea textarea {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: var(--body) !important;
    font-size: 0.92rem !important;
  }
  .stTextArea textarea:focus {
    border-color: var(--accent-orange) !important;
    box-shadow: 0 0 0 1px var(--accent-orange) !important;
  }

  /* Buttons */
  .stButton > button {
    background: var(--accent-red) !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: var(--heading) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 1px !important;
    padding: 10px 24px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
  }
  .stButton > button:hover {
    background: #cc3333 !important;
    transform: translateY(-1px) !important;
  }

  /* Secondary button */
  .btn-secondary > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text-secondary) !important;
  }
  .btn-secondary > button:hover {
    border-color: var(--accent-red) !important;
    color: var(--accent-red) !important;
  }

  /* Sidebar sections */
  .sidebar-section {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 14px;
    margin: 12px 0;
  }
  .sidebar-section-title {
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--accent-orange);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
  }

  /* Quick action chips */
  .quick-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
  }
  .qa-chip {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 5px 13px;
    font-size: 0.8rem;
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.18s;
  }
  .qa-chip:hover {
    border-color: var(--accent-orange);
    color: var(--accent-orange);
  }

  /* Stats row */
  .stats-row { display: flex; gap: 12px; margin: 16px 0; }
  .stat-box {
    flex: 1;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 12px;
    text-align: center;
  }
  .stat-val {
    font-family: var(--mono);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent-orange);
    display: block;
  }
  .stat-lbl {
    font-size: 0.72rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 5px; }
  ::-webkit-scrollbar-track { background: var(--bg-primary); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  /* File uploader */
  [data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 6px !important;
    padding: 8px !important;
  }

  /* Expander */
  .streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
  }

  /* Divider */
  hr { border-color: var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "session_001"
if "rag_ready" not in st.session_state:
    st.session_state.rag_ready = False
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0
if "last_model" not in st.session_state:
    st.session_state.last_model = "—"
if "extra_docs_loaded" not in st.session_state:
    st.session_state.extra_docs_loaded = 0
if "user_input_value" not in st.session_state:
    st.session_state.user_input_value = ""


# ──────────────────────────────────────────────────────────────
# AGENT INIT
# ──────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def init_agent():
    """Initialise l'agent et le vector store (cached)."""
    from agent import get_vector_store, get_agent
    vs = get_vector_store()
    agent = get_agent()
    return agent, vs is not None


# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo / Title
    st.markdown("""
    <div style="padding:16px 0 8px; text-align:center;">
      <div style="font-size:2.8rem; margin-bottom:6px;">🔧</div>
      <div style="font-family:'Rajdhani',sans-serif; font-size:1.4rem; font-weight:700;
                  letter-spacing:3px; text-transform:uppercase; color:#e6edf3;">
        AUTO-MÉCA
      </div>
      <div style="font-family:'Share Tech Mono',monospace; font-size:0.68rem;
                  color:#ff8c00; letter-spacing:2px; margin-top:2px;">
        EXPERT SYSTEM v1.0
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Init agent
    if st.session_state.agent is None:
        with st.spinner("⚙️ Initialisation du système..."):
            try:
                agent, rag_ok = init_agent()
                st.session_state.agent = agent
                st.session_state.rag_ready = rag_ok
            except Exception as e:
                st.error(f"Erreur d'initialisation: {e}")

    # Status badges
    st.markdown("**STATUT SYSTÈME**")
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; gap:6px; margin:8px 0 14px;">
      <span class="status-badge badge-online">● AGENT EN LIGNE</span>
      <span class="status-badge badge-rag">📚 RAG {'ACTIF' if st.session_state.rag_ready else 'INACTIF'}</span>
      <span class="status-badge badge-model">⚡ SÉLECTION DYNAMIQUE ACTIVE</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # Session stats
    st.markdown(f"""
    <div class="sidebar-section">
      <div class="sidebar-section-title">📊 SESSION COURANTE</div>
      <div class="stats-row">
        <div class="stat-box">
          <span class="stat-val">{st.session_state.msg_count}</span>
          <span class="stat-lbl">Messages</span>
        </div>
        <div class="stat-box">
          <span class="stat-val">{st.session_state.extra_docs_loaded}</span>
          <span class="stat-lbl">Docs ajoutés</span>
        </div>
      </div>
      <div style="font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:#8b949e; margin-top:6px;">
        Thread: {st.session_state.thread_id} | Dernier modèle: {st.session_state.last_model}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Upload additional PDFs
    st.markdown(f"""
    <div class="sidebar-section-title" style="margin-top:16px;">📎 AJOUTER DES MANUELS</div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload PDFs / TXT",
        accept_multiple_files=True,
        type=["pdf", "txt"],
        label_visibility="collapsed",
    )

    if uploaded_files and st.button("Indexer les documents"):
        import agent as agent_module
        from langchain.text_splitter import CharacterTextSplitter
        from langchain_community.embeddings import OpenAIEmbeddings
        from PyPDF2 import PdfReader

        with st.spinner("Indexation en cours..."):
            try:
                extra_text = ""
                for f in uploaded_files:
                    if f.name.endswith(".pdf"):
                        reader = PdfReader(f)
                        for page in reader.pages:
                            extra_text += page.extract_text() or ""
                    else:
                        extra_text += f.read().decode("utf-8", errors="ignore")

                splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                chunks = splitter.split_text(extra_text)
                emb = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

                import agent as agent_module
                if agent_module._vector_store is None:
                    from langchain_community.vectorstores import FAISS
                    agent_module._vector_store = FAISS.from_texts(chunks, emb)
                else:
                    agent_module._vector_store.add_texts(chunks)

                st.session_state.extra_docs_loaded += len(uploaded_files)
                st.session_state.rag_ready = True
                st.success(f"✅ {len(chunks)} chunks indexés!")
            except Exception as e:
                st.error(f"Erreur: {e}")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Nouvelle session
    if st.button("🔄 Nouvelle session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.msg_count = 0
        st.session_state.thread_id = f"session_{len(st.session_state.messages):04d}"
        st.rerun()

    # Model info
    st.markdown("""
    <div class="sidebar-section" style="margin-top:12px;">
      <div class="sidebar-section-title">⚙️ SÉLECTION DYNAMIQUE</div>
      <div style="font-size:0.8rem; color:#8b949e; line-height:1.6;">
        <span style="color:#ff4444;">●</span> <b style="color:#e6edf3;">gpt-4-turbo</b><br>
        &nbsp;&nbsp;diagnostic, panne, erreur code, moteur<br><br>
        <span style="color:#00d67e;">●</span> <b style="color:#e6edf3;">gpt-3.5-turbo</b><br>
        &nbsp;&nbsp;questions générales / stock
      </div>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────
# MAIN CONTENT
# ──────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div class="app-header">
  <div class="app-header-icon">🚗</div>
  <div>
    <div class="app-title">Auto-Méca Expert</div>
    <div class="app-subtitle">SYSTÈME DE SUPPORT TECHNIQUE — VÉHICULES HYBRIDES</div>
  </div>
</div>
""", unsafe_allow_html=True)

# # Quick action examples
# st.markdown("""
# <div style="margin-bottom:14px;">
#   <div style="font-family:'Share Tech Mono',monospace; font-size:0.7rem; color:#8b949e;
#               text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">
#     💡 Exemples de requêtes
#   </div>
#   <div class="quick-actions">
#     <span class="qa-chip">🔴 Diagnostic code P0A0F</span>
#     <span class="qa-chip">⚡ Panne moteur hybride</span>
#     <span class="qa-chip">🔧 Erreur code P0300</span>
#     <span class="qa-chip">📦 Stock batterie Prius</span>
#     <span class="qa-chip">🛢️ Procédure vidange huile</span>
#     <span class="qa-chip">⚠️ Diagnostic IMA Honda</span>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# ── Chat history ──
chat_container = st.container()

with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div class="sys-msg">
          ─── SESSION DÉMARRÉE ─── AGENT PRÊT ─── POSEZ VOTRE PREMIÈRE QUESTION ───
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        model_info = msg.get("model", "")

        if role == "user":
            st.markdown(f"""
            <div class="chat-msg chat-user">
              <div class="msg-label">👨‍🔧 Mécanicien</div>
              {content}
            </div>
            """, unsafe_allow_html=True)
        else:
            model_tag = f'<span class="model-tag">⚡ {model_info}</span>' if model_info else ""
            # Convert markdown-style bold to HTML for display
            display_content = content.replace("\n", "<br>")
            st.markdown(f"""
            <div class="chat-msg chat-agent">
              <div class="msg-label">🤖 Auto-Méca Expert {model_tag}</div>
              {display_content}
            </div>
            """, unsafe_allow_html=True)


# ── Input form ──
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_area(
    "Question",
    placeholder="Décrivez le problème: symptômes, codes erreurs, modèle du véhicule...",
    height=90,
    label_visibility="collapsed",
    key="input_area",
)
with col2:
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    send = st.button("ENVOYER ▶", use_container_width=True)
    st.markdown("<div class='btn-secondary'>", unsafe_allow_html=True)
    clear = st.button("Effacer", use_container_width=True, key="clear_btn")
    st.markdown("</div>", unsafe_allow_html=True)

if clear:
    st.session_state.messages = []
    st.session_state.msg_count = 0
    st.rerun()

# ── Process message ──
if send and user_input.strip():
    if st.session_state.agent is None:
        st.error("Agent non initialisé. Rechargez la page.")
    else:
        # Detect which model will be used
        complex_keywords = ["diagnostic", "panne", "erreur code", "moteur", "défaillance",
                           "problème", "code p", "erreur", "fault", "repair", "réparation"]
        is_complex = any(kw in user_input.lower() for kw in complex_keywords)
        model_used = "gpt-4-turbo" if is_complex else "gpt-3.5-turbo"
        st.session_state.last_model = model_used

        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.msg_count += 1

        # Call agent
        with st.spinner("🔍 Analyse en cours..."):
            try:
                from agent import get_agent as _get_agent
                agent = _get_agent(user_input)
                response = agent.invoke(
                    input={"messages": [HumanMessage(user_input)]},
                    config={"configurable": {"thread_id": st.session_state.thread_id}},
                )
                answer = response["messages"][-1].content

                st.session_state.messages.append({
                    "role": "agent",
                    "content": answer,
                    "model": model_used,
                })
                st.session_state.msg_count += 1
            except Exception as e:
                st.error(f"Erreur de l'agent: {str(e)}")
        st.rerun()
