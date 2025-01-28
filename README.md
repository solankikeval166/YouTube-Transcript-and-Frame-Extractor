
# YouTube Transcript and Frame Extractor

This Streamlit-based application helps users fetch YouTube video transcripts and extract specific segments based on user queries. It uses `youtube_transcript_api` to fetch transcripts and the `GoogleGenerativeAI` model to extract relevant frames.

## Features

- Fetch transcripts from individual YouTube videos or playlists.
- Convert transcripts into human-readable text with timestamps.
- Use the **GoogleGenerativeAI** model to extract relevant frames (text segments) based on user queries.
- Display extracted frames along with their start and end times.

## Requirements

### Prerequisites

- Python 3.x (preferably 3.10 or later).
- A GEMINI API Key from Google Cloud for **GoogleGenerativeAI**.

### Install Required Python Packages

Follow these steps to set up the project:

1. Clone the repository or create a directory for the project:
    ```bash
    git clone https://github.com/your-username/YouTube-Transcript-Frame-Extractor.git
    cd YouTube-Transcript-Frame-Extractor
    ```

2. Create a virtual environment (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate      # macOS/Linux
    .\venv\Scripts\activate       # Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Setup GEMINI API Key

1. Create a Google Cloud project and enable the [Google Generative AI API](https://ai.google.dev/gemini-api/docs/api-key).
2. Generate an API key and save it securely.
3. Enter your GEMINI API Key in the application interface when prompted.

## Running the Application

Start the Streamlit app with the following command:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## Usage

### Interface Overview

1. **GEMINI API Key**: Enter your API key to enable Google Generative AI-based processing.
2. **Input Type**:
   - **Playlist**: Enter the URL of a YouTube playlist.
   - **Individual Video**: Paste one or more YouTube video URLs (one per line).
3. **Ask a Question**: Enter a question related to the content of the videos or playlist.
4. **Fetch Transcripts and Extract Frames**: Click the button to process the input and display relevant frames.

### Output

The app will display:
- The transcript segments related to your query.
- Timestamps for the start and end of each segment.
- The corresponding transcript file identifier.

## Example Workflow

1. Enter the URL of a YouTube video or playlist.
2. Input your GEMINI API Key.
3. Ask a question (e.g., "What are the key points about AI in this video?").
4. Click "Fetch Transcripts and Extract Frames."
5. Review the extracted text segments with timestamps.

## Notes

- If a transcript is unavailable for a video, the app will skip that video.
- Ensure your GEMINI API Key is valid and has sufficient quota for processing.

## Example Playlist URL for Testing

You can use the following example URL to test the application:
- Playlist: `https://www.youtube.com/playlist?list=PL0vfts4VzfNgUUEtEjxDVfh4iocVR3qIb`

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
