import requests
import json

search_term = "memory enhancement"

# Step 1: Search PubMed IDs
search_url = (
    f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    f"?db=pubmed&term={search_term}&retmode=json&retmax=5"
)

search_response = requests.get(search_url)
search_data = search_response.json()

paper_ids = search_data["esearchresult"]["idlist"]

print("Found IDs:", paper_ids)

papers = []

# Step 2: Fetch details for each paper
for paper_id in paper_ids:

    summary_url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        f"?db=pubmed&id={paper_id}&retmode=json"
    )

    summary_response = requests.get(summary_url)
    summary_data = summary_response.json()

    result = summary_data["result"][paper_id]

    title = result.get("title", "No title")
    pubdate = result.get("pubdate", "No date")

    papers.append({
        "id": paper_id,
        "title": title,
        "pubdate": pubdate,
        "link": f"https://pubmed.ncbi.nlm.nih.gov/{paper_id}/"
    })

# Save JSON
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(papers, file, indent=2)

print(f"Saved {len(papers)} PubMed papers")
