import requests
from bs4 import BeautifulSoup
import json

url = "https://arxiv.org/search/?query=artificial+intelligence&searchtype=all"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

papers = []

results = soup.find_all("li", class_="arxiv-result")

for item in results:
    title_tag = item.find("p", class_="title")
    link_tag = item.find("p", class_="list-title")

    if title_tag and link_tag:
        a_tag = link_tag.find("a")

        if a_tag:
            title = title_tag.text.strip()
            link = a_tag["href"]

            papers.append({
                "title": title,
                "link": link
            })

with open("data.json", "w", encoding="utf-8") as file:
    json.dump(papers, file, indent=2)

print(f"Saved {len(papers)} papers to data.json")