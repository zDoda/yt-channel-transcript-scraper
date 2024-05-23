from youtube_transcript_api import YouTubeTranscriptApi

transcript = YouTubeTranscriptApi.get_transcript('vtj4f4SZk3A')

transcript_arr = []

for line in transcript:
    transcript_arr.append(line['text'])

print(*transcript_arr)
