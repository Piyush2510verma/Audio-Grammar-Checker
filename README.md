# Audio-Grammar-Checker


This Streamlit app lets you upload an audio file (`.wav` or `.mp3`), transcribes it using **OpenAI's Whisper**, and evaluates your grammar using **Google Gemini**.

---

## 🚀 Features
- Upload `.wav` or `.mp3` files
- Transcription with Whisper ASR
- Grammar evaluation with Gemini (Google Generative AI)
- Grammar score out of 100
- Short feedback for improvement

---

## 📂 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/piyush2510verma/Audio-Grammar-Checker.git
   cd Audio-Grammar-Checker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:  
   Create a `.env` file in the project root directory and add:
   ```
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

4. **Run the app**:
   ```bash
   streamlit run shl.py
   ```


---

## 🧠 How It Works

1. **Transcription**: Whisper converts the uploaded audio into text.
2. **Grammar Evaluation**: Gemini analyzes the transcription and provides:
   - A grammar score (0-100)
   - Brief feedback for improvement

---



