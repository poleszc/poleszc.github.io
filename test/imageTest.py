from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from os.path  import basename


url = "https://www.ifsc-climbing.org/index.php?option=com_ifsc&task=athlete.display&id=67"


try:
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        image = soup.find("img", class_="athlete-img")

        image_url = image["data-src"]
        print(image_url)
        photo_r = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})
        with open("VadimTimonov.jpg","wb") as f:
            f.write(photo_r.content)


    else:
        print("Downloading failed!")
        print(f"Status code: {r.status_code}")
except Exception as e:
    print(f"Exception {e} occured!")
