import streamlit as st
from google.generativeai import GenerativeModel, configure
import os

# 🛡️ Configure your Gemini API key (keep it secret~!)
configure(api_key=st.secrets["GEMINI_API_KEY"])

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

# 💬 Chat input
user_input = st.text_input("You:", placeholder="Say something...")

# 🧚 Response area
if user_input:
    prompt = f"{style_prompt}\nThe user says: '{user_input}'\nHow would you reply?"
    response = model.generate_content(prompt)
    st.markdown(f"**{character}**: {response.text}")
