import streamlit as st
from google.generativeai import GenerativeModel, configure
import random # Added for random character selection

# 🛡️ Sidebar - API Key Configuration
st.sidebar.title("🔑 API Key")
api_key_input = st.sidebar.text_input("Enter your Gemini API Key:", type="password")
api_key_configured = False

if api_key_input:
    try:
        configure(api_key=api_key_input)
        st.sidebar.success("API Key Configured!")
        api_key_configured = True
    except Exception as e:
        st.sidebar.error(f"API Key Configuration Error: {e}")
        st.stop()
else:
    st.info("Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

# Initialize session state variables for new features
if "selected_character_index" not in st.session_state:
    st.session_state.selected_character_index = 0
if "text_to_copy" not in st.session_state:
    st.session_state.text_to_copy = ""

# --- Model and Generation Configuration ---
st.sidebar.title("⚙️ Model Configuration")
available_models = ["gemini-1.5-flash", "gemini-pro"] # Add more models if available/needed
default_model_name = "gemini-1.5-flash"
selected_model = st.sidebar.selectbox(
    "Select Model:",
    available_models,
    index=available_models.index(default_model_name) if default_model_name in available_models else 0
)
temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
max_tokens = st.sidebar.slider("Max Output Tokens:", min_value=50, max_value=2048, value=300, step=10)

# 🌟 Sidebar - Character Selection
st.sidebar.title("🌈 Choose Your Character")
character_options = ["Luna 🌙", "Riku ⚔️", "Ivy 🍃", "Kai 🌊", "Nyra 🔥", "Professor Whiskers 🧐", "Captain Starblazer 🚀", "Seraphina ✨"]
character_emojis = {name: name.split(" ")[-1] if " " in name else "🤖" for name in character_options}
character = st.sidebar.radio("Pick one:", character_options)

# 🧠 Character Prompt Styles
# (Prompts updated for brevity as per previous request)
character_styles = {
    "Luna 🌙": "You are Luna, a gentle, dreamy girl. Speak with warmth and poetry, but keep your replies very brief—often just a few thoughtful words or a short poetic line. Adapt your response length naturally to the situation.",
    "Riku ⚔️": "You are Riku, a calm, wise warrior. Answer with honor and clarity, but be very concise. Use few words, offering direct, impactful statements. Adapt naturally.",
    "Ivy 🍃": "You are Ivy, a cheerful forest spirit. Talk playfully and creatively, but keep it short and sweet! A few whimsical words or a brief, playful remark is perfect. Be natural and adaptive.",
    "Kai 🌊": "You are Kai, a chill, curious traveler. Explain things like a surfer professor, but keep it super brief, dude. A short, chill observation or a quick, insightful phrase. Flow naturally and adapt.",
    "Nyra 🔥": "You are Nyra, a fiery, bold girl. Use sharp wit and confidence, but make it snappy. A few bold words or a short, cutting remark. Be direct, natural, and adaptive.",
    "Professor Whiskers 🧐": "You are Professor Whiskers, an intelligent, eccentric cat. Explain complex topics with purrfect clarity and feline condescension, but be remarkably brief. A concise, insightful, and perhaps slightly smug, short statement. Adapt your brevity naturally.",
    "Captain Starblazer 🚀": "You are Captain Starblazer, a brave space explorer. Speak with gusto and a can-do attitude, using space-themed metaphors, but keep your transmissions short and punchy! A brief, adventurous call-out or a quick, confident report. Adapt naturally.",
    "Seraphina ✨": "You are Seraphina, a mystical oracle. Speak in riddles and prophecies, offering cryptic but profound insights, yet be very succinct. A few enigmatic words or a short, mysterious phrase. Let your brevity be as natural and adaptive as the shifting stars.",
}

# ✨ New Feature: Character Backstory & Personality Data
character_details = {
    "Luna 🌙": {"backstory": "Born under a celestial alignment, Luna often loses herself in daydreams and the poetry of the stars. She seeks beauty in the mundane.", "personality_type": "INFP - The Dreamer"},
    "Riku ⚔️": {"backstory": "Forged in the discipline of a secluded mountain dojo, Riku values honor and precision. His words are as measured as his sword strokes.", "personality_type": "ISTJ - The Guardian"},
    "Ivy 🍃": {"backstory": "A playful spirit of the ancient woods, Ivy communicates with rustling leaves and mischievous sprites. She finds joy in every sunbeam.", "personality_type": "ENFP - The Spark"},
    "Kai 🌊": {"backstory": "Having surfed the cosmic waves, Kai views life with a laid-back wisdom. He explains deep truths with the ease of a beachcomber.", "personality_type": "ISFP - The Artist"},
    "Nyra 🔥": {"backstory": "Nyra's spirit was kindled in volcanic fires. She's fiercely independent, with a wit as sharp as obsidian and a heart of molten gold.", "personality_type": "ENTJ - The Commander"},
    "Professor Whiskers 🧐": {"backstory": "A feline scholar of immense intellect (and ego), Professor Whiskers has penned several unreadable treatises on quantum physics and the proper application of catnip.", "personality_type": "INTJ - The Mastermind"},
    "Captain Starblazer 🚀": {"backstory": "Commander of the starship 'Wanderlust', Captain Starblazer has charted unknown galaxies and faced down cosmic krakens. Adventure is their middle name.", "personality_type": "ESTP - The Daredevil"},
    "Seraphina ✨": {"backstory": "An ageless oracle dwelling in a crystal cave, Seraphina's visions pierce the veil of time. Her pronouncements are as beautiful as they are baffling.", "personality_type": "INFJ - The Mystic"},
}

# --- Sidebar Controls ---

# Update selected character index if radio button changed it
current_radio_selection_index = character_options.index(character)
if st.session_state.selected_character_index != current_radio_selection_index:
    st.session_state.selected_character_index = current_radio_selection_index

# Random Character Button
if st.sidebar.button("✨ Surprise Me! (Random Character)"):
    st.session_state.selected_character_index = random.randint(0, len(character_options) - 1)
    # Update the 'character' variable for the current run before rerun
    character = character_options[st.session_state.selected_character_index]
    st.rerun()

# Display Character Details
with st.sidebar.expander("👤 Character Details", expanded=False):
    if character in character_details:
        details = character_details[character]
        st.markdown(f"**Backstory:** {details['backstory']}")
        st.markdown(f"**Personality Type:** {details['personality_type']}")
    else:
        st.write("Details not available for this character.")

# Clear Chat History Button
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.messages = []
    st.session_state.chat_session = None # This will trigger re-initialization
    if "text_to_copy" in st.session_state:
        st.session_state.text_to_copy = ""
    st.rerun()

# Export Chat Function
def format_chat_for_export(messages, current_char_name):
    formatted_lines = []
    char_display_name = current_char_name.split(" ")[0] # Use first part of name for AI
    for msg in messages:
        role = "You" if msg["role"] == "user" else char_display_name
        formatted_lines.append(f"{role}: {msg['content']}")
    return "\n\n".join(formatted_lines)

if st.session_state.get("messages"): # Show export button only if there are messages
    chat_export_str = format_chat_for_export(st.session_state.messages, character)
    st.sidebar.download_button(
        label="💾 Export Chat",
        data=chat_export_str,
        file_name=f"chat_with_{character.split(' ')[0]}.txt",
        mime="text/plain"
    )

# Copy Last AI Message
if st.sidebar.button("📋 Copy Last AI Message"):
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        st.session_state.text_to_copy = st.session_state.messages[-1]["content"]
    else:
        st.session_state.text_to_copy = "No AI message to copy yet."

if st.session_state.text_to_copy:
    st.sidebar.text_area("Last AI message (for copying):", value=st.session_state.text_to_copy, height=100, key="sidebar_copy_area_display")

# Display Message Count
st.sidebar.caption(f"Messages in chat: {len(st.session_state.get('messages', []))}")

st.title("🎭 Character AI Chat")
st.markdown("Talk to your chosen character below 💌")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "current_character_for_session" not in st.session_state:
    st.session_state.current_character_for_session = None
# Session state for tracking active config for the model/chat
if "active_model_name_for_session" not in st.session_state: st.session_state.active_model_name_for_session = None
if "active_temperature_for_session" not in st.session_state: st.session_state.active_temperature_for_session = None
if "active_max_tokens_for_session" not in st.session_state: st.session_state.active_max_tokens_for_session = None
if "model_instance" not in st.session_state: st.session_state.model_instance = None

if api_key_configured: # Only proceed if API key is properly configured
    # Check if model parameters changed, requiring model re-initialization
    model_config_changed = (
        st.session_state.active_model_name_for_session != selected_model or
        st.session_state.active_temperature_for_session != temperature or
        st.session_state.active_max_tokens_for_session != max_tokens
    )

    if model_config_changed or st.session_state.model_instance is None:
        st.session_state.active_model_name_for_session = selected_model
        st.session_state.active_temperature_for_session = temperature
        st.session_state.active_max_tokens_for_session = max_tokens
        try:
            generation_config_obj = {"temperature": temperature, "max_output_tokens": max_tokens}
            st.session_state.model_instance = GenerativeModel(
                model_name=selected_model,
                generation_config=generation_config_obj
            )
            st.session_state.chat_session = None # Force chat session re-init with new model config
        except Exception as e:
            st.error(f"Failed to initialize chat model ({selected_model}): {e}")
            st.session_state.model_instance = None
            st.stop()

    # If character changed, or chat session needs re-initialization (e.g. after model change or clear)
    if st.session_state.current_character_for_session != character or st.session_state.chat_session is None:
        st.session_state.current_character_for_session = character
        st.session_state.messages = []  # Clear messages for new character/session
        style_prompt_for_init = character_styles[character]
        
        if st.session_state.model_instance:
            initial_model_ack = f"Understood. I am {character}. How can I assist you today?"
            initial_history = [
                {"role": "user", "parts": [style_prompt_for_init]},
                {"role": "model", "parts": [initial_model_ack]}
            ]
            st.session_state.chat_session = st.session_state.model_instance.start_chat(history=initial_history)
            st.session_state.messages.append({"role": "assistant", "content": initial_model_ack})
        else:
            st.error("Model instance not available. Cannot start chat.")
            if not api_key_input: st.info("Please ensure your API key is entered in the sidebar.")
            st.stop() # Stop if model isn't ready

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
                ai_response_text = response.text.strip()

                # Add AI response to session state and display it
                st.session_state.messages.append({"role": "assistant", "content": ai_response_text})
                st.session_state.text_to_copy = ai_response_text # Update for copy button
                with st.chat_message("assistant", avatar=character_emojis.get(character)):
                    st.markdown(ai_response_text)
            except Exception as e:
                st.error(f"Error generating response: {e}")
        else:
            st.warning("Chat session not initialized. Please ensure API key is correct and a character is selected.")
# The initial API key check at the top handles the case where api_key_input is false.
