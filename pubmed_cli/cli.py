import requests
import pandas as pd
import argparse
import re

# PubMed API base URLs
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_papers(query, debug=False):
    """Fetch paper IDs from PubMed based on a query."""
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": 10}
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    paper_ids = response.json().get("esearchresult", {}).get("idlist", [])

    if debug:
        print(f"🔍 Debug: Fetched Paper IDs: {paper_ids}")
    return paper_ids

def fetch_paper_details(paper_ids, debug=False):
    """Fetch paper details from PubMed."""
    if not paper_ids:
        return {}

    params = {"db": "pubmed", "id": ",".join(paper_ids), "retmode": "json"}
    response = requests.get(PUBMED_SUMMARY_URL, params=params)
    response.raise_for_status()
    data = response.json().get("result", {})

    if debug:
        print(f"🔍 Debug: Fetched Paper Details: {data}")
    return data

def fetch_paper_authors(paper_id, debug=False):
    """Fetch detailed author information including email and affiliations."""
    params = {"db": "pubmed", "id": paper_id, "rettype": "medline", "retmode": "text"}
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    text_data = response.text

    email = "N/A"
    affiliations = {}
    authors = []

    author_affiliation_pattern = re.findall(r"AU  - (.+?)\n", text_data)
    affiliation_pattern = re.findall(r"AD  - (.+?)\n", text_data)

    for i, author in enumerate(author_affiliation_pattern):
        authors.append(author)
        affiliations[author] = affiliation_pattern[i] if i < len(affiliation_pattern) else "Unknown Affiliation"

    email_match = re.search(r"Electronic address: (.+?)\n", text_data)
    if email_match:
        email = email_match.group(1).strip()

    if debug:
        print(f"🔍 Debug: Processed Paper ID {paper_id} - Authors: {authors}, Email: {email}")

    return authors, affiliations, email

def filter_non_academic_authors(paper_data, debug=False):
    """Identify non-academic authors based on affiliation keywords."""
    company_keywords = ["Inc", "Ltd", "Pharma", "Biotech", "Corporation"]
    filtered_papers = []

    for paper_id, details in paper_data.items():
        if paper_id == "uids":
            continue

        title = details.get("title", "N/A")
        pub_date = details.get("pubdate", "N/A")

        authors, affiliations, corresponding_author_email = fetch_paper_authors(paper_id, debug)

        non_academic_authors = []
        company_affiliations = []

        for author in authors:
            affiliation = affiliations.get(author, "Unknown Affiliation")
            if any(keyword in affiliation for keyword in company_keywords):
                non_academic_authors.append(author)
                company_affiliations.append(affiliation)

        paper_entry = {
            "PubmedID": paper_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": corresponding_author_email if corresponding_author_email else "N/A"
        }

        filtered_papers.append(paper_entry)

        if debug:
            print(f"🔍 Debug: Processed Paper ID {paper_id} - {paper_entry}")

    return filtered_papers

def save_to_csv(data, filename):
    """Save filtered data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"✅ Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers with non-academic authors from PubMed.",
        usage="python cli.py '<query>' -f <filename.csv> [-d]",
        epilog="Example: python cli.py 'cancer research' -f results.csv -d"
    )
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument("-f", "--file", required=True, help="Filename to save results as CSV. (Required)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    paper_ids = fetch_pubmed_papers(args.query, args.debug)
    paper_data = fetch_paper_details(paper_ids, args.debug)
    filtered_papers = filter_non_academic_authors(paper_data, args.debug)

    save_to_csv(filtered_papers, args.file)

if __name__ == "__main__":
    main()
