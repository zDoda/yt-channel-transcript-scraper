import requests
from bs4 import BeautifulSoup

vidId = "rSHREFWb41M"
response = requests.get(f"https://www.youtube.com/watch?v={vidId}")
soup = BeautifulSoup(response.content, "html.parser")

# Get the title of the HTML document
title = soup.title.string
print(title[:-9])

