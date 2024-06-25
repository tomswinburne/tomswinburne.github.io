import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import requests

def get_doi_from_crossref(title, author):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 6.0; Windows NT 5.1)'
    }
    params = {
        'query.bibliographic': title,
        'query.author': author,
        'rows': 1
    }
    response = requests.get("https://api.crossref.org/works", headers=headers, params=params)
    print("trying",title,author)
    if response.status_code == 200:
        data = response.json()
        if data['message']['items']:
            return data['message']['items'][0].get('DOI', '')
    return ''

def bibtex_to_markdown(bibtex_file, output_md_file):
    with open(bibtex_file, 'r') as bibfile:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibfile, parser=parser)

    # Reverse the list of entries
    reversed_entries = bib_database.entries[::-1]

    with open(output_md_file, 'w') as mdfile:
        mdfile.write("# Publications\n\n")
        for entry in reversed_entries:
            title = entry.get('title', 'No Title')
            author = entry.get('author', 'No Author')
            year = entry.get('year', 'No Year')
            journal = entry.get('journal', 'No Journal')
            doi = entry.get('doi', '')

            if not doi:
                doi = get_doi_from_crossref(title, author)

            if doi:
                doi_link = f"[DOI](https://doi.org/{doi})"
            else:
                doi_link = ""

            mdfile.write(f"- **{title}**, {author}, *{journal}*, {year}. {doi_link}\n")

if __name__ == "__main__":
    bibtex_file = 'publications.bib'  # replace with your BibTeX file
    output_md_file = 'papers.md'  # replace with your desired output Markdown file
    bibtex_to_markdown(bibtex_file, output_md_file)

