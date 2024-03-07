from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

NUMBER_OF_PEOPLE = 10 # For this script to work, this value must be between 0 and 50    

# FILE_NAME = "international.md"
# FILE_NAME = "poland.md"
# FILE_NAME = "italy.md"
FILE_NAME = "usa.md"

# url = "https://www.8a.nu/ranking/bouldering?topAscents=top10&gender=combined&style=combined&time=lastyear&age=combined&country" # INTERNATIONAL
# url = "https://www.8a.nu/ranking/bouldering?country=poland" # POLAND
# url = "https://www.8a.nu/ranking/bouldering?country=italy" # ITALY
url = "https://www.8a.nu/ranking/bouldering?country=united-states" # USA




def generateHeader(file):
    country = FILE_NAME.split(".")[0].strip()
    if country == "international":
        file.write(f"# Międzynarodowy ranking wspinaczy\n")
    elif country == "poland":
        file.write(f"# Ranking wspinaczy w Polsce\n")
    elif country == "italy":
        file.write(f"# Ranking wspinaczy we Włoszech\n")
    elif country == "usa":
        file.write(f"# Ranking wspinaczy w USA\n")
    else:
        file.write(f"# Ranking wspinaczy\n")

def findInstagramProfile(name):
    query = f"{name} climber instagram"
    profile = ""

    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=5)]
        profile = results[0]['href']
    print(profile)
    return profile

def generateAscentFile(climber):
    profile_file = "".join(climber[0].split()) + ".md"
    profile_url = climber[5]

    try:
        r = requests.get(profile_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            info = []

            name = soup.find("div", class_="title").text.strip()
            location = soup.find("div", class_="location").text.strip()
            age = soup.find("div", class_ = "user-age").text.strip()
            stats = soup.find("div", class_="statistics")
            routes = "".join(stats.find("div", class_="statistics-value").text.strip().split())
            boulders = "".join(stats.find("div", class_="statistics-value").find_next("div", class_="statistics-value").text.strip().split())

            with open(profile_file, "w+") as profile:
                profile.write(f"# {name}\n")
                profile.write(f"- __Pełne imię:__ {name}\n")
                profile.write(f"- __Miejsce zamieszkania:__ {location}\n")
                profile.write(f"- __Wiek:__ {age}\n")
                profile.write(f"- __Liczba zrobionych dróg:__ {routes}\n")
                profile.write(f"- __Liczba zrobionych boulderów:__ {boulders}\n")
                profile.write(f"- [Profil na Instagramie]({findInstagramProfile(name)})\n")
            print(f"{name} generated")



            # To nie działa bo to dynamiczna strona, potrzebaby było selenium zeby poczekac na załadowanie
            # hardest = soup.find("div", class_="statistics-line stats")
            # print(hardest)
            # hardestInfo = []
            # hardestInfo.append(hardest.find("div", class_="grade-difficulty").text.strip())
            # hardestInfo.append(hardest.find_all("div", class_="number-cell")[-1].text.strip())

            # secondHardest = soup.find("div", class_="statistics-line stats").find("div", class_="statistics-line stats")
            # print(secondHardest)
            # secondHardestInfo = []
            # secondHardestInfo.append(secondHardest.find("div", class_="grade-difficulty").text.strip())
            # secondHardestInfo.append(secondHardest.find_all("div", class_="number-cell")[-1].text.strip())

            # thirdHardest = soup.find("div", class_="statistics-line stats").find("div", class_="statistics-line stats").find("div", class_="statistics-line stats")
            # print(thirdHardest)
            # thirdHardestInfo = []
            # thirdHardestInfo.append(thirdHardest.find("div", class_="grade-difficulty").text.strip())
            # thirdHardestInfo.append(thirdHardest.find_all("div", class_="number-cell")[-1].text.strip())

            # ascents = [hardestInfo, secondHardestInfo, thirdHardestInfo]    
            # print(ascents)  
        else:
            print("Downloading failed!")
            print(f"Status code: {r.status_code}")
    except Exception as e:
        print(f"Exception {e} occured!")

def generatePerson(file, climber):
    ascent_file = "".join(climber[0].split()) + ".html"
    full = "people/" + ascent_file
    file.write(f"## {climber[3]}. {climber[0]} ([Dodatkowe informacje]({full}))\n")
    file.write(f"* __Liczba Punktów:__ {climber[4]}\n")
    file.write(f"* __Rok urodzenia:__ {climber[1]}\n")
    file.write(f"* __Kraj:__ {climber[2]}\n")
    generateAscentFile(climber)

def generateMarkdown(climbers):
    with open(FILE_NAME, "w+") as file:
        generateHeader(file)
        for ix, climber in enumerate(climbers):
            if (ix >= NUMBER_OF_PEOPLE):
                break
            generatePerson(file, climber)



try:
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        climbers = []

        lines = soup.find_all("div", class_="line")
        for ix, line in enumerate(lines):
            if ix >= NUMBER_OF_PEOPLE:
                break
            link = line.find("a", class_="") # Wyciagamy link do profilu na 8a
            profile_url = "https://www.8a.nu" + link['href']
            rank = line.find("div", class_="rank-column").text.strip().replace('.', '')
            name = line.find("div", class_="name").text.strip()
            try:
                country, birth_year = line.find("div", class_="info").text.split("•")
            except Exception as e:
                birth_year = '0'
            points = line.find("div", class_="points-column").text.strip().split()
            climbers.append([name, birth_year.strip(), country.strip(), rank, "".join(points), profile_url])
        generateMarkdown(climbers)
    else:
        print("Downloading failed!")
        print(f"Status code: {r.status_code}")
except Exception as e:
    print(f"Exception {e} occured!")






