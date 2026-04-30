import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import time
import random
import base64

# ---------- Setup ----------
nltk.download('vader_lexicon', quiet=True)
sia = SentimentIntensityAnalyzer()

# ---------- Data ----------
AFFIRMATIONS = [
    "You are enough, just as you are.",
    "This feeling will pass. You've survived 100% of your bad days.",
    "It's okay to take a break. Rest is productive.",
    "You are not alone. Reach out if you need to.",
    "Every small step forward is progress.",
    "Your feelings are valid. Today is a new day.",
    "You deserve kindness, especially from yourself.",
    "Breathe. You've got this."
]

RECOVERY_VIDEOS = [
    ("🧘 Guided Meditation for Anxiety", "https://www.youtube.com/watch?v=ZToicYcHIOU"),
    ("💪 Overcoming Depression – Practical Tips", "https://www.youtube.com/watch?v=3BQN8K3E5oE"),
    ("🧠 How to Practice Self-Care", "https://www.youtube.com/watch?v=InVrHhCjB9w"),
    ("🌿 Stress Management Techniques", "https://www.youtube.com/watch?v=0fL-pn80s-c")
]

RECOVERY_TIPS = [
    "🌱 **Talk to someone** – Share your feelings with a trusted friend or family member.",
    "📝 **Write a journal** – Putting thoughts on paper can reduce anxiety.",
    "🧘 **Practice deep breathing** – Try the breathing exercise in the sidebar.",
    "🚶 **Take a walk** – Fresh air and sunlight boost mood.",
    "🛌 **Prioritise sleep** – Rest is essential for mental health.",
    "🍎 **Eat balanced meals** – Nutrition affects your mood.",
    "🎯 **Set small goals** – Celebrate tiny achievements.",
    "🙏 **Be kind to yourself** – You are doing your best."
]

# ---------- Session state ----------
if "messages" not in st.session_state:
    welcome = "Hello. How are you feeling today?"
    affirmation = random.choice(AFFIRMATIONS)
    st.session_state.messages = [
        {"role": "assistant", "content": f"{welcome}\n\n✨ *Daily affirmation:* {affirmation}"}
    ]
if "history" not in st.session_state:
    st.session_state.history = []
if "breathing" not in st.session_state:
    st.session_state.breathing = False

# ---------- Helper: download link ----------
def get_download_link():
    chat_text = ""
    for msg in st.session_state.messages:
        role = "You" if msg["role"] == "user" else "MindMate"
        chat_text += f"{role}: {msg['content']}\n\n"
    b64 = base64.b64encode(chat_text.encode()).decode()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f'<a href="data:text/plain;base64,{b64}" download="mindmate_chat_{timestamp}.txt">📥 Download Chat History</a>'

# ---------- Page config ----------
st.set_page_config(page_title="MindMate – Mental Health Assistant", page_icon="🧠", layout="wide")

# ---------- Sidebar ----------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/brain.png", width=80)
    st.title("MindMate")
    
    st.markdown("### 🚨 **Indian Helplines**")
    st.markdown("📞 iCall (TISS) : 9152987821 (10am-8pm)")
    st.markdown("📞 Vandrevala : 1860-266-2345 (24x7)")
    st.markdown("📞 NIMHANS : 080-46110007 (10am-6pm)")
    st.markdown("📞 Fortis Stress Helpline : 08376804102")
    st.markdown("🚨 Emergency : 112")
    st.markdown("---")
    
    st.markdown("### 📈 Your Mood History")
    if st.session_state.history:
        for ts, label, score in st.session_state.history[-10:]:
            emoji = "😊" if label=="positive" else "😞" if label=="negative" else "😐"
            st.write(f"{ts.strftime('%H:%M:%S')} {emoji} {label} ({score:.2f})")
    else:
        st.info("Chat to see mood history.")
    
    st.markdown("---")
    st.markdown("### 🧘 Breathing Exercise")
    if st.button("Start 1‑minute Box Breathing", use_container_width=True):
        st.session_state.breathing = True
    
    st.markdown("---")
    st.markdown("### 💾 Save Conversation")
    st.markdown(get_download_link(), unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": f"Conversation cleared. {random.choice(AFFIRMATIONS)}"}]
        st.rerun()
    
    st.caption("⚠️ Not a replacement for professional care.")

# ---------- Main area ----------
# College header (above chat title)
st.markdown("""
<div style="text-align:center; background:#e8f0fe; padding:0.8rem; border-radius:10px; margin-bottom:0.5rem;">
    <h4 style="margin:0;">🏛️ Dept. of Computer Science and Application</h4>
    <p style="margin:0; font-size:1rem;">Govt. First Grade College for Women, Jamkhandi</p>
</div>
""", unsafe_allow_html=True)

st.title("💬 MindMate Chat")
st.caption("I'm here to listen. You can type or use voice input (if supported).")

# ---------- Recovery Resources (videos & tips) ----------
with st.expander("📚 **Recovery Resources – Videos & Tips**", expanded=False):
    st.subheader("🎥 Helpful Videos")
    for title, url in RECOVERY_VIDEOS:
        st.markdown(f"- [{title}]({url})")
    st.subheader("💪 How to Recover from Mental Health Challenges")
    for tip in RECOVERY_TIPS:
        st.markdown(tip)
    st.info("Recovery is a journey. Small, consistent steps make a big difference.")

# ---------- Breathing exercise modal ----------
if st.session_state.breathing:
    st.markdown("### 🌬️ Box Breathing Guide")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Start session", use_container_width=True):
            placeholder = st.empty()
            steps = ["Inhale... 4 sec", "Hold... 4 sec", "Exhale... 4 sec", "Hold... 4 sec"]
            for step in steps:
                placeholder.info(f"**{step}**")
                time.sleep(4)
            placeholder.success("✅ Session complete! How do you feel now?")
            time.sleep(1)
        if st.button("Close", use_container_width=True):
            st.session_state.breathing = False
            st.rerun()
    st.markdown("---")

# ---------- Chat history display ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------- User input ----------
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

    # Crisis detection
    crisis_words = ["suicide", "kill myself", "end my life", "want to die", "self harm", "no hope"]
    if any(w in prompt.lower() for w in crisis_words):
        reply = "🚨 **I'm sorry you're feeling this way.**\n\nIndia helplines:\n📞 iCall: 9152987821\n📞 Vandrevala: 1860-266-2345\n📞 NIMHANS: 080-46110007\n🚨 Emergency: 112\n\nYou are not alone."

    # Save to history
    st.session_state.history.append((datetime.now(), label, score))

    # Bot response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

    # Update sidebar mood indicator
    emoji = "😊" if label=="positive" else "😞" if label=="negative" else "😐"
    st.sidebar.info(f"Latest mood: {emoji} {label} ({score:.2f})")

    st.rerun()
