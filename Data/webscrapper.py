# %%
from bs4 import BeautifulSoup
import requests
import json

dict = {}

hints = ["around-the-house","before-and-after","book-title","classic-movie","classic-tv","college-life","event","family","fictional-character","fictional-place","food-and-drink","fun-and-games","headline","husband-and-wife","in-the-kitchen","landmark","living-thing","megaword","movie-quotes"]

for y in hints:
    counter = 0
    html = requests.get("https://wheeloffortuneanswer.com/" + y + "/").text

    soup = BeautifulSoup(html, 'lxml')
    for s in soup.select('a'):
        s.extract()
    phrases = soup.find_all("td",class_ = "column-1")

    for x in range(0,50):
        phrases.pop(len(phrases) - 1)


    for x in phrases:
        if counter < 10 and True:
            key = x.get_text().strip()
            dict[key] = y
            counter += 1

with open("phrases.json","w") as file:
    file = json.dump(dict, file)


