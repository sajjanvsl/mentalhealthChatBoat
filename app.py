import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime

# Download VADER lexicon (safe, idempotent)
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

# College header
st.set_page_config(page_title="MindMate", layout="wide")
st.markdown("""
<div style="text-align:center; background:#f0f2f6; padding:1rem; border-radius:10px; margin-bottom:1rem;">
    <h4>🏛️ Dept. of Computer Science and Application</h4>
    <p>Govt. First Grade College for Women, Jamkhandi</p>
</div>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello. How are you feeling?"}]
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar
with st.sidebar:
    st.title("MindMate")
    st.markdown("### Mood history")
    if st.session_state.history:
        for ts, label, score in st.session_state.history[-10:]:
            emoji = "😊" if label=="positive" else "😞" if label=="negative" else "😐"
            st.write(f"{ts.strftime('%H:%M:%S')} {emoji} {label} ({score:.2f})")
    else:
        st.info("Chat to see mood history.")
    
    if st.button("Clear chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Cleared. How are you?"}]
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🚨 Indian Helplines")
    st.markdown("📞 iCall: 9152987821 (10am-8pm)")
    st.markdown("📞 Vandrevala: 1860-266-2345 (24x7)")
    st.markdown("🚨 Emergency: 112")
    st.caption("Not a replacement for professional care.")

# Main chat
st.title("💬 MindMate Chat")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("How are you feeling today?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Sentiment analysis
    score = sia.polarity_scores(prompt)["compound"]
    if score >= 0.05:
        label = "positive"
        reply = "That's great! Keep nurturing those positive feelings."
    elif score <= -0.05:
        label = "negative"
        reply = "I hear you're going through a tough time. Would you like to share more? Or call iCall: 9152987821."
    else:
        label = "neutral"
        reply = "Tell me more – I'm here to listen."

    # Crisis detection (override)
    crisis_words = ["suicide", "kill myself", "end my life", "want to die", "self harm", "no hope"]
    if any(w in prompt.lower() for w in crisis_words):
        reply = "🚨 **I'm sorry you're feeling this way.**\n\nIndia helplines:\n📞 iCall: 9152987821\n📞 Vandrevala: 1860-266-2345\n🚨 Emergency: 112\n\nYou are not alone."

    # Save to history
    st.session_state.history.append((datetime.now(), label, score))

    # Add bot response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

    # Sidebar mood indicator
    emoji = "😊" if label=="positive" else "😞" if label=="negative" else "😐"
    st.sidebar.info(f"Latest mood: {emoji} {label} ({score:.2f})")

    st.rerun()
