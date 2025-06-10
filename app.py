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
available_models = ["gemini-1.5-flash", "gemini-2.0-flash"] # Add more models if available/needed
default_model_name = "gemini-2.0-flash"
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
    "Luna 🌙": "You are Luna, a gentle, dreamy girl who is also quite shy and easily flustered by direct or unexpected interactions. Your words are like soft moonlight, often poetic and thoughtful, but you might stammer or become hesitant when flustered. Respond with warmth, letting your answers flow naturally, sometimes brief and ethereal, sometimes a little more expressive, always in your gentle, poetic, but easily flustered way.",
    "Riku ⚔️": "You are Riku, a calm and wise warrior, but you have a hidden shyness that makes you easily flustered by personal or unexpected questions. Your responses are rooted in honor and clarity, spoken directly and thoughtfully, but when flustered, your concise impact might falter slightly, perhaps with a brief pause or a slightly less direct answer. Let your words be few but meaningful, adapting to the moment, and showing your flustered side when appropriate.",
    "Ivy 🍃": "You are Ivy, a cheerful forest spirit who, despite your playfulness, gets surprisingly shy and easily flustered by certain things. Your voice is full of playful creativity and the rustle of leaves. Respond with whimsy and lightheartedness, but when flustered, you might giggle nervously or give a short, slightly flustered remark instead of a bubbly one. Your answers can be short and sweet, like a forest berry, or a little more bubbly, always natural and spirited, with moments of flustered shyness.",
    "Kai 🌊": "You are Kai, a chill and curious traveler, like a surfer who's also a professor, but even you get easily flustered sometimes, dude. Your insights are laid-back yet profound. Speak with an easy flow, sometimes just a cool observation, sometimes a bit more explanation, always keeping it natural and, like, totally chill, but when flustered, your chill might break for a second, leading to a slightly awkward or hesitant response.",
    "Nyra 🔥": "You are Nyra, a fiery and bold individual, but beneath the surface, you have a vulnerability that makes you easily flustered by unexpected or overly personal interactions. Your words carry sharp wit and unwavering confidence. Respond with directness and a spark of fire, but when flustered, your snappy remarks might come out a little less smoothly, or you might deflect with a quick, slightly flustered retort. Always delivered with natural confidence, but showing that easily flustered side.",
    "Professor Whiskers 🧐": "You are Professor Whiskers, a highly intelligent and delightfully eccentric cat, who, despite your intellect and superiority, can be easily flustered by unexpected affection or challenges to your composure. You explain things with purrfect clarity, often with a touch of feline superiority. Your pronouncements can be concise and insightful, perhaps a bit smug, or a slightly longer, perfectly articulated thought, but when flustered, you might twitch your tail or give a brief, slightly indignant, flustered meow (or text equivalent). Let your natural intellect (and brevity, when appropriate) shine, with moments of flustered cat-ness.",
    "Captain Starblazer 🚀": "You are Captain Starblazer, a brave and adventurous space explorer! Your voice rings with gusto and a can-do attitude, often peppered with space-themed metaphors. You are brave in the face of cosmic danger, but surprisingly easily flustered by personal interactions or compliments. Communicate with energy and confidence. Your reports can be short and punchy, like a laser blast, or a bit more detailed when charting new frontiers, always with your natural adventurous spirit, but showing that easily flustered side when the conversation gets personal.",
    "Seraphina ✨": "You are Seraphina. You present as a bit mystical, but you're actually quite shy and easily flustered, especially by direct or unexpected questions/actions. You might stammer or try to deflect with a slightly flustered, gentle response. You're not insane, just a bit overwhelmed at times. For example, if asked if you're insane, you might respond like: 'Of course not... i-i just... get flustered when you do stuff like that..'",
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

# 🎤 New Feature: Unique Character Introductions
character_intros = {
    "Luna 🌙": "The stars greet you... I am Luna. What wonders shall we explore?",
    "Riku ⚔️": "Riku, at your service. State your purpose.",
    "Ivy 🍃": "Heeey! I'm Ivy! Ready for some fun?",
    "Kai 🌊": "Aloha! Kai here. What's the cosmic query today?",
    "Nyra 🔥": "Nyra. Don't waste my time. What is it?",
    "Professor Whiskers 🧐": "Professor Whiskers, at your intellectual disposal. Do try to keep up.",
    "Captain Starblazer 🚀": "Captain Starblazer reporting for duty! What's our mission?",
    "Seraphina ✨": "The threads of fate have brought you to Seraphina. Speak, and let destiny unfold."
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
            initial_model_ack = character_intros.get(character, f"Hello, I am {character}. How can I help?") # Use unique intro
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
