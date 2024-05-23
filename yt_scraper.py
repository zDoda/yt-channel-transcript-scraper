from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
import os
# Ensure you have access to the Ollama library and it's correctly installed.
import ollama

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

channel_name = "deya"
filename = 'deya_youtube.htmml'
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
                    summary_file_path = f"{
                        os.path.splitext(file_path)[0]}_summary.txt"
                    # Write the summary to a new file
                    with open(summary_file_path, 'w', encoding='utf-8') as summary_file:
                        summary_file.write(summary)
                    print(f"Summary for {os.path.basename(file_path)} written to {
                          os.path.basename(summary_file_path)}")


def print_chars_after_substring(filename, substring, num_chars=11):
    with open(filename, 'r') as file:
        content = file.read()

    arr = []

    start_index = 0
    while True:
        start_index = content.find(substring, start_index)
        if start_index == -1:
            break
        start_index += len(substring)
        end_index = start_index + num_chars
        arr.append(content[start_index:end_index])
        start_index = end_index
    return list(set(arr))


def transcript_summary(videoIds: list):
    for videoId in videoIds:
        transcript = YouTubeTranscriptApi.get_transcript(videoId)
        transcript_arr = []
        for line in transcript:
            transcript_arr.append(line['text'])
        response = requests.get(f"https://www.youtube.com/watch?v={vidId}")
        soup = BeautifulSoup(response.content, "html.parser")

        # Get the title of the HTML document
        title = soup.title.string
        print(title[:-9])
        with open(f'vids/{title[:-9]}.txt', 'w') as file:
            file.write(' '.join(transcript_arr))


videoIds = print_chars_after_substring(filename, substring)
transcript_summary(videoIds)

# Call the function with your top-level directory
process_files_in_directory(directory_path)
