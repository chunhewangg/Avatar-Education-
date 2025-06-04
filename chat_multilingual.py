import streamlit as st
import requests
import json
import time
import os
import anthropic
import openai

# Streamlit app setup
st.set_page_config(page_title="AI Avatar Chat", page_icon="🤖")
st.title("Chat with AI Avatars")

# Language code to full name mapping
LANGUAGE_NAMES = {
    "en": "English",
    "zh": "Chinese",
    "es": "Spanish",
    "fr": "French",
    "ja": "Japanese",
    "ko": "Korean"
}

# Hardcoded password (not secure for production use)
PASSWORD = "chatbot"

# Initialize session state for authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Authentication logic
if not st.session_state.authenticated:
    password_input = st.text_input("Enter Password:", type="password")
    if password_input == PASSWORD:
        st.session_state.authenticated = True
        st.rerun()
    else:
        st.stop()  # Prevents the rest of the page from loading

# Main app content (only shown if authenticated)
st.write("Welcome! Feel free to switch to different avatars and start to chat.")
st.write("The assistant supports multiple languages with multilingual voices.")

# Debug mode toggle in sidebar
st.sidebar.subheader("Advanced Settings")
debug_mode = st.sidebar.checkbox("Enable Debug Mode")

# Language support information
st.sidebar.subheader("Supported Languages")
supported_languages = [
    {"code": "en", "name": "English", "supported": True, "voice": "Native"},
    {"code": "zh-CN", "name": "Chinese (Mandarin)", "supported": True, "voice": "Multilingual"},
    {"code": "es", "name": "Spanish", "supported": True, "voice": "Multilingual"},
    {"code": "fr", "name": "French", "supported": True, "voice": "Multilingual"},
    {"code": "ja", "name": "Japanese", "supported": True, "voice": "Multilingual"},
    {"code": "ko", "name": "Korean", "supported": True, "voice": "Multilingual"},
    {"code": "de", "name": "German", "supported": True, "voice": "Multilingual"},
    {"code": "it", "name": "Italian", "supported": True, "voice": "Multilingual"},
    {"code": "pt", "name": "Portuguese", "supported": True, "voice": "Multilingual"},
    {"code": "ru", "name": "Russian", "supported": True, "voice": "Multilingual"},
    {"code": "hi", "name": "Hindi", "supported": True, "voice": "Multilingual"},
    {"code": "ar", "name": "Arabic", "supported": True, "voice": "Multilingual"},
]


if debug_mode:
    st.sidebar.info("""
    Voice Types:
    - Native: Language-specific voices optimized for that language
    - Multilingual: Generic voices that work with multiple languages
    """)
    
    st.sidebar.subheader("Multilingual Voice IDs")
    st.sidebar.markdown("""
    - Skylar (F, Young): `1ae3be1e24894ccabdb4d8139399f721`
    - Nova (F, Mature): `8bfd950373f7439c92f1dec2fc072333`
    - Fable (M, Young): `8b92884579014f8e8147836bbd0c13ca`
    - Harry (M, Mature): `b66ccf9ec0c94388a9ed2d2373907404`
    """)

# Explain potential language issues
st.sidebar.info("""
**Note about non-English languages:**

For languages other than English, we use multilingual voices.
These may sometimes encounter errors with certain texts.
If you experience issues, try using simpler sentences.
""")



# API Keys - Set directly in code
CLAUDE_API_KEY = "###########################################"
OPENAI_API_KEY = "###########################################"
HEYGEN_API_KEY = "###########################################"
HEYGEN_API_URL = "https://api.heygen.com/v2"

# Initialize Claude client
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# Initialize session state for chat history and API conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize a separate history for API calls that will maintain context
if "api_messages" not in st.session_state:
    st.session_state.api_messages = [
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Hello! I'm your AI assistant. How can I help you today?"
                }
            ]
        }
    ]

# Sidebar with avatar selection
st.sidebar.title("Avatar Settings")

# Available HeyGen avatars with gender and age metadata
avatar_options = {
    # Female avatars
    "Angela-inblackskirt-20220820": {"display_name": "Angela (Young Female)", "gender": "female", "age": "young"},
    "Daisy-inskirt-20220818": {"display_name": "Daisy (Mature Female)", "gender": "female", "age": "mature"},
    "Natalie-inblackdress-20230922": {"display_name": "Natalie (Young Female)", "gender": "female", "age": "young"},
    "Amelia-inblueoutfit-20220822": {"display_name": "Amelia (Mature Female)", "gender": "female", "age": "mature"},
    
    # Male avatars
    "Daniel-insuitnoglasses-20230724": {"display_name": "Daniel (Young Male)", "gender": "male", "age": "young"},
    "Ben-insuitwithtie-20220727": {"display_name": "Ben (Mature Male)", "gender": "male", "age": "mature"},
    "Alex-insuitwithoutie-20230302": {"display_name": "Alex (Young Male)", "gender": "male", "age": "young"},
    "Thomas-insuitwithtie-20220819": {"display_name": "Thomas (Mature Male)", "gender": "male", "age": "mature"}
}

talking_photo_options = {
    "6bd4b0a03c2e41979ad2e8498d093bd0": {"display_name": "Girl"},
    "527f55c838344a27af5f268dfe1920a5": {"display_name": "Professional Woman"},
    "6112aff6fe364e81898dd8dad717a943": {"display_name": "Young Girl"}
    # Add more talking photos as needed with their IDs
}

# Add language selection
st.sidebar.subheader("Language Settings")
st.sidebar.markdown("*Note: The assistant will automatically detect and respond in the language you use.*")

# Avatar selection with improved UI
st.sidebar.subheader("Avatar Selection")

# Group avatars by gender for better organization
female_avatars = {k: v for k, v in avatar_options.items() if v["gender"] == "female"}
male_avatars = {k: v for k, v in avatar_options.items() if v["gender"] == "male"}

character_type = st.sidebar.radio(
    "Select Character Type",
    options=["Avatar", "Talking Photo"],
    index=0,  # Default to Avatar
    horizontal=True
)

# Replace your current avatar selection code with this conditional logic
if character_type == "Avatar":
    # Group avatars by gender for better organization
    gender_selection = st.sidebar.radio(
        "Select Gender",
        options=["Female", "Male"],
        index=0,  # Default to Female
        horizontal=True
    )

    # Filter avatars based on selected gender
    if gender_selection == "Female":
        avatar_subset = female_avatars
    else:
        avatar_subset = male_avatars

    # Create the selectbox for the filtered avatars
    selected_character = st.sidebar.selectbox(
        "Choose Avatar", 
        options=list(avatar_subset.keys()),
        format_func=lambda x: avatar_subset[x]["display_name"]
    )
    selected_character_type = "avatar"
else:
    # Select a talking photo
    selected_character = st.sidebar.selectbox(
        "Choose Talking Photo", 
        options=list(talking_photo_options.keys()),
        format_func=lambda x: talking_photo_options[x]["display_name"]
    )
    selected_character_type = "talking_photo"
# Function to get LLM response using Claude API
def get_llm_response(prompt):
    # Updated system prompt to detect and respond in the same language as input
    system_prompt = """You are a helpful AI assistant speaking through a video avatar. 

Important: ALWAYS respond in the SAME LANGUAGE as the user's message.

Your responses must be:
1. Concise - exactly 10-20 words
2. Direct - no preambles, explanations, or reasoning
3. Conversational - as if talking naturally to a friend
4. Clean - no special markers, tags, or formatting
5. In the SAME LANGUAGE as the user's input (whether English, Chinese, Spanish, etc.)

ONLY provide the exact words you want the avatar to say. Do not include any reasoning, 
explanations about what you're doing, or meta-commentary about your response.
"""
    
    try:
        # Add the user's new message to the API conversation history
        st.session_state.api_messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        })
        
        # Send the entire conversation history to Claude
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=150,
            system=system_prompt,
            messages=st.session_state.api_messages
        )
        
        # Get Claude's response
        assistant_response = response.content[0].text.strip()
        
        # Add the response to the API conversation history
        st.session_state.api_messages.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": assistant_response
                }
            ]
        })
        
        return assistant_response
    except anthropic.APIError as e:
        error_message = str(e)
        if "overloaded" in error_message or "529" in error_message:
            st.warning("Claude is overloaded. Switching to ChatGPT.")
            return get_fallback_response(prompt)
        else:
            st.error(f"Error getting Claude response: {e}")
            return "I'm having trouble connecting to Claude. Please try again later."

def get_fallback_response(prompt):
    """Fallback to OpenAI's GPT-3.5 Turbo"""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Convert the API message history to OpenAI format
        openai_messages = []
        
        # Add system message with updated language instruction
        openai_messages.append({
            "role": "system", 
            "content": """You are a helpful AI assistant speaking through a video avatar. 

Important: ALWAYS respond in the SAME LANGUAGE as the user's message.

Your responses must be:
1. Concise - exactly 10-20 words
2. Direct - no preambles, explanations, or reasoning
3. Conversational - as if talking naturally to a friend
4. Clean - no special markers, tags, or formatting
5. In the SAME LANGUAGE as the user's input (whether English, Chinese, Spanish, etc.)

ONLY provide the exact words you want the avatar to say. Do not include any reasoning, 
explanations about what you're doing, or meta-commentary about your response.
"""
        })
        
        # Convert the conversation history
        for msg in st.session_state.api_messages:
            role = msg["role"]
            # Skip the initial assistant message to avoid confusion
            if role == "assistant" and len(openai_messages) == 1:
                continue
                
            content = msg["content"][0]["text"] if isinstance(msg["content"], list) else msg["content"]
            openai_messages.append({"role": role, "content": content})
        
        # Add the current user message if not already included
        if openai_messages[-1]["role"] != "user" or openai_messages[-1]["content"] != prompt:
            openai_messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=openai_messages,
            max_tokens=150
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Add the response to the API conversation history
        st.session_state.api_messages.append({
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": response_text
                }
            ]
        })
        
        return response_text
    except Exception as e:
        return f"Error getting fallback response: {e}"

# Function to detect language of text with more detailed Chinese detection
def detect_language(text):
    # Check for Chinese characters
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        # For voice_map key consistency, return "zh" instead of "zh-CN"
        return "zh"
    
    # Add more language detection logic here...
    # Check for Japanese characters (Hiragana, Katakana)
    if any('\u3040' <= char <= '\u30ff' for char in text):
        return "ja"  # Japanese
    
    # Check for Korean characters
    if any('\uac00' <= char <= '\ud7a3' for char in text):
        return "ko"  # Korean
    
    # Check for common Spanish words
    spanish_words = ["el", "la", "los", "las", "un", "una", "y", "o", "pero", "porque", "como", "qué", "cuándo", "dónde"]
    words = text.lower().split()
    if any(word in spanish_words for word in words) and any('á' in text or 'é' in text or 'í' in text or 'ó' in text or 'ú' in text or 'ñ' in text):
        return "es"  # Spanish
    
    # Check for common French words
    french_words = ["le", "la", "les", "un", "une", "des", "et", "ou", "mais", "parce", "que", "comment", "quand", "où"]
    if any(word in french_words for word in words) and any('é' in text or 'è' in text or 'ê' in text or 'ç' in text or 'à' in text):
        return "fr"  # French
    
    # Default to English
    return "en"

def generate_heygen_video(character_id, text, character_type="avatar"):
    # Create progress tracking elements
    progress_placeholder = st.empty()
    progress_bar = st.progress(0)
    progress_placeholder.info("Preparing to generate video...")
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": HEYGEN_API_KEY
    }
    
    # Detect language of the response
    detected_language = detect_language(text)
    
    # Voice ID mapping by language and gender
    voice_map = {
        # English voices
        "en": {
            "female_young": "1bd001e7e50f421d891986aad5158bc8",  # Daisy (young female)
            "female_mature": "2d5b0e6cf36f460aa7fc47e3eee4ba54",  # Alice (mature female)
            "male_young": "e95166076b8c458abcd636a5f59b0e81",    # Daniel (young male)
            "male_mature": "11a8b3b5ea33441294501cb8fc45f3da",   # Matthew (mature male)
        },
        # Chinese voices
        "zh": {
            "female_young": "00c8fd447ad7480ab1785825978a2215",  # Using correct voice ID for female_young
            "female_mature": "5b3f164f63ee46b5bcb28e21e7f5427e",  # Luli (mature female)
            "male_young": "7a72eedf88374b65a2a3f873bd471d73",    # Xiaotong (young male)
            "male_mature": "e1adcef3cf42401b84b0fa5ea8b14b77",   # Zhigang (mature male)
        },
        # Spanish voices
        "es": {
            "female_young": "41a37ffe4f3742cd94fc9f0263c7d697",  # Sofia (young female)
            "female_mature": "2fb39c2a1df94fbab396a85f72b5e48b",  # Isabella (mature female)
            "male_young": "2d2d443a7bbb4663942c19f3ad5b025d",    # Miguel (young male)
            "male_mature": "e3f58532df7d4df79c1c7176a7fb3cd1",   # Javier (mature male)
        },
        # Japanese voices
        "ja": {
            "female_young": "3984e56f97204e98b51d26bef43e2c8f",  # Aiko (young female)
            "female_mature": "21cad0c84c5543bba5fd4fb31abd0078",  # Yumi (mature female)
            "male_young": "a2ad6ae9c3b64b47ba2423cefba33c9a",    # Takashi (young male)
            "male_mature": "b08c4f76ceb54e3295337bb78f0dc0c4",   # Kenji (mature male)
        },
        # Korean voices
        "ko": {
            "female_young": "aea35fae3a4640dbb107e23c71260b99",  # Ji-woo (young female)
            "female_mature": "5f4d8a8e33a44b8c814cb0b6e2197a2d",  # Seo-yeon (mature female)
            "male_young": "9dd9a7c8c4e44c6d8f1282a0f93d1acf",    # Min-jun (young male)
            "male_mature": "faf3431b55cf4a268a5f6f62f4063764",   # Joon-ho (mature male)
        },
        # French voices
        "fr": {
            "female_young": "ab14736db6e24d07b49c4bd75bee21d2",  # Chloé (young female)
            "female_mature": "1e6a91f6ea764eba9fc56a209c71f169",  # Sophie (mature female)
            "male_young": "74dc44e4df9e40ee8c4bb241391b27bb",    # Lucas (young male)
            "male_mature": "9fae597cc45b4fc39056a583a2ac18d9",   # Pierre (mature male)
        }
    }
    
    # Determine gender and age category based on avatar metadata if it's an avatar
    if character_type == "avatar" and character_id in avatar_options:
        gender = avatar_options[character_id]["gender"]
        age = avatar_options[character_id]["age"]
        voice_category = f"{gender}_{age}"
    else:
        # Default to female_young for talking photos or unknown avatars
        voice_category = "female_young"
    
    # Select appropriate voice based on language and avatar characteristics
    # If language not in our map, default to English
    if detected_language not in voice_map:
        if debug_mode:
            progress_placeholder.warning(
                f"Language '{detected_language}' not supported in voice map. Falling back to English.")
        detected_language = "en"  # Default to English

    # Get the voice ID
    voice_id = voice_map[detected_language][voice_category]
    progress_placeholder.info(f"Using voice ID: {voice_id} for detected language: {detected_language}")
    
    # Log the language detection and voice selection if debug mode is enabled
    if debug_mode:
        language_name = LANGUAGE_NAMES.get(detected_language, detected_language)
        progress_placeholder.info(f"Debug Info: Detected language: {language_name}, Voice category: {voice_category}, Voice ID: {voice_id}")
    
    # Updated payload structure based on character type
    if character_type == "avatar":
        character_config = {
            "type": "avatar",
            "avatar_id": character_id,
            "avatar_style": "normal"
        }
    else:  # talking_photo type
        character_config = {
            "type": "talking_photo",
            "talking_photo_id": character_id
        }
    
    # Updated payload structure for v2 API
    payload = {
        "video_inputs": [
            {
                "character": character_config,
                "voice": {
                    "type": "text",
                    "input_text": text,
                    "voice_id": voice_id
                },
                "background": {
                    "type": "color",
                    "value": "#ffffff"  # White background
                }
            }
        ],
        "dimension": {
            "width": 720,  # Lower resolution for free tier
            "height": 406   # 16:9 aspect ratio
        },
        "test": True,  # Enable test mode for the free tier
        "title": "Avatar Chat Video"  # Add a title to the video
    }
    
    # Debug logging if enabled
    if debug_mode:
        st.sidebar.subheader("API Request Debug")
        st.sidebar.code(json.dumps(payload, indent=2), language="json")
    
    try:
        # Try v2 API first
        progress_placeholder.info("Sending request to HeyGen API...")
        response = requests.post(f"{HEYGEN_API_URL}/video/generate", 
                                headers=headers, 
                                data=json.dumps(payload))
        
        # If v2 fails, try v1 endpoint
        if response.status_code != 200:
            progress_placeholder.info("Trying alternative API endpoint...")
            # Log the error if debug mode is enabled
            if debug_mode:
                try:
                    error_json = response.json()
                    st.sidebar.warning("V2 API Error Response:")
                    st.sidebar.code(json.dumps(error_json, indent=2), language="json")
                except:
                    st.sidebar.warning(f"V2 API Error: {response.text}")
            
            # Create v1 payload with proper structure based on character type
            if character_type == "avatar":
                v1_payload = {
                    "avatar_id": character_id,
                    "avatar_style": "normal",
                    "voice_type": "text",
                    "voice_input": text,
                    "voice_id": voice_id,
                    "background": "#ffffff",
                    "test": True,
                    "title": "Avatar Chat Response"
                }
            else:  # talking_photo type
                v1_payload = {
                    "talking_photo_id": character_id,
                    "voice_type": "text",
                    "voice_input": text,
                    "voice_id": voice_id,
                    "background": "#ffffff",
                    "test": True,
                    "title": "Talking Photo Response"
                }
            
            # Log the v1 payload if debug mode is enabled
            if debug_mode:
                st.sidebar.info("Trying V1 API with payload:")
                st.sidebar.code(json.dumps(v1_payload, indent=2), language="json")
                
            # Make the v1 API call with proper headers and using json parameter
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Api-Key": HEYGEN_API_KEY
            }
            response = requests.post(
                "https://api.heygen.com/v1/video.task", 
                headers=headers, 
                json=v1_payload  # Use json parameter instead of data
            )
            
        if response.status_code != 200:
            # Handle error response properly
            error_message = "Unknown error"
            try:
                # Try to parse the error JSON
                error_json = response.json()
                if "error" in error_json and error_json["error"]:
                    if isinstance(error_json["error"], dict) and "message" in error_json["error"]:
                        error_message = f"Error: {error_json['error']['message']}"
                        if "detail" in error_json["error"]:
                            error_message += f" - {error_json['error']['detail']}"
                    else:
                        error_message = f"Error: {error_json['error']}"
                elif "message" in error_json:
                    error_message = f"Error: {error_json['message']}"
            except:
                # If we can't parse JSON, use the raw text
                error_message = f"Error creating video (HTTP {response.status_code}): {response.text}"
            
            st.error(error_message)
            if debug_mode:
                st.sidebar.error("API Error Details:")
                st.sidebar.code(response.text, language="json")
            return None
        
        # Handle different response formats between v1 and v2
        response_json = response.json()
        
        # v1 API returns data with task_id, v2 returns data with video_id
        if "task_id" in response_json.get("data", {}):
            video_id = response_json.get("data", {}).get("task_id")
        else:
            video_id = response_json.get("data", {}).get("video_id")
            
        if not video_id:
            st.error("Failed to get video ID")
            return None
            
        # Log the video ID for debugging
        progress_placeholder.info(f"Video ID: {video_id}")
        
        # Check video status and wait for completion
        status = "pending"
        attempt_count = 0
        max_attempts = 200  # Increased to 10 minutes (3 sec × 200)
        
        with st.spinner(""):
            while status in ["pending", "processing", "waiting"]:
                # Update progress info
                progress_percent = min(90, attempt_count * 0.45)  # Slower progress to reflect longer wait
                progress_bar.progress(int(progress_percent))
                progress_placeholder.info(f"Generating video: {progress_percent:.0f}% complete (this may take 5-10 minutes)")
                
                time.sleep(3)  # Check every 3 seconds
                attempt_count += 1
                
                # Modified status check for consistent endpoint handling
                try:
                    # First try v1 endpoint - most reliable for status checks
                    status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
                    status_response = requests.get(status_url, headers=headers)
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json().get("data", {})
                        status = status_data.get("status")
                        
                        # Show more detailed status info if debug mode is enabled
                        if debug_mode:
                            st.sidebar.info(f"Status check response:")
                            st.sidebar.code(json.dumps(status_response.json(), indent=2), language="json")
                        
                        progress_placeholder.info(f"Generating video: {progress_percent:.0f}% complete - Status: {status} (attempt {attempt_count}/{max_attempts})")
                        
                        if status == "completed":
                            video_url = status_data.get("video_url")
                            progress_bar.progress(100)
                            progress_placeholder.success("Video generation complete!")
                            return video_url
                        elif status == "failed":
                            error_details = status_data.get("error", {})
                            if isinstance(error_details, dict):
                                error_message = error_details.get("message", "Unknown error")
                                error_detail = error_details.get("detail", "")
                                error_code = error_details.get("code", "")
                                error_text = f"Video generation failed: {error_message}"
                                if error_detail:
                                    error_text += f". {error_detail}"
                                if error_code:
                                    error_text += f" (Code: {error_code})"
                            else:
                                error_text = f"Video generation failed: {error_details}"
                            
                            progress_placeholder.error(error_text)
                            if debug_mode:
                                st.sidebar.error("Error details:")
                                st.sidebar.code(json.dumps(error_details, indent=2), language="json")
                            return None
                    else:
                        # Try v2 endpoint as fallback
                        status_url = f"https://api.heygen.com/v2/video_status.get?video_id={video_id}"
                        status_response = requests.get(status_url, headers=headers)
                        
                        if status_response.status_code == 200:
                            try:
                                status_data = status_response.json().get("data", {})
                                status = status_data.get("status")
                                
                                # Show more detailed status info if debug mode is enabled
                                if debug_mode:
                                    st.sidebar.info(f"V2 Status check response:")
                                    st.sidebar.code(json.dumps(status_response.json(), indent=2), language="json")
                                
                                progress_placeholder.info(f"Generating video: {progress_percent:.0f}% complete - Status: {status} (attempt {attempt_count}/{max_attempts})")
                                
                                if status == "completed":
                                    video_url = status_data.get("video_url")
                                    progress_bar.progress(100)
                                    progress_placeholder.success("Video generation complete!")
                                    return video_url
                                elif status == "failed":
                                    error_details = status_data.get("error", {})
                                    if isinstance(error_details, dict):
                                        error_message = error_details.get("message", "Unknown error")
                                        error_detail = error_details.get("detail", "")
                                        error_code = error_details.get("code", "")
                                        error_text = f"Video generation failed: {error_message}"
                                        if error_detail:
                                            error_text += f". {error_detail}"
                                        if error_code:
                                            error_text += f" (Code: {error_code})"
                                    else:
                                        error_text = f"Video generation failed: {error_details}"
                                    
                                    progress_placeholder.error(error_text)
                                    if debug_mode:
                                        st.sidebar.error("Error details:")
                                        st.sidebar.code(json.dumps(error_details, indent=2), language="json")
                                    return None
                            except Exception as parse_error:
                                progress_placeholder.warning(f"Could not parse V2 status response: {parse_error}")
                                if debug_mode:
                                    st.sidebar.warning(f"V2 status response parsing error: {parse_error}")
                                    st.sidebar.code(status_response.text, language="json")
                except Exception as e:
                    # If we can't connect, don't fail - just continue checking
                    progress_placeholder.info(f"Waiting for video processing... (attempt {attempt_count}/{max_attempts})")
            
            # Continue checking even if we reach max attempts - don't give up!
            if attempt_count >= max_attempts:
                # Show a message but don't terminate - just keep checking
                progress_placeholder.info("Still waiting for video generation... (It can take up to 15 minutes)")
                
                # Check status again
                try:
                    status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
                    status_response = requests.get(status_url, headers=headers)
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json().get("data", {})
                        status = status_data.get("status")
                        
                        # If video is still processing, reset counter to keep checking
                        if status in ["pending", "processing", "waiting"]:
                            attempt_count = 0  # Reset counter to keep checking
                            max_attempts = 200  # Another 10 minutes
                        
                        # If completed, return the URL
                        if status == "completed":
                            video_url = status_data.get("video_url")
                            progress_bar.progress(100)
                            progress_placeholder.success("Video generation complete!")
                            return video_url
                except:
                    # If error, just log it
                    pass
                
                # If we still can't get the video, provide a way for user to check HeyGen dashboard
                progress_placeholder.warning("Video taking longer than expected.")
                # Return the video ID so the user has something to reference
                return None
                    
        return None
    except Exception as e:
        st.error(f"Error with API: {e}")
        return None

# Chat interface
user_input = st.chat_input("Type your message here...")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.write(message["content"])
        else:
            if "video_url" in message and message["video_url"]:
                st.video(message["video_url"])
            st.write(message["content"])

# Process new user input
if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display the user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get LLM response
    llm_response = get_llm_response(user_input)
    
    if llm_response:
        # Create assistant message container first
        assistant_container = st.chat_message("assistant")
        assistant_container.write(llm_response)
        
        # Detect language and show info
        detected_language = detect_language(llm_response)
        language_name = LANGUAGE_NAMES.get(detected_language, detected_language)
        
        # Show video generation status
        video_status = assistant_container.empty()
        video_status.info(f"Generating avatar video in {language_name}... (please wait 5-10 minutes)")
        
        # Generate video with the response (happens in background)
        video_url = generate_heygen_video(
            selected_character,
            llm_response,
            selected_character_type  # Pass the character type
        )
        
        # Update the response with the video
        if video_url:
            video_status.empty()
            assistant_container.video(video_url)
        else:
            # Show error message with troubleshooting info
            video_status.error(
                f"Video generation failed. Possible reasons: "
                f"1) The voice may not support {language_name} text. "
                f"2) API rate limit exceeded. "
                f"3) Service unavailable. Try English instead."
            )
            
            # Add a refresh button
            if st.button("Check for video again"):
                st.rerun()
        
        # Store in session state
        st.session_state.messages.append({
            "role": "assistant", 
            "content": llm_response,
            "video_url": video_url if video_url else None
        })