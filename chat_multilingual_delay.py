import streamlit as st
import requests
import json
import time
import os
import anthropic
import openai
from dotenv import load_dotenv
import threading
import queue
from datetime import datetime, timedelta
import uuid
import random

load_dotenv()

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
        st.stop()

# ==== NEW: QUEUE MANAGEMENT SYSTEM ====

# Initialize global queue for video generation requests
if "video_queue" not in st.session_state:
    st.session_state.video_queue = queue.Queue()

if "processing_requests" not in st.session_state:
    st.session_state.processing_requests = {}

if "user_session_id" not in st.session_state:
    st.session_state.user_session_id = str(uuid.uuid4())

# Rate limiting configuration
MAX_CONCURRENT_REQUESTS = 20  # Maximum concurrent video generations
REQUEST_DELAY = 3  # Minimum seconds between requests per user
GLOBAL_REQUEST_DELAY = 3  # Minimum seconds between any requests globally

# Track request timestamps for rate limiting
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = {}

if "global_last_request" not in st.session_state:
    st.session_state.global_last_request = datetime.min

class VideoRequest:
    def __init__(self, user_session_id, character_id, text, character_type, request_id=None):
        self.user_session_id = user_session_id
        self.character_id = character_id
        self.text = text
        self.character_type = character_type
        self.request_id = request_id or str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.status = "queued"
        self.result = None
        self.error = None

def can_make_request(user_session_id):
    """Check if user can make a new request based on rate limiting"""
    now = datetime.now()
    
    # Check global rate limit
    if now - st.session_state.global_last_request < timedelta(seconds=GLOBAL_REQUEST_DELAY):
        return False, "Please wait a moment before making another request"
    
    # Check user-specific rate limit
    if user_session_id in st.session_state.last_request_time:
        last_request = st.session_state.last_request_time[user_session_id]
        if now - last_request < timedelta(seconds=REQUEST_DELAY):
            wait_time = REQUEST_DELAY - (now - last_request).seconds
            return False, f"Please wait {wait_time} seconds before making another request"
    
    # Check concurrent request limit
    active_requests = sum(1 for req in st.session_state.processing_requests.values() 
                         if req.status == "processing")
    if active_requests >= MAX_CONCURRENT_REQUESTS:
        return False, "Server is busy. Your request will be queued."
    
    return True, ""

def add_staggered_delay():
    """Add a random delay to stagger requests"""
    delay = random.uniform(0.5, 2.0)  # Random delay between 0.5-2 seconds
    time.sleep(delay)

# ==== END QUEUE MANAGEMENT SYSTEM ====

# Main app content (only shown if authenticated)
st.write("Welcome! Feel free to switch to different avatars and start to chat.")
st.write("The assistant supports multiple languages with multilingual voices.")

# Show queue status if there are pending requests
active_requests = len([req for req in st.session_state.processing_requests.values() 
                      if req.status in ["queued", "processing"]])
if active_requests > 0:
    st.info(f"📊 Active video requests: {active_requests}")

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
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
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
    options=["Video Avatar", "Photo Avatar"],
    index=0,
    horizontal=True
)

# Replace your current avatar selection code with this conditional logic
if character_type == "Video Avatar":
    gender_selection = st.sidebar.radio(
        "Select Gender",
        options=["Female", "Male"],
        index=0,
        horizontal=True
    )

    if gender_selection == "Female":
        avatar_subset = female_avatars
    else:
        avatar_subset = male_avatars

    selected_character = st.sidebar.selectbox(
        "Choose Avatar", 
        options=list(avatar_subset.keys()),
        format_func=lambda x: avatar_subset[x]["display_name"]
    )
    selected_character_type = "avatar"
else:
    selected_character = st.sidebar.selectbox(
        "Choose Talking Photo", 
        options=list(talking_photo_options.keys()),
        format_func=lambda x: talking_photo_options[x]["display_name"]
    )
    selected_character_type = "talking_photo"

# Function to get LLM response using Claude API
def get_llm_response(prompt):
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
        st.session_state.api_messages.append({
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        })
        
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=150,
            system=system_prompt,
            messages=st.session_state.api_messages
        )
        
        assistant_response = response.content[0].text.strip()
        
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
        
        openai_messages = []
        
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
        
        for msg in st.session_state.api_messages:
            role = msg["role"]
            if role == "assistant" and len(openai_messages) == 1:
                continue
                
            content = msg["content"][0]["text"] if isinstance(msg["content"], list) else msg["content"]
            openai_messages.append({"role": role, "content": content})
        
        if openai_messages[-1]["role"] != "user" or openai_messages[-1]["content"] != prompt:
            openai_messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=openai_messages,
            max_tokens=150
        )
        
        response_text = response.choices[0].message.content.strip()
        
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

def detect_language(text):
    if any('\u4e00' <= char <= '\u9fff' for char in text):
        return "zh"
    
    if any('\u3040' <= char <= '\u30ff' for char in text):
        return "ja"
    
    if any('\uac00' <= char <= '\ud7a3' for char in text):
        return "ko"
    
    spanish_words = ["el", "la", "los", "las", "un", "una", "y", "o", "pero", "porque", "como", "qué", "cuándo", "dónde"]
    words = text.lower().split()
    if any(word in spanish_words for word in words) and any('á' in text or 'é' in text or 'í' in text or 'ó' in text or 'ú' in text or 'ñ' in text):
        return "es"
    
    french_words = ["le", "la", "les", "un", "une", "des", "et", "ou", "mais", "parce", "que", "comment", "quand", "où"]
    if any(word in french_words for word in words) and any('é' in text or 'è' in text or 'ê' in text or 'ç' in text or 'à' in text):
        return "fr"
    
    return "en"

def generate_heygen_video_with_queue(character_id, text, character_type="avatar"):
    """Enhanced video generation with queue management and rate limiting"""
    user_session_id = st.session_state.user_session_id
    
    # Check if user can make a request
    can_request, message = can_make_request(user_session_id)
    if not can_request:
        st.warning(message)
        return None
    
    # Update request timestamps
    now = datetime.now()
    st.session_state.last_request_time[user_session_id] = now
    st.session_state.global_last_request = now
    
    # Create request object
    video_request = VideoRequest(user_session_id, character_id, text, character_type)
    st.session_state.processing_requests[video_request.request_id] = video_request
    
    # Add staggered delay to prevent simultaneous API calls
    add_staggered_delay()
    
    # Create progress tracking elements
    progress_placeholder = st.empty()
    progress_bar = st.progress(0)
    progress_placeholder.info("Preparing to generate video...")
    
    # Update request status
    video_request.status = "processing"
    
    try:
        return generate_heygen_video_core(
            character_id, text, character_type, 
            progress_placeholder, progress_bar, 
            video_request
        )
    except Exception as e:
        video_request.status = "failed"
        video_request.error = str(e)
        st.error(f"Video generation failed: {e}")
        return None
    finally:
        # Clean up request from processing list
        if video_request.request_id in st.session_state.processing_requests:
            del st.session_state.processing_requests[video_request.request_id]

def generate_heygen_video_core(character_id, text, character_type, progress_placeholder, progress_bar, video_request):
    """Core video generation logic (same as original but with progress tracking)"""
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": HEYGEN_API_KEY
    }
    
    detected_language = detect_language(text)
    
    # Voice ID mapping by language and gender (same as original)
    voice_map = {
        "en": {
            "female_young": "1bd001e7e50f421d891986aad5158bc8",
            "female_mature": "2d5b0e6cf36f460aa7fc47e3eee4ba54",
            "male_young": "e95166076b8c458abcd636a5f59b0e81",
            "male_mature": "11a8b3b5ea33441294501cb8fc45f3da",
        },
        "zh": {
            "female_young": "00c8fd447ad7480ab1785825978a2215",
            "female_mature": "5b3f164f63ee46b5bcb28e21e7f5427e",
            "male_young": "7a72eedf88374b65a2a3f873bd471d73",
            "male_mature": "e1adcef3cf42401b84b0fa5ea8b14b77",
        },
        "es": {
            "female_young": "41a37ffe4f3742cd94fc9f0263c7d697",
            "female_mature": "2fb39c2a1df94fbab396a85f72b5e48b",
            "male_young": "2d2d443a7bbb4663942c19f3ad5b025d",
            "male_mature": "e3f58532df7d4df79c1c7176a7fb3cd1",
        },
        "ja": {
            "female_young": "3984e56f97204e98b51d26bef43e2c8f",
            "female_mature": "21cad0c84c5543bba5fd4fb31abd0078",
            "male_young": "a2ad6ae9c3b64b47ba2423cefba33c9a",
            "male_mature": "b08c4f76ceb54e3295337bb78f0dc0c4",
        },
        "ko": {
            "female_young": "aea35fae3a4640dbb107e23c71260b99",
            "female_mature": "5f4d8a8e33a44b8c814cb0b6e2197a2d",
            "male_young": "9dd9a7c8c4e44c6d8f1282a0f93d1acf",
            "male_mature": "faf3431b55cf4a268a5f6f62f4063764",
        },
        "fr": {
            "female_young": "ab14736db6e24d07b49c4bd75bee21d2",
            "female_mature": "1e6a91f6ea764eba9fc56a209c71f169",
            "male_young": "74dc44e4df9e40ee8c4bb241391b27bb",
            "male_mature": "9fae597cc45b4fc39056a583a2ac18d9",
        }
    }
    
    # Determine voice settings (same logic as original)
    if character_type == "avatar" and character_id in avatar_options:
        gender = avatar_options[character_id]["gender"]
        age = avatar_options[character_id]["age"]
        voice_category = f"{gender}_{age}"
    else:
        voice_category = "female_young"
    
    if detected_language not in voice_map:
        if debug_mode:
            progress_placeholder.warning(
                f"Language '{detected_language}' not supported in voice map. Falling back to English.")
        detected_language = "en"

    voice_id = voice_map[detected_language][voice_category]
    progress_placeholder.info(f"Using voice ID: {voice_id} for detected language: {detected_language}")
    
    # Create payload (same logic as original)
    if character_type == "avatar":
        character_config = {
            "type": "avatar",
            "avatar_id": character_id,
            "avatar_style": "normal"
        }
    else:
        character_config = {
            "type": "talking_photo",
            "talking_photo_id": character_id
        }
    
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
                    "value": "#ffffff"
                }
            }
        ],
        "dimension": {
            "width": 720,
            "height": 406
        },
        "test": True,
        "title": "Avatar Chat Video"
    }
    
    try:
        progress_placeholder.info("Sending request to HeyGen API...")
        
        # Add exponential backoff for failed requests
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = requests.post(f"{HEYGEN_API_URL}/video/generate", 
                                        headers=headers, 
                                        data=json.dumps(payload),
                                        timeout=30)
                break
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    progress_placeholder.warning(f"Request timeout. Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                else:
                    raise
        
        # Handle response (same logic as original but with enhanced error handling)
        if response.status_code != 200:
            # Try v1 API if v2 fails
            progress_placeholder.info("Trying alternative API endpoint...")
            
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
            else:
                v1_payload = {
                    "talking_photo_id": character_id,
                    "voice_type": "text",
                    "voice_input": text,
                    "voice_id": voice_id,
                    "background": "#ffffff",
                    "test": True,
                    "title": "Talking Photo Response"
                }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Api-Key": HEYGEN_API_KEY
            }
            
            response = requests.post(
                "https://api.heygen.com/v1/video.task", 
                headers=headers, 
                json=v1_payload,
                timeout=30
            )
            
        if response.status_code != 200:
            error_message = "Unknown error"
            try:
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
                error_message = f"Error creating video (HTTP {response.status_code}): {response.text}"
            
            video_request.status = "failed"
            video_request.error = error_message
            st.error(error_message)
            return None
        
        # Get video ID and poll for completion (same logic as original)
        response_json = response.json()
        
        if "task_id" in response_json.get("data", {}):
            video_id = response_json.get("data", {}).get("task_id")
        else:
            video_id = response_json.get("data", {}).get("video_id")
            
        if not video_id:
            video_request.status = "failed"
            video_request.error = "Failed to get video ID"
            st.error("Failed to get video ID")
            return None
            
        progress_placeholder.info(f"Video ID: {video_id}")
        
        # Enhanced status checking with better error handling
        status = "pending"
        attempt_count = 0
        max_attempts = 200
        
        with st.spinner(""):
            while status in ["pending", "processing", "waiting"]:
                progress_percent = min(90, attempt_count * 0.45)
                progress_bar.progress(int(progress_percent))
                progress_placeholder.info(f"Generating video: {progress_percent:.0f}% complete (this may take 5-10 minutes)")
                
                # Add jitter to polling interval to reduce server load
                poll_interval = 3 + random.uniform(-0.5, 0.5)
                time.sleep(poll_interval)
                attempt_count += 1
                
                try:
                    status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
                    status_response = requests.get(status_url, headers=headers, timeout=10)
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json().get("data", {})
                        status = status_data.get("status")
                        
                        progress_placeholder.info(f"Generating video: {progress_percent:.0f}% complete - Status: {status} (attempt {attempt_count}/{max_attempts})")
                        
                        if status == "completed":
                            video_url = status_data.get("video_url")
                            progress_bar.progress(100)
                            progress_placeholder.success("Video generation complete!")
                            video_request.status = "completed"
                            video_request.result = video_url
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
                            
                            video_request.status = "failed"
                            video_request.error = error_text
                            progress_placeholder.error(error_text)
                            return None
                    else:
                        # Try v2 endpoint as fallback (same logic as original)
                        status_url = f"https://api.heygen.com/v2/video_status.get?video_id={video_id}"
                        status_response = requests.get(status_url, headers=headers, timeout=10)
                        
                        if status_response.status_code == 200:
                            try:
                                status_data = status_response.json().get("data", {})
                                status = status_data.get("status")
                                
                                progress_placeholder.info(f"Generating video: {progress_percent:.0f}% complete - Status: {status} (attempt {attempt_count}/{max_attempts})")
                                
                                if status == "completed":
                                    video_url = status_data.get("video_url")
                                    progress_bar.progress(100)
                                    progress_placeholder.success("Video generation complete!")
                                    video_request.status = "completed"
                                    video_request.result = video_url
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
                                    
                                    video_request.status = "failed"
                                    video_request.error = error_text
                                    progress_placeholder.error(error_text)
                                    return None
                            except Exception as parse_error:
                                progress_placeholder.warning(f"Could not parse V2 status response: {parse_error}")
                except Exception as e:
                    # If we can't connect, don't fail - just continue checking
                    progress_placeholder.info(f"Waiting for video processing... (attempt {attempt_count}/{max_attempts})")
                    # Add exponential backoff for connection errors
                    time.sleep(min(10, 2 ** (attempt_count // 20)))
            
            # Handle timeout scenario
            if attempt_count >= max_attempts:
                progress_placeholder.warning("Video taking longer than expected.")
                video_request.status = "timeout"
                video_request.error = "Video generation timed out"
                
                # One final status check
                try:
                    status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
                    status_response = requests.get(status_url, headers=headers, timeout=10)
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json().get("data", {})
                        status = status_data.get("status")
                        
                        if status == "completed":
                            video_url = status_data.get("video_url")
                            progress_bar.progress(100)
                            progress_placeholder.success("Video generation complete!")
                            video_request.status = "completed"
                            video_request.result = video_url
                            return video_url
                except:
                    pass
                
                return None
                    
        return None
    except Exception as e:
        video_request.status = "failed"
        video_request.error = str(e)
        st.error(f"Error with API: {e}")
        return None

# Wrapper function to maintain compatibility with existing code
def generate_heygen_video(character_id, text, character_type="avatar"):
    """Main video generation function with enhanced queue management"""
    return generate_heygen_video_with_queue(character_id, text, character_type)

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
        
        # Generate video with the response (happens with queue management)
        video_url = generate_heygen_video(
            selected_character,
            llm_response,
            selected_character_type
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
                f"3) Service unavailable. Try English instead. "
                f"4) Server is busy - try again in a few minutes."
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

# Add a status dashboard in the sidebar for admin monitoring
if debug_mode:
    st.sidebar.subheader("🔧 System Status")
    
    # Show current active requests
    active_requests = [req for req in st.session_state.processing_requests.values() 
                      if req.status in ["queued", "processing"]]
    
    st.sidebar.metric("Active Requests", len(active_requests))
    
    # Show recent request history
    if st.session_state.processing_requests:
        st.sidebar.subheader("Recent Requests")
        for req_id, req in list(st.session_state.processing_requests.items())[-5:]:
            status_color = {
                "completed": "🟢",
                "failed": "🔴", 
                "processing": "🟡",
                "queued": "⏳",
                "timeout": "🟠"
            }.get(req.status, "⚪")
            
            st.sidebar.text(f"{status_color} {req.status}")
    
    # Add manual controls
    st.sidebar.subheader("🎛️ Manual Controls")
    if st.sidebar.button("Clear Request History"):
        st.session_state.processing_requests = {}
        st.sidebar.success("Request history cleared!")
    
    if st.sidebar.button("Reset Rate Limits"):
        st.session_state.last_request_time = {}
        st.session_state.global_last_request = datetime.min
        st.sidebar.success("Rate limits reset!")

# Add user guidance
st.sidebar.subheader("💡 Usage Tips")
st.sidebar.info("""
**For smooth experience:**
- Wait for your video to complete before sending another message
- If the server is busy, your request will be queued
- Simpler sentences work better for non-English languages
- Try English if other languages fail
""")