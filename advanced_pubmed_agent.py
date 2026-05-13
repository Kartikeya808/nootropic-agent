import requests
import json
import xml.etree.ElementTree as ET

search_term = "(nootropics OR cognitive enhancement) AND humans"

# SEARCH FOR IDS
search_url = (
    f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    f"?db=pubmed&term={search_term}&retmode=json&retmax=5"
)

search_response = requests.get(search_url, timeout=10)
search_data = search_response.json()

paper_ids = search_data["esearchresult"]["idlist"]

print("Found IDs:", paper_ids)

papers = []

# FETCH EACH PAPER
for paper_id in paper_ids:

    print(f"Fetching paper {paper_id}...")

    try:

        fetch_url = (
            f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            f"?db=pubmed&id={paper_id}&retmode=xml"
        )

        fetch_response = requests.get(fetch_url, timeout=10)

        root = ET.fromstring(fetch_response.content)

        article = root.find(".//PubmedArticle")

        if article is None:
            print(f"No article found for {paper_id}")
            continue

        # TITLE
        title_element = article.find(".//ArticleTitle")
        title = title_element.text if title_element is not None else "No title"

        # ABSTRACT
        abstract_text = ""

        abstract_elements = article.findall(".//AbstractText")

        for section in abstract_elements:
            if section.text:
                abstract_text += section.text + " "

        # DATE
        pubdate_element = article.find(".//PubDate/Year")
        pubdate = pubdate_element.text if pubdate_element is not None else "Unknown"

        papers.append({
            "id": paper_id,
            "title": title,
            "abstract": abstract_text.strip(),
            "pubdate": pubdate,
            "link": f"https://pubmed.ncbi.nlm.nih.gov/{paper_id}/"
        })

        print(f"Saved paper {paper_id}")

    except Exception as e:
        print(f"Error with {paper_id}: {e}")

# SAVE JSON
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(papers, file, indent=2, ensure_ascii=False)

print(f"\nSaved {len(papers)} detailed papers")