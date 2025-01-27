import os
import json
import warnings
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api import TranscriptsDisabled, VideoUnavailable, NoTranscriptFound

# Setup environment
warnings.filterwarnings("ignore")

# Streamlit App Layout
st.title("YouTube Transcript and Quote Extractor")

# Input field for GEMINI API Key
st.subheader("Enter Your GEMINI API Key")
GOOGLE_API_KEY = st.text_input("GEMINI API Key", type="password")

# Input field for YouTube URLs
st.subheader("Enter YouTube URLs")
urls_input = st.text_area("Paste YouTube URLs (one per line)")

# Function to fetch transcript from YouTube
def fetch_transcript(video_url, count):
    try:
        # Extract video ID from URL
        video_id = video_url.split('v=')[-1].split('&')[0]

        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Format the transcript into a JSON format
        formatter = JSONFormatter()
        formatted_transcript = formatter.format_transcript(transcript)

        # Ensure the transcripts folder exists
        if not os.path.exists('./transcripts'):
            os.makedirs('./transcripts')

        # Save the transcript to a JSON file with the video count as filename
        filename = f"./transcripts/transcript_{count}.json"
        with open(filename, "w") as file:
            file.write(formatted_transcript)

        return filename

    except VideoUnavailable:
        st.warning("The video is unavailable.")
    except TranscriptsDisabled:
        st.warning("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        st.warning("No transcript available for this video.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    return None

# Function to load transcripts and convert them to text
def change_transcript_to_txt(file_name):
    try:
        with open(file_name, 'r') as file:
            transcript = json.load(file)

        text_content = ""
        for entry in transcript:
            if '[Music]' not in entry['text']:  # Skip '[Music]' entries
                text_content += f"Text: {entry['text']}, Start: {entry['start']}, Duration: {entry['duration']}\n"

        return text_content

    except FileNotFoundError:
        st.error(f"The file {file_name} does not exist.")
    except json.JSONDecodeError:
        st.error(f"Error decoding the JSON file {file_name}. It may be corrupted.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

# Function to load all transcripts from the 'transcripts' folder
def load_transcripts():
    transcripts = ""
    file_names = os.listdir('./transcripts/')
    for file_name in file_names:
        if file_name.endswith('.json'):  # Only process JSON files
            file_path = os.path.join('./transcripts/', file_name)
            text = change_transcript_to_txt(file_path)
            transcripts += text
    return transcripts

# Function to extract quotes from the transcript
def quotes_extractor(transcript):
    if not GOOGLE_API_KEY:
        st.warning("Please provide a valid GEMINI API Key.")
        return []

    task_decomposer = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        format="json",
        api_key=GOOGLE_API_KEY
    )

    template = f"""
                  You are an AI assistant specializing in extracting and structuring quotes from user-provided video transcripts. 
                  Your primary task is to extract relevant quotes along with their corresponding timeframes. Ensure your response strictly adheres to the specified JSON format.

                  - Instructions:
                    - Analyze the provided transcript.
                    - Identify quotes based on the given context, preserving their exact wording.
                    - Include the start and end times for each quote from the transcript.
                    
                  - Output Format:
                    - json
                      - "quote": "Extracted quote from the transcript.",
                      - "start": "Timestamp indicating when the quote begins.",
                      - "end": "Timestamp indicating when the quote ends."

                  - Guidelines:
                  - Avoid adding explanations, commentary, or any information outside the JSON structure in your response.
                  - If no quotes are found, return an empty JSON object.
                  

                  - Input:
                    Here is the transcript:
                    {transcript}
                """

    prompt = PromptTemplate(template=template, input_variables=["transcript"])

    requirements_chain = prompt | task_decomposer

    result = requirements_chain.invoke({"transcript": transcript})

    quotes = json.loads(result[8:-4])

    for quote in quotes:
        # Extract the numeric part of the start time and convert to float
        quote['start'] = float(quote['start'].replace('s', ''))

    sorted_quotes = sorted(quotes, key=lambda x: x['start'])

    return sorted_quotes

# Button to process URLs
if st.button("Fetch Transcripts and Extract Quotes"):
    if urls_input.strip():
        if GOOGLE_API_KEY:  # Check if API Key is provided
            urls = urls_input.split("\n")
            final_transcripts = ""
            count = 1
            for url in urls:
                filename = fetch_transcript(url, count)
                if filename:
                    st.write(f"Transcript saved as {filename}")
                    final_transcripts += change_transcript_to_txt(filename)
                    count += 1

            if final_transcripts:
                st.subheader("Extracted Quotes:")
                quotes = quotes_extractor(final_transcripts)
                if quotes:
                    for quote in quotes:
                        st.write(f"**Quote:** {quote['quote']}")
                        st.write(f"**Start Time:** {quote['start']}s")
                        st.write(f"**End Time:** {quote['end']}s")
                        st.write("---")
                else:
                    st.warning("No quotes extracted.")
            else:
                st.warning("No transcripts available for the given URLs.")
        else:
            st.warning("Please enter a GEMINI API Key to proceed.")
    else:
        st.warning("Please enter at least one YouTube URL.")
