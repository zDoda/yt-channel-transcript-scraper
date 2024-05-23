import requests
from bs4 import BeautifulSoup
import re



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


channel_url = 'https://www.youtube.com/watch?v=erLbbextvlY'
html_content = get_youtube_channel_html(channel_url)
video_ids = extract_video_id(html_content)

for vid in video_ids:
    print(vid)