from googlesearch import search
import requests
import os


query = "Vadim Timonov climber"

for j in search(query, num=1, stop=1, pause=2):
    image_url = j
    if image_url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        download_image(image_url)
        break