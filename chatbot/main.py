import streamlit as st
from helper import get_response

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Help Desk Chatbot",
    page_icon="🎓",
    layout="centered",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f172a; }

    h1 { color: #f8fafc !important; text-align: center;
         font-family: 'Segoe UI', sans-serif; }

    .user-bubble {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white; padding: 10px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 6px 0 6px 20%; text-align: right;
        font-size: 15px; font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 2px 8px rgba(37,99,235,0.4);
    }
    .bot-bubble {
        background: linear-gradient(135deg, #1e293b, #334155);
        color: #e2e8f0; padding: 10px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 6px 20% 6px 0; text-align: left;
        font-size: 15px; font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .chat-label { font-size: 11px; color: #94a3b8;
                  font-family: 'Segoe UI', sans-serif; }
    .user-label { text-align: right; margin-right: 4px; }
    .bot-label  { text-align: left;  margin-left:  4px; }

    /* Keyword chip buttons */
    .stButton > button {
        background-color: #1e293b !important;
        color: #cbd5e1 !important;
        border: 1px solid #334155 !important;
        border-radius: 20px !important;
        padding: 4px 10px !important;
        font-size: 12px !important;
        font-family: 'Segoe UI', sans-serif !important;
        transition: all 0.2s !important;
        white-space: nowrap !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #2563eb !important;
        color: white !important;
        border-color: #2563eb !important;
    }

    /* Input box */
    .stTextInput > div > div > input {
        background-color: #1e293b !important;
        color: #f1f5f9 !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        font-family: 'Segoe UI', sans-serif !important;
    }

    /* Send button inside form */
    .stForm .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 8px 18px !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        width: 100% !important;
    }

    .chat-box {
        max-height: 52vh;
        overflow-y: auto;
        padding: 8px 4px;
        margin-bottom: 8px;
    }

    .chip-label {
        color: #64748b;
        font-size: 12px;
        font-family: 'Segoe UI', sans-serif;
        margin: 8px 0 4px 2px;
    }

    hr { border-color: #1e293b; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "bot",
        "content": "👋 Hello! I'm your Student Help Desk Assistant. "
                   "Ask me about timetable, exams, assignments, attendance, fees, and much more!"
    }]

if "submitted_text" not in st.session_state:
    st.session_state.submitted_text = ""

if "chip_text" not in st.session_state:
    st.session_state.chip_text = ""

# ── Callbacks ──────────────────────────────────────────────────────────────────
def handle_form_submit():
    val = st.session_state.get("chat_input", "").strip()
    if val:
        st.session_state.submitted_text = val

def make_chip_callback(label):
    def _cb():
        st.session_state.chip_text = label
    return _cb

# ── Process pending input at top of every rerun ────────────────────────────────
pending = ""
if st.session_state.chip_text:
    pending = st.session_state.chip_text
    st.session_state.chip_text = ""
elif st.session_state.submitted_text:
    pending = st.session_state.submitted_text
    st.session_state.submitted_text = ""

if pending:
    st.session_state.messages.append({"role": "user",  "content": pending})
    st.session_state.messages.append({"role": "bot",   "content": get_response(pending)})

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 🎓 Student Help Desk")
st.markdown(
    "<p style='text-align:center;color:#64748b;font-family:Segoe UI,sans-serif;"
    "margin-top:-10px;'>Your 24/7 Academic Assistant</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ── Chat display ───────────────────────────────────────────────────────────────
chat_html = '<div class="chat-box">'
for msg in st.session_state.messages:
    if msg["role"] == "user":
        chat_html += '<div class="chat-label user-label">You</div>'
        chat_html += f'<div class="user-bubble">{msg["content"]}</div>'
    else:
        chat_html += '<div class="chat-label bot-label">🤖 Bot</div>'
        chat_html += f'<div class="bot-bubble">{msg["content"]}</div>'
chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

st.markdown("---")

# ── Input form  →  Enter key AND Send button both work ─────────────────────────
with st.form(key="chat_form", clear_on_submit=True):
    col_input, col_btn = st.columns([6, 1])
    with col_input:
        st.text_input(
            label="msg",
            label_visibility="collapsed",
            placeholder="Type your question and press Enter or click Send…",
            key="chat_input",
        )
    with col_btn:
        st.form_submit_button("Send ➤", on_click=handle_form_submit)

# ── Keyword chips  ─  displayed BELOW the input bar ───────────────────────────
st.markdown('<p class="chip-label">💡 Quick topics — click any to ask instantly:</p>',
            unsafe_allow_html=True)

chips = [
    "Hello",        "Timetable",    "Next Class",   "Exam Dates",
    "Fees",       "Attendance",    "Syllabus",     "Placement",
    "Study Tips",   "college fest" , "Help",
]

ROW_SIZE = 6
for row_start in range(0, len(chips), ROW_SIZE):
    row_chips = chips[row_start: row_start + ROW_SIZE]
    cols = st.columns(len(row_chips))
    for col, chip in zip(cols, row_chips):
        col.button(chip, key=f"chip_{chip}", on_click=make_chip_callback(chip))

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<p style='text-align:center;color:#334155;font-size:12px;"
    "font-family:Segoe UI,sans-serif;margin-top:14px;'>"
    "Student Help Desk Chatbot • Rule-Based NLP Project</p>",
    unsafe_allow_html=True,
)
