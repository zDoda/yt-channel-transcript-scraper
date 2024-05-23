from youtube_transcript_api import YouTubeTranscriptApi

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
        start_index = end_index  # Move past this occurrence
    return arr

# Example usage
filename = 'deya_youtube.htmml'
substring = '"videoIds":["'
videoIds = list(set(print_chars_after_substring(filename, substring)))

for videoId in videoIds:
    transcript = YouTubeTranscriptApi.get_transcript(videoId)
    transcript_arr = []
    for line in transcript:
        transcript_arr.append(line['text'])
    with open(f'deya_videoId_{videoId}.txt', 'w') as file:
        file.write(' '.join(transcript_arr))
