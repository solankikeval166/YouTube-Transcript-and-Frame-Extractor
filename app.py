import os
import json
import warnings
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api import TranscriptsDisabled, VideoUnavailable, NoTranscriptFound
from pytube import Playlist  # Import Playlist from pytube

# Setup environment
warnings.filterwarnings("ignore")

# Streamlit App Layout
st.title("YouTube Transcript and Frame Extractor")

# Input field for GEMINI API Key
st.subheader("Enter Your GEMINI API Key")
GOOGLE_API_KEY = st.text_input("GEMINI API Key", type="password")

# Select between individual video URL or playlist URL
st.subheader("Choose Input Type")
input_type = st.radio("Select URL Type", ("Playlist", "Individual Video"))

# Input field for YouTube URLs
if input_type == "Individual Video":
    st.subheader("Enter YouTube Video URLs")
    urls_input = st.text_area("Paste YouTube URLs (one per line)")
else:
    st.subheader("Enter YouTube Playlist URL")
    playlist_url_input = st.text_input("Paste Playlist URL")

# Input field for the user's question
st.subheader("Ask a Question Regarding the Transcript")
user_question = st.text_input("Enter your question here...")

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
        print("The video is unavailable.")
    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        pass
        print("No transcript available for this video.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

# Function to load transcripts and convert them to text


def change_transcript_to_txt(file_name):
    try:
        with open(file_name, 'r') as file:
            transcript = json.load(file)

        text_content = ""
        for entry in transcript:
            if '[Music]' not in entry['text']:  # Skip '[Music]' entries
                start = round(entry['start'], 2)
                end = round(entry['start'] + entry['duration'], 2)
                text_content += f"Text: {entry['text']}, Start: {start}, End: {end}\n"

        return text_content

    except FileNotFoundError:
        st.error(f"The file {file_name} does not exist.")
    except json.JSONDecodeError:
        st.error(
            f"Error decoding the JSON file {file_name}. It may be corrupted.")
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
            text = str(file_path) + "\n"
            text += change_transcript_to_txt(file_path)
            transcripts += text + "\n"
    return transcripts


def relevant_text_extractor(question, transcript):
    if not GOOGLE_API_KEY:
        st.warning("Please provide a valid GEMINI API Key.")
        return []

    task_decomposer = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.5,
        api_key=GOOGLE_API_KEY
    )

    template = f"""
                You are an expert AI assistant specializing in extracting and structuring specific text segments from user-provided video transcripts.
                Your primary task is to extract relevant parts of the transcript that directly answer or relate to the user's question, along with their corresponding timeframes. 
                Your output must strictly follow the provided JSON format.

                - Instructions:
                    - Analyze the provided transcript thoroughly.
                    - Identify and extract text segments that are most relevant to the user's question, preserving their exact wording.
                    - Include the start and end times for each extracted segment as specified in the transcript.
                
                - Output Format:
                    - The response must be in this JSON structure:
                        - "transcript_id": "The transcript identifier associated with transcript at the beginning of every new transcript in this format './transcripts/transcript_1.json' Please use only transcript_1 as identifier."
                        - "relevant_text": "Extracted text from the transcript.",
                        - "start": "Timestamp indicating when the text begins.",
                        - "end": "Timestamp indicating when the text ends." 
                
                - Guidelines:
                    - If multiple relevant segments are found, include each as a separate JSON object in a list.
                    - Do not include any explanations, commentary, or additional information outside the JSON structure.
                    - Ensure timeframes (start and end) align precisely with the transcript's timestamps.
                    
                - Input:
                - Transcript:
                    - {transcript}
                
                - User's Question:
                    - {question}
                """

    prompt = PromptTemplate(template=template, input_variables=[
                            "question", "transcript"])

    requirements_chain = prompt | task_decomposer

    result = requirements_chain.invoke(
        {"question": question, "transcript": transcript})

    # print(type(result))

    # with open("file.txt", "w") as f:
    #     f.write(result)

    try:
        # frames = result
        frames = json.loads(result[8:-4])

        for frame in frames:
            # Extract the numeric part of the start time and convert to float
            frame['start'] = float(frame['start'].replace('s', ''))
            frame['end'] = float(frame['end'].replace('s', ''))

        sorted_frames = sorted(frames, key=lambda x: x['start'])

        return sorted_frames
    except Exception as e:
        print(f"Error extracting relevant text: No data received from the model.")
        return []

# Function to fetch all video URLs from a playlist using pytube


def fetch_playlist_urls(playlist_url):
    try:
        playlist = Playlist(playlist_url)
        return playlist.video_urls
    except Exception as e:
        st.error(f"Error fetching playlist: {e}")
        return []


# Button to process URLs
if st.button("Fetch Transcripts and Extract Frames"):
    if input_type == "Playlist":
        # Process playlist URLs
        if playlist_url_input.strip():
            if GOOGLE_API_KEY:  # Check if API Key is provided
                video_urls = fetch_playlist_urls(playlist_url_input)
                if video_urls:
                    final_transcripts = ""
                    count = 1
                    for url in video_urls:
                        filename = fetch_transcript(url, count)
                        if filename:
                            # st.write(f"Transcript saved as {filename}")
                            final_transcripts += change_transcript_to_txt(
                                filename)
                            count += 1

                    if final_transcripts:
                        if user_question.strip():
                            st.subheader(f"Answer to: {user_question}")
                            frames = relevant_text_extractor(
                                user_question, final_transcripts)
                            if frames:
                                for frame in frames:
                                    st.write(
                                        f"**Trnascript_id:** {frame['transcript_id']}")
                                    st.write(
                                        f"**Frame:** {frame['relevant_text']}")
                                    st.write(
                                        f"**Start Time:** {frame['start']} s")
                                    st.write(f"**End Time:** {frame['end']} s")
                                    st.write("---")
                            else:
                                st.warning(
                                    "No frames extracted for the given question.")
                        else:
                            st.warning(
                                "Please enter a question to extract frames.")
                    else:
                        st.warning(
                            "No transcripts available for the given playlist.")
                else:
                    st.warning("No videos found in the playlist.")
            else:
                st.warning("Please enter a GEMINI API Key to proceed.")
        else:
            st.warning("Please enter a YouTube playlist URL.")

    elif input_type == "Individual Video":
        # Process individual URLs
        if urls_input.strip():
            if GOOGLE_API_KEY:  # Check if API Key is provided
                urls = urls_input.split("\n")
                final_transcripts = ""
                count = 1
                for url in urls:
                    filename = fetch_transcript(url, count)
                    if filename:
                        # st.write(f"Transcript saved as {filename}")
                        final_transcripts += change_transcript_to_txt(filename)
                        count += 1

                if final_transcripts:
                    if user_question.strip():
                        st.subheader(f"Answer to: {user_question}")
                        frames = relevant_text_extractor(
                            user_question, final_transcripts)
                        if frames:
                            for frame in frames:
                                st.write(
                                    f"**Trnascript_id:** {frame['transcript_id']}")
                                st.write(
                                    f"**Frame:** {frame['relevant_text']}")
                                st.write(f"**Start Time:** {frame['start']} s")
                                st.write(f"**End Time:** {frame['end']} s")
                                st.write("---")
                        else:
                            st.warning(
                                "No frames extracted for the given question.")
                    else:
                        st.warning(
                            "Please enter a question to extract frames.")
                else:
                    st.warning("No transcripts available for the given URLs.")
            else:
                st.warning("Please enter a GEMINI API Key to proceed.")
        else:
            st.warning("Please enter at least one YouTube URL.")