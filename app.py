# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 21:50:03 2026

@author: Admin
"""

import streamlit as st
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os
from datetime import datetime

# Setup NLTK data directory (writable on cloud)
nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)
try:
    nltk.data.find(f"{nltk_data_dir}/sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon", download_dir=nltk_data_dir)

sia = SentimentIntensityAnalyzer()

# College header
st.set_page_config(page_title="MindMate", layout="wide")
st.markdown("""
<div style="text-align:center; background:#f0f2f6; padding:1rem; border-radius:10px;">
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
    for ts, label, score in st.session_state.history[-10:]:
        emoji = "😊" if label=="positive" else "😞" if label=="negative" else "😐"
        st.write(f"{ts.strftime('%H:%M:%S')} {emoji} {label} ({score:.2f})")
    if st.button("Clear chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Cleared. How are you?"}]
        st.rerun()
    st.markdown("---")
    st.markdown("🚨 **Indian Helplines**\n📞 iCall: 9152987821\n📞 Vandrevala: 1860-266-2345")
    st.caption("Not a replacement for professional care.")

# Main chat
st.title("💬 MindMate Chat")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    score = sia.polarity_scores(prompt)["compound"]
    if score >= 0.05:
        label = "positive"
        reply = "That's great! Keep it up."
    elif score <= -0.05:
        label = "negative"
        reply = "I hear you're struggling. Consider calling iCall: 9152987821."
    else:
        label = "neutral"
        reply = "Tell me more – I'm here to listen."

    crisis_words = ["suicide", "kill myself", "end my life", "self harm"]
    if any(w in prompt.lower() for w in crisis_words):
        reply = "🚨 **Crisis alert**\n\nIndia helplines:\n📞 iCall: 9152987821\n📞 Vandrevala: 1860-266-2345"

    st.session_state.history.append((datetime.now(), label, score))
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
    st.rerun()