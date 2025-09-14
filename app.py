import streamlit as st
import requests
import re

st.set_page_config(page_title="💊 Pharma Agentic AI Assistant", layout="wide")
st.title("💊 Pharma Agentic AI Assistant")

# ---------- custom CSS (bubbles + input) ----------
st.markdown("""
<style>
/* ---------- Chat container ---------- */
.chat-container {
    max-height: 75vh;
    overflow-y: auto;
    padding: 16px;
    scroll-behavior: smooth;
    background: linear-gradient(145deg, #f9f9fc, #eef1f6);
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}

/* ---------- Chat messages ---------- */
.chat-message {
    padding: 16px 20px;
    margin: 8px 0;
    border-radius: 24px;
    max-width: 70%;
    word-wrap: break-word;
    animation: fadeSlide 0.3s ease-in-out;
    position: relative;
    font-family: 'Segoe UI', sans-serif;
    line-height: 1.4;
}
@keyframes fadeSlide { from {opacity:0; transform: translateY(12px);} to {opacity:1; transform: translateY(0);} }

.user-message {
    background: linear-gradient(120deg, #34B7F1, #00CFFF);
    color: white;
    margin-left:auto;
    text-align:right;
    box-shadow: 0 4px 12px rgba(52, 183, 241, 0.3);
}
/* ---------- Shimmer effect for streaming agent ---------- */
.agent-message.shimmer {
    position: relative;
    overflow: hidden;
    background: linear-gradient(90deg, #e0e0e0 25%, #f0f0f0 50%, #e0e0e0 75%);
    background-size: 200% 100%;
    color: transparent; /* hide original text for shimmer */
    animation: shimmer 1.5s infinite;
    border-radius: 24px;
    padding: 16px 20px;
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Optional: retain avatar on shimmer bubble */
.agent-message.shimmer::before {
    content: "🤖 ";
    position: absolute;
    left: 16px;
    top: 16px;
    color: #25D366;
    font-size: 18px;
}
.followup-message {
    background:#FFF3CD;
    color:#856404;
    margin-right:auto;
    text-align:left;
    font-style:italic;
    border-left:4px solid #FFD966;
    padding-left:14px;
    animation: pulse 1.2s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); }
    100% { transform: scale(1); }
}

/* ---------- Avatars ---------- */
.avatar {
    display:inline-block;
    width:36px;
    height:36px;
    border-radius:50%;
    text-align:center;
    line-height:36px;
    font-size:18px;
    margin:4px;
    transition: transform 0.3s;
}
.avatar:hover { transform: scale(1.2); }
.user-avatar { background:#007BFF; color:white; float:right; }
.agent-avatar { background:#25D366; color:white; float:left; }

/* ---------- Typing dots ---------- */
.typing {
    display:inline-block;
    padding: 8px 12px;
    border-radius: 20px;
    background: #e0e0e0;
    margin: 6px 0;
}
.typing span {
    display:inline-block;
    width: 8px; height: 8px;
    margin: 0 3px;
    background: #999;
    border-radius:50%;
    animation: blink 1.4s infinite both;
}
.typing span:nth-child(2) { animation-delay:.2s; }
.typing span:nth-child(3) { animation-delay:.4s; }
@keyframes blink { 0% {opacity:.2;} 20%{opacity:1;} 100%{opacity:.2;} }

/* ---------- Images & Code ---------- */
img.chat-img { max-width:100%; border-radius:12px; margin-top:8px; transition: transform 0.3s;}
img.chat-img:hover { transform: scale(1.05); }
pre { background:#272822; color:#f8f8f2; padding:12px; border-radius:12px; overflow:auto; box-shadow:0 4px 12px rgba(0,0,0,0.1);}
a { color:#25D366; text-decoration:none; transition: color 0.2s; }
a:hover { color:#1da851; }

/* ---------- Floating input bar ---------- */
.chat-input-bar {
    position: fixed;
    left: 0; right: 0; bottom: 0;
    background: rgba(255,255,255,0.95);
    padding: 14px 20px;
    border-top: 1px solid #eee;
    box-shadow: 0 -4px 24px rgba(0,0,0,0.08);
    backdrop-filter: blur(6px);
    z-index:9999;
}
.chat-input-inner {
    max-width: 900px;
    margin: 0 auto;
    display:flex;
    gap:12px;
    align-items:center;
}
.chat-textbox {
    flex:1;
    padding:14px 18px;
    border-radius:28px;
    border:1px solid #ccc;
    font-size:16px;
    transition: all 0.2s ease-in-out;
}
.chat-textbox:focus {
    border-color:#25D366;
    box-shadow:0 0 0 2px rgba(37,211,102,0.2);
    outline:none;
}
.send-btn {
    background: linear-gradient(135deg,#25D366,#1da851);
    color:white;
    border-radius:50%;
    width:50px; height:50px;
    border:none;
    font-size:20px;
    cursor:pointer;
    transition: transform 0.2s;
}
.send-btn:hover { transform: scale(1.1); }

</style>
""", unsafe_allow_html=True)

# ---------- helper ----------
def clean_response(text: str) -> str:
    # Strip out the extra "AI Response / Steps / Follow-up" markers we don't want during streaming
    text = re.sub(r"--- Steps Taken ---.*", "", text, flags=re.DOTALL)
    text = re.sub(r"--- Follow-up ---.*", "", text, flags=re.DOTALL)
    text = text.replace("--- AI Response ---", "").strip()
    return text

# ---------- session ----------
if "history" not in st.session_state:
    st.session_state["history"] = []

# Load backend history once (if empty)
if not st.session_state["history"]:
    try:
        backend_history = requests.get("http://127.0.0.1:8000/history").json()
        if isinstance(backend_history, list):
            st.session_state["history"] = backend_history
    except Exception:
        st.session_state["history"] = []

# ---------- render function ----------
def render_history():
    """Render every completed message in history (top area)."""
    for msg in st.session_state["history"]:
        user_text = msg.get("query", "")
        agent_text = msg.get("response", "")
        follow_up = msg.get("follow_up", None)

        if user_text:
            st.markdown(
                f"<div class='chat-message user-message'>"
                f"<div class='avatar user-avatar'>💬</div>"
                f"<b>You:</b> {user_text}</div>",
                unsafe_allow_html=True,
            )

        if agent_text:
            st.markdown(
                f"<div class='chat-message agent-message'>"
                f"<div class='avatar agent-avatar'>🤖</div>"
                f"<b>Agent:</b> {agent_text}</div>",
                unsafe_allow_html=True,
            )

        if follow_up and str(follow_up).strip():
            st.markdown(
                f"<div class='chat-message followup-message'>💡 <b>Follow-up:</b> {follow_up}</div>",
                unsafe_allow_html=True,
            )

# ---------- chat container (top) ----------
chat_container = st.container()
with chat_container:
    render_history()   # render completed history at top
    # add a gap so chat isn't hidden under the fixed input bar
    st.markdown("<div style='height:90px'></div>", unsafe_allow_html=True)

# ---------- input UI (styled) ----------
# We'll keep Streamlit input to capture input reliably, but visually place a floating bar
with st.form(key="chat_form", clear_on_submit=True):
  user_query = st.text_input(
    "Message",  # 👈 non-empty label for accessibility
    placeholder="Type your message...",
    label_visibility="collapsed"
)
  submitted = st.form_submit_button("Send")


# ---------- on submit: append user and stream agent into the chat_container ----------
if submitted and user_query.strip():
    # append a history entry (response empty until filled)
    st.session_state["history"].append({
        "query": user_query,
        "response": "",   # will be filled as streaming proceeds
        "agent": "Agent",
        "follow_up": None
    })
    # Keep last input for display (visual)
    st.session_state["_last_input"] = ""

    # Render only the new user message + create a placeholder for streaming INSIDE chat_container
    with chat_container:
        # show the newly added user message immediately (right side)
        st.markdown(
            f"<div class='chat-message user-message'>"
            f"<div class='avatar user-avatar'>💬</div>"
            f"<b>You:</b> {user_query}</div>",
            unsafe_allow_html=True,
        )

        # placeholder for the agent's streaming response (appears above input)
        response_placeholder = st.empty()
        # initial loader text until first chunk
        response_placeholder.markdown(
            f"<div class='chat-message agent-message'>"
            f"<div class='avatar agent-avatar'>🤖</div>"
            f"<b>Agent:</b> ⏳ Thinking...</div>",
            unsafe_allow_html=True,
        )

    # Stream from backend and update the placeholder and session_state
    response_text = ""
    cleaned_text = ""   # <-- initialize before try/loop to avoid NameError
    try:
        r = requests.post(
            "http://127.0.0.1:8000/query-stream",
            json={"user_query": user_query},
            stream=True,
            timeout=120
        )

        for chunk in r.iter_content(chunk_size=1024):
            if not chunk:
                continue
            # accumulate and clean
            try:
                response_text += chunk.decode(errors="ignore")
            except Exception:
                response_text += str(chunk)

            # produce cleaned_text for display (removes steps/follow-up markers)
            cleaned_text = clean_response(response_text)

            # update the session history last item so next full rerun renders correctly
            st.session_state["history"][-1]["response"] = cleaned_text

            # live-update the placeholder INSIDE chat area
            response_placeholder.markdown(
                f"<div class='chat-message agent-message'>"
                f"<div class='avatar agent-avatar'>🤖</div>"
                f"<b>Agent:</b> {cleaned_text}</div>",
                unsafe_allow_html=True,
            )

        # after streaming loop ends ensure final text is stored (safe guard)
        st.session_state["history"][-1]["response"] = cleaned_text

    except Exception as e:
        # show error in the same placeholder area
        with chat_container:
            response_placeholder.markdown(
                f"<div class='chat-message agent-message error-message'>"
                f"<div class='avatar agent-avatar'>🤖</div>"
                f"<b>Error:</b> {e}</div>",
                unsafe_allow_html=True,
            )
        # ensure history last item stores error text too
        st.session_state["history"][-1]["response"] = f"Error: {e}"
