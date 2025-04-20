import streamlit as st
import librosa
import numpy as np
import os
import google.generativeai as genai
import tempfile
import whisper
import json
import re

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCgFeBOFoyIwIZuwzn-KgyIp7oXQP3q7aM"  # Replace with your actual Gemini API key
genai.configure(api_key=GEMINI_API_KEY)

# Load Whisper model once
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")  # Options: 'tiny', 'base', 'small', 'medium', 'large'

# Load and transcribe audio
def transcribe_audio(file_path, model):
    result = model.transcribe(file_path)
    return result["text"]

# Send transcription to Gemini for grammar scoring
def grammar_score_with_gemini(transcription):
    prompt = f"""
You are an English grammar evaluation expert.

Task:
- Analyze the following transcription of a spoken English audio.
- Score the speaker's grammar out of 100 based on correctness, fluency, clarity, and proper sentence structure.
- Also provide brief feedback (1-2 sentences) about what can be improved.

Transcription:              
\"\"\"{transcription}\"\"\"

Respond ONLY in JSON format like:
{{
  "grammar_score": <integer between 0 and 100>,
  "feedback": "<brief feedback>"
}}
"""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# ================== STREAMLIT APP ==================

st.set_page_config(page_title="Audio Grammar Checker", page_icon="🎵")
st.title("🎵 Audio Grammar Checker")
st.write("Upload an audio file (.wav or .mp3) to evaluate grammar based on transcription.")

# Upload audio file
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    suffix = ".wav" if uploaded_file.name.endswith(".wav") else ".mp3"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    with st.spinner("🔄 Loading Whisper model and transcribing..."):
        model = load_whisper_model()
        transcription = transcribe_audio(tmp_file_path, model)

    st.subheader("📄 Transcription")
    st.success(transcription)

    with st.spinner("🔎 Scoring grammar with Gemini..."):
        gemini_response = grammar_score_with_gemini(transcription)

    st.subheader("🎓 Grammar Evaluation")
    try:
        # Extract JSON part using regex
        match = re.search(r"\{.*\}", gemini_response, re.DOTALL)
        if match:
            gemini_data = json.loads(match.group())
            st.metric(label="Grammar Score", value=f"{gemini_data['grammar_score']} / 100")
            st.info(gemini_data['feedback'])
        else:
            raise ValueError("No valid JSON found in response.")
    except (json.JSONDecodeError, ValueError) as e:
        st.error("Failed to parse Gemini response. Here is the raw response:")
        st.code(gemini_response)
    except Exception as e:
        st.error(f"Unexpected error: {e}")

    # Clean up temp file
    os.remove(tmp_file_path)

# Sidebar
st.sidebar.title("About")
st.sidebar.info("This app uses OpenAI's Whisper for speech-to-text and Google's Gemini for grammar evaluation.")
st.sidebar.markdown("---")
