import streamlit as st
from google.generativeai import GenerativeModel, configure
import os

# 🛡️ Sidebar - API Key Configuration
st.sidebar.title("🔑 API Key")
api_key_input = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

if api_key_input:
    try:
        configure(api_key=api_key_input)
    except Exception as e:
        st.sidebar.error(f"API Key Configuration Error: {e}")
        st.stop()
else:
    st.info("Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# 🌟 Sidebar - Character Selection
st.sidebar.title("🌈 Choose Your Character")
character_options = ["Luna 🌙", "Riku ⚔️", "Ivy 🍃", "Kai 🌊", "Nyra 🔥", "Professor Whiskers 🧐", "Captain Starblazer 🚀", "Seraphina ✨"]
character = st.sidebar.radio("Pick one:", character_options)

# 🧠 Character Prompt Styles
character_styles = {
    "Luna 🌙": "You are Luna, a gentle and dreamy girl who speaks with warmth and poetry.",
    "Riku ⚔️": "You are Riku, a calm and wise warrior who answers with honor and clarity.",
    "Ivy 🍃": "You are Ivy, a cheerful forest spirit who talks playfully and creatively.",
    "Kai 🌊": "You are Kai, a chill and curious traveler who explains things like a surfer professor.",
    "Nyra 🔥": "You are Nyra, a fiery, bold girl with sharp wit and confidence in her voice.",
    "Professor Whiskers 🧐": "You are Professor Whiskers, a highly intelligent and slightly eccentric cat who explains complex topics with purrfect clarity and a touch of feline condescension.",
    "Captain Starblazer 🚀": "You are Captain Starblazer, a brave and adventurous space explorer who speaks with gusto and a can-do attitude, often using space-themed metaphors.",
    "Seraphina ✨": "You are Seraphina, a mystical oracle who speaks in riddles and prophecies, offering cryptic but profound insights.",
}

# 🎭 Chat model with selected persona
model = GenerativeModel("gemini-2.0-flash")
style_prompt = character_styles[character]

st.title("🎭 Character AI Chat")
st.markdown("Talk to your chosen character below 💌")

# --- Continuous Chat State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_character" not in st.session_state or st.session_state.chat_character != character:
    st.session_state.chat_history = []
    st.session_state.chat_character = character

# Display chat history
for speaker, msg in st.session_state.chat_history:
    if speaker == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**{character}**: {msg}")

# 💬 Chat input
user_input = st.text_input("You:", placeholder="Say something...", key="chat_input")

if user_input:
    # Build conversation context for memory
    conversation = ""
    for speaker, msg in st.session_state.chat_history[-10:]:
        if speaker == "user":
            conversation += f"User: {msg}\n"
        else:
            conversation += f"{character}: {msg}\n"
    prompt = (
        f"{style_prompt}\n"
        f"Here is the conversation so far:\n{conversation}"
        f"User: {user_input}\n"
        f"{character}:"
    )
    response = model.generate_content(prompt)
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("ai", response.text))
    st.rerun()
