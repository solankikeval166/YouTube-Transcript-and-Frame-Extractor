# YouTube Transcript and Quote Extractor

This application allows users to fetch YouTube video transcripts and extract quotes from them based on timestamps. The application uses the `youtube_transcript_api` to get transcripts and the `GoogleGenerativeAI` model to extract structured quotes along with their start and end times.

## Features:
- Fetch YouTube video transcripts in JSON format.
- Extract quotes from transcripts along with start and end timestamps.
- Sort quotes by their timestamp.
- Display the extracted quotes on the web interface.

## Requirements

Before running the application, make sure you have the following installed:
- Python 3.x (preferably 3.10 or later)
- Google API Key for `GoogleGenerativeAI`
- Required Python packages (listed below)

### Install Required Packages

Clone the repository or create a new directory for this project. Then, create a virtual environment (optional but recommended), and install the dependencies:

1. Clone the repository (or download the script):
    ```bash
    git clone https://github.com/solankikeval166/Youtube-Transcriber-and-Quote-Extractor.git
    
    cd YouTube-Transcript-Extractor
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    
    source venv/bin/activate  # For macOS/Linux
    
    .\venv\Scripts\activate   # For Windows
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Setup Google API Key

To use the **GoogleGenerativeAI** model for quote extraction, you need to set up your own Google API key.

1. Create a Google Cloud project and enable the [Google Generative AI API](https://ai.google.dev/gemini-api/docs/api-key).
2. Create API credentials (API key).
3. Enter your API key in the app interface when prompted.

## Running the Application

To start the application:

1. Make sure you have the required dependencies installed.
2. Run the following command to launch the Streamlit app:
    ```bash
    streamlit run app.py
    ```

3. Open the application in your browser at:
    ```
    http://localhost:8501
    ```

### Streamlit App Interface

- **GEMINI API Key**: Enter your GEMINI API key to extract quotes from transcripts.
- **YouTube URLs**: Enter YouTube video URLs (one per line) for which you want to fetch transcripts and extract quotes.
- **Fetch Transcripts and Extract Quotes**: Click this button to:
  - Fetch the transcripts for the provided YouTube URLs.
  - Extract quotes based on the timestamps from the transcripts.
  - Display the quotes sorted by their timestamps.

## How It Works

1. **Enter YouTube URLs**: Paste one or more YouTube video URLs (one per line).
2. **Fetch Transcripts**: The application will fetch the video transcripts from YouTube using the `youtube_transcript_api`.
3. **Extract Quotes**: The transcript is analyzed, and relevant quotes are extracted based on the context in the video. The start and end times of each quote are also provided.

## Example

### Example URL:

You can use the following sample YouTube URL for testing:
https://www.youtube.com/watch?v=XHAV87e0hLY

