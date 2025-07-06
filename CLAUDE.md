# Avatar Education Project Knowledge Base

This document contains Claude's knowledge about the Avatar Education project codebase.

## Project Overview

The Avatar Education project consists of two main applications:
1. **Avatar Generation Dashboard** (`avatar_generation.py`) - Create and manage AI avatars
2. **Multilingual Chat Interface** (`chat_multilingual.py`) - Chat with avatars in multiple languages

## File: avatar_generation.py

### Purpose
A Streamlit web application for creating and managing AI avatars using HeyGen's API.

### Key Features
- **Password Protection**: Simple authentication with password "chatbot"
- **Avatar Search**: Find existing avatars with recent avatars display (top 3)
- **Photo Training**: Upload photos to create talking avatars
- **AI Generation**: Generate avatar photos using AI with custom attributes
- **Multi-step Workflows**: Guided processes for avatar creation

### Main Functions

#### API Helper Functions
- `get_headers()` - Standard API headers for HeyGen requests
- `get_upload_headers(content_type)` - Headers for file uploads
- `check_api_key_valid()` - Validates HeyGen API key

#### Avatar Management
- `get_recent_avatars(limit=3)` - Gets most recently created avatars, sorted by group creation timestamp
- `search_avatars(search_term)` - Searches avatars by name across all groups
- `upload_asset(file, file_type)` - Uploads files to HeyGen's asset storage

#### AI Avatar Generation
- `generate_photo_avatar(avatar_attributes)` - Creates AI-generated avatar photos
  - **Fixed Issue**: Added required `name` field to API payload
  - Requires: name, age, gender, ethnicity, orientation, pose, style, appearance
- `check_photo_generation_status(generation_id)` - Polls generation progress

#### Photo Training Workflow
- `create_avatar_group(name, image_key, generation_id=None)` - Creates avatar groups
- `train_avatar_group(group_id)` - Starts avatar training process
- `check_training_status(group_id)` - Monitors training progress

#### UI Management
- `set_page(page)` - Navigation between app sections
- `reset_avatar_creation_state()` - Clears session state
- `get_image_download_link(img_url, filename)` - Creates download links

### App Structure

#### Navigation Pages
1. **Home** - Dashboard overview and quick navigation
2. **Search Avatars** - Recent avatars + search functionality
3. **Train Photo into Talking Avatar** - 3-step upload and training process
4. **Generate Photo with AI** - 2-step AI generation and download

#### Session State Variables
- Authentication, navigation, avatar IDs, file uploads, training status, generation progress

### API Endpoints Used
- `GET /v2/avatar_group.list` - List avatar groups
- `GET /v2/avatar_group/{group_id}/avatars` - Get avatars in group
- `POST /v1/asset` - Upload files
- `POST /v2/photo_avatar/photo/generate` - Generate AI photos
- `GET /v2/photo_avatar/generation/{generation_id}` - Check generation status
- `POST /v2/photo_avatar/avatar_group/create` - Create avatar groups
- `POST /v2/photo_avatar/train` - Start training
- `GET /v2/photo_avatar/train/status/{group_id}` - Check training status

### Recent Fixes
1. **AI Generation Error**: Added missing `name` field to photo generation API payload
2. **Search Issue**: Fixed avatar search to search individual avatars by name instead of filtering by group names
3. **Recent Avatars**: Implemented proper sorting by group creation timestamp

## File: chat_multilingual.py

### Purpose
A Streamlit chat interface that generates videos of avatars speaking responses in multiple languages.

### Key Features
- **Authentication**: Password protection ("chatbot")
- **Multilingual Support**: 12+ languages with appropriate voice selection
- **Dual Character Types**: Video avatars and talking photos
- **AI Integration**: Claude (primary) with ChatGPT fallback
- **Real-time Video Generation**: HeyGen video creation with progress tracking

### Main Functions

#### AI Response Generation
- `get_llm_response(prompt)` - Primary Claude API integration
- `get_fallback_response(prompt)` - ChatGPT backup when Claude overloaded
- **Response Requirements**: 10-20 words, conversational, same language as input

#### Language Processing
- `detect_language(text)` - Detects Chinese, Japanese, Korean, Spanish, French, defaults to English
- Language-specific voice mapping by gender and age

#### Video Generation
- `generate_heygen_video(character_id, text, character_type)` - Core video creation
  - Progress tracking with visual feedback
  - Handles both avatar and talking_photo types
  - Automatic voice selection based on language/character
  - Robust error handling and retry logic

### Supported Languages & Voices
- **English**: Native voices optimized for English
- **Chinese, Spanish, French, Japanese, Korean**: Multilingual voices
- **Additional**: German, Italian, Portuguese, Russian, Hindi, Arabic

### Character Options

#### Video Avatars (8 total)
- **Female**: Angela (Young), Daisy (Mature), Natalie (Young), Amelia (Mature)
- **Male**: Daniel (Young), Ben (Mature), Alex (Young), Thomas (Mature)

#### Talking Photos (3 total)
- Girl, Professional Woman, Young Girl (using custom avatar IDs)

### API Integration
- **Claude**: claude-3-7-sonnet model with conversation history
- **OpenAI**: gpt-3.5-turbo as fallback
- **HeyGen**: v2/v1 API endpoints for video generation

### Voice ID Mapping
Complex voice selection system:
- Detects language of response text
- Maps to appropriate voice based on character gender/age
- Falls back to English if language not supported
- Includes 40+ voice IDs across languages and character types

### Error Handling
- API overload detection and fallback
- Multiple video generation endpoint attempts
- Extended timeout handling (up to 15 minutes)
- Comprehensive debug mode for troubleshooting

## Environment Variables Required
- `HEYGEN_API_KEY` - HeyGen API access
- `CLAUDE_API_KEY` - Anthropic Claude API
- `OPENAI_API_KEY` - OpenAI ChatGPT fallback

## Common Issues & Solutions
1. **Avatar Name Missing**: Ensure `name` field included in generation requests
2. **Search Not Working**: Search now properly filters individual avatars, not groups
3. **Video Generation Timeout**: Normal for HeyGen, can take 5-15 minutes
4. **Language Detection**: Uses character-based detection for Asian languages, keyword-based for European

## Recent Improvements
- Added recent avatars display (3 most recent by creation timestamp)
- Fixed avatar search to work by individual avatar names
- Enhanced debug logging for avatar creation process
- Improved voice selection logic for multilingual support