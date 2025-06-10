import streamlit as st
from google.generativeai import GenerativeModel, configure

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
character_emojis = {name: name.split(" ")[-1] if " " in name else "🤖" for name in character_options}
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

st.title("🎭 Character AI Chat")
st.markdown("Talk to your chosen character below 💌")

# Model name from context (ensure this is a valid model)
active_model_name = "gemini-2.0-flash"

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "current_character_for_session" not in st.session_state:
    st.session_state.current_character_for_session = None

# Only proceed if API key is configured
if api_key_input:
    # If character changed, or chat session not initialized for the current character
    if st.session_state.current_character_for_session != character or st.session_state.chat_session is None:
        st.session_state.current_character_for_session = character
        st.session_state.messages = []  # Clear messages for new character/session
        style_prompt_for_init = character_styles[character]
        
        try:
            model = GenerativeModel(active_model_name)
            initial_model_ack = f"Understood. I am {character}. How can I assist you today?"
            # Prime the chat session with the character's persona
            initial_history = [
                {"role": "user", "parts": [style_prompt_for_init]},
                {"role": "model", "parts": [initial_model_ack]}
            ]
            st.session_state.chat_session = model.start_chat(history=initial_history)
            
            # Add the character's initial acknowledgment to the displayed messages
            st.session_state.messages.append({"role": "assistant", "content": initial_model_ack})
        except Exception as e:
            st.error(f"Failed to initialize chat model ({active_model_name}): {e}")
            st.session_state.chat_session = None # Ensure chat session is None if init fails
            st.stop()

    # Display prior chat messages
    for message in st.session_state.messages:
        avatar_emoji = character_emojis.get(character) if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar_emoji):
            st.markdown(message["content"])

    # Chat input using st.chat_input
    if user_input_val := st.chat_input(f"Chat with {character}..."):
        if st.session_state.chat_session:
            # Add user message to session state and display it
            st.session_state.messages.append({"role": "user", "content": user_input_val})
            with st.chat_message("user"):
                st.markdown(user_input_val)

            # Send message to Gemini and get response
            try:
                response = st.session_state.chat_session.send_message(user_input_val)
                ai_response_text = response.text

                # Add AI response to session state and display it
                st.session_state.messages.append({"role": "assistant", "content": ai_response_text})
                with st.chat_message("assistant", avatar=character_emojis.get(character)):
                    st.markdown(ai_response_text)
            except Exception as e:
                st.error(f"Error generating response: {e}")
        else:
            st.warning("Chat session not initialized. Please ensure API key is correct and a character is selected.")
# The initial API key check at the top handles the case where api_key_input is false.
