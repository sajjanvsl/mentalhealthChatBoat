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

# ---------- FAQ responses (trained) ----------
FAQ_PAIRS = [
    {
        "patterns": ["not feeling great", "not doing well", "feeling down", "bad day", "not great today"],
        "response": "I'm sorry to hear you're not doing well today. It's not always easy, but can you tell me what has you feeling down? I'm here to listen."
    },
    {
        "patterns": ["feel anxious", "feeling anxious", "anxiety", "i'm anxious"],
        "response": "Anxiety can feel very overwhelming. Is your anxiety caused by an upcoming event, one of your relationships, or overthinking? Let's explore this together."
    },
    {
        "patterns": ["overthinking", "overthink", "thinking too much", "can't stop thinking"],
        "response": "When we feel stressed, our brains can run at 100 tabs open. When did you notice this pattern, and does it impact your daily routine? Let's try to challenge one of those thoughts."
    },
    {
        "patterns": ["overwhelmed", "100 things", "too many things", "so much to do", "stressed with work"],
        "response": "Damn, your brain's running at 100 tabs open, huh? 🤯 Ever tried closing some? Let's pick just ONE thing that feels urgent right now."
    }
]

def match_faq(user_message):
    lower_msg = user_message.lower()
    for faq in FAQ_PAIRS:
        for pattern in faq["patterns"]:
            if pattern in lower_msg:
                return faq["response"]
    return None

# ---------- Daily affirmations and tips ----------
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

DAILY_COPING_TIPS = [
    "🌿 **Tip:** When anxious, name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste.",
    "📝 **Tip:** Write down three small things you're grateful for today.",
    "🧘 **Tip:** Try the 4-7-8 breathing: inhale 4s, hold 7s, exhale 8s.",
    "🚶 **Tip:** A 10-minute walk outdoors can reset your mood.",
    "💬 **Tip:** Reach out to one person today – a text or call can help.",
    "🎧 **Tip:** Listen to calming music or nature sounds for 5 minutes.",
    "🍵 **Tip:** Make a warm drink and sit without distractions for a few minutes.",
    "📖 **Tip:** Read a few pages of a book you enjoy – a mini escape."
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

# ---------- Emergency contacts (Indian helplines + emails) ----------
INDIAN_HELPLINES = {
    "iCall (TISS)": {"phone": "9152987821", "email": "icall@tiss.edu", "hours": "Mon-Sat 10am-8pm"},
    "Vandrevala Foundation": {"phone": "1860-266-2345", "email": "help@vandrevalafoundation.com", "hours": "24x7"},
    "NIMHANS Helpline": {"phone": "080-46110007", "email": "nimhanshelpline@gmail.com", "hours": "10am-6pm"},
    "Fortis Stress Helpline": {"phone": "08376804102", "email": "", "hours": "24x7"},
    "Emergency": {"phone": "112", "email": "", "hours": "24x7"}
}

# ---------- Session state ----------
if "messages" not in st.session_state:
    welcome = "Hello. How are you feeling today?"
    affirmation = random.choice(AFFIRMATIONS)
    daily_tip = random.choice(DAILY_COPING_TIPS)
    st.session_state.messages = [
        {"role": "assistant", "content": f"{welcome}\n\n✨ *Daily affirmation:* {affirmation}\n\n💡 *Daily coping tip:* {daily_tip}"}
    ]
if "history" not in st.session_state:
    st.session_state.history = []
if "breathing" not in st.session_state:
    st.session_state.breathing = False
if "grounding" not in st.session_state:
    st.session_state.grounding = False

# ---------- Helper: download link ----------
def get_download_link():
    chat_text = ""
    for msg in st.session_state.messages:
        role = "You" if msg["role"] == "user" else "MindMate"
        chat_text += f"{role}: {msg['content']}\n\n"
    b64 = base64.b64encode(chat_text.encode()).decode()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f'<a href="data:text/plain;base64,{b64}" download="mindmate_chat_{timestamp}.txt">📥 Download Chat History</a>'

# ---------- Grounding exercise ----------
def grounding_exercise():
    st.markdown("### 🌿 5-4-3-2-1 Grounding Exercise")
    st.info("This technique helps bring you back to the present moment during anxiety or panic.")
    steps = [
        "👀 **5 things you can SEE** – Look around and name 5 objects.",
        "🖐️ **4 things you can FEEL** – Touch fabric, your chair, your skin.",
        "👂 **3 things you can HEAR** – Listen for sounds near and far.",
        "👃 **2 things you can SMELL** – Breathe in deeply – coffee, soap, air.",
        "👅 **1 thing you can TASTE** – Take a sip of water or think of a flavour."
    ]
    for step in steps:
        st.markdown(f"- {step}")
    if st.button("✅ Done – back to chat", key="close_grounding"):
        st.session_state.grounding = False
        st.rerun()

# ---------- Page config ----------
st.set_page_config(page_title="MindMate – Mental Health Assistant", page_icon="🧠", layout="wide")

# ---------- Sidebar ----------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/brain.png", width=80)
    st.title("MindMate")
    
    # Emergency contacts expandable
    with st.expander("🚨 **Emergency Contacts (India)**", expanded=False):
        for name, info in INDIAN_HELPLINES.items():
            st.markdown(f"**{name}**")
            st.markdown(f"📞 {info['phone']}")
            if info['email']:
                st.markdown(f"✉️ {info['email']}")
            st.markdown(f"🕒 {info['hours']}")
            st.markdown("---")
    
    st.markdown("### 📈 Your Mood History")
    if st.session_state.history:
        for ts, label, score in st.session_state.history[-10:]:
            emoji = "😊" if label=="positive" else "😞" if label=="negative" else "😐"
            st.write(f"{ts.strftime('%H:%M:%S')} {emoji} {label} ({score:.2f})")
    else:
        st.info("Chat to see mood history.")
    
    st.markdown("---")
    st.markdown("### 🧘 Quick Exercises")
    if st.button("Box Breathing (1 min)", use_container_width=True):
        st.session_state.breathing = True
    if st.button("5-4-3-2-1 Grounding", use_container_width=True):
        st.session_state.grounding = True
    
    st.markdown("---")
    st.markdown("### 💾 Save Conversation")
    st.markdown(get_download_link(), unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        new_tip = random.choice(DAILY_COPING_TIPS)
        st.session_state.messages = [{"role": "assistant", "content": f"Conversation cleared. How are you feeling?\n\n💡 *Daily coping tip:* {new_tip}"}]
        st.rerun()
    
    st.caption("⚠️ Not a replacement for professional care.")

# ---------- Main area ----------
st.markdown("""
<div style="text-align:center; background:#e8f0fe; padding:0.8rem; border-radius:10px; margin-bottom:0.5rem;">
    <h4 style="margin:0;">🏛️ Dept. of Computer Science and Application</h4>
    <p style="margin:0; font-size:1rem;">Govt. First Grade College for Women, Jamkhandi</p>
</div>
""", unsafe_allow_html=True)

st.title("💬 MindMate Chat")
st.caption("I'm here to listen. Type your feelings – I'll respond with care.")

# ---------- Recovery Resources ----------
with st.expander("📚 **Recovery Resources – Videos & Self-Help**", expanded=False):
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

# ---------- Grounding exercise modal ----------
if st.session_state.grounding:
    grounding_exercise()
    st.markdown("---")

# ---------- Chat history display ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------- Core response logic with FAQ priority ----------
def get_bot_response(user_message):
    # Crisis detection (highest priority)
    crisis_words = ["suicide", "kill myself", "end my life", "want to die", "self harm", "no hope"]
    if any(w in user_message.lower() for w in crisis_words):
        return ("🚨 **I'm really sorry you're feeling this way.**\n\n"
                "**India helplines (24x7):**\n"
                "📞 Vandrevala: 1860-266-2345\n"
                "📞 Emergency: 112\n\n"
                "✉️ Email support: icall@tiss.edu, help@vandrevalafoundation.com\n\n"
                "You are not alone. Please reach out now.")
    
    # FAQ matching
    faq_response = match_faq(user_message)
    if faq_response:
        return faq_response
    
    # Sentiment-based fallback
    score = sia.polarity_scores(user_message)["compound"]
    if score >= 0.05:
        return "That's great! Keep nurturing those positive feelings."
    elif score <= -0.05:
        return ("I hear you're going through a tough time. Would you like to share more? "
                "You can also reach iCall at 9152987821 or email icall@tiss.edu.")
    else:
        return "Tell me more – I'm here to listen."

# ---------- User input ----------
if prompt := st.chat_input("How are you feeling today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    reply = get_bot_response(prompt)
    
    # Sentiment logging
    score = sia.polarity_scores(prompt)["compound"]
    if score >= 0.05:
        label = "positive"
    elif score <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    st.session_state.history.append((datetime.now(), label, score))

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

    emoji = "😊" if label=="positive" else "😞" if label=="negative" else "😐"
    st.sidebar.info(f"Latest mood: {emoji} {label} ({score:.2f})")

    st.rerun()
