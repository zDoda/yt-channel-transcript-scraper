from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import os
# Ensure you have access to the Ollama library and it's correctly installed.
import ollama
import requests
import re

# Define the directory path where your .txt files are stored
# Update this path to the top-level directory you want to process
directory_path = '/Users/czook/Github/deya_chatbot/vids'

# Function to call Ollama API using the library
prompt = '''
You are helping me summarizing the captions for my videos in a more readable format.
You are going to recieve a text file that has the closed captions of each of my videos,
I want you to rewrite all of these videos in markdown format.
Please include a video name based off the contents.
Please only output the markdown.
'''

substring = '"videoIds":["'


def get_summary(text):
    response = ollama.chat(
        model='llama3',  # Use the appropriate model for your needs
        messages=[
            {
                'role': 'system',
                'content': prompt,
            },
            {
                'role': 'user',
                'content': text,
            },
        ]
    )
    return response['message']['content']

# Function to process files in directories


def process_files_in_directory(directory_path):
    # Walk through the directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Check if the file ends with .txt
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)  # Full path to the file
                # Read the content of the file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Get the summary from Ollama
                    summary = get_summary(content)
                    # Create a new file name for the summary
                    summary_file_path = f"{os.path.splitext(file_path)[0]}_summary.txt"
                    # Write the summary to a new file
                    with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
                        summary_file.write(summary)
                    print(f"Summary for {os.path.basename(file_path)} written to {os.path.basename(summary_file_path)}")

def get_youtube_channel_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch page, status code: {response.status_code}")

def extract_video_id(html_content):
    video_ids = re.findall(r'"videoId":"(.*?)"', html_content)
    return list(set(video_ids))

def transcript_summary(videoIds: list):
    for videoId in videoIds:
        transcript = YouTubeTranscriptApi.get_transcript(videoId)
        transcript_arr = []
        for line in transcript:
            transcript_arr.append(line['text'])
        response = requests.get(f"https://www.youtube.com/watch?v={videoId}")
        soup = BeautifulSoup(response.content, "html.parser")

        # Get the title of the HTML document
        title = soup.title.string
        print(title[:-9])
        with open(f'vids/{title[:-10]}.txt', 'w') as file:
            file.write(' '.join(transcript_arr))


channel_url = 'https://www.youtube.com/watch?v=erLbbextvlY'
html_content = get_youtube_channel_html(channel_url)
video_ids = extract_video_id(html_content)
transcript_summary(video_ids)

# Call the function with your top-level directory
process_files_in_directory(directory_path)
