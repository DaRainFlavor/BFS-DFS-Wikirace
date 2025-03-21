# MEMBERS
# Add members once finished

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
from collections import deque
import re
import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_lg") # change lg to md if it takes too long

def extract_wikilinks(wiki_url):
    # Extracts the text containing wikilinks and the links itself
    # Example
    # <a href="/wiki/Neutron_generator">Neutron tube</a>
    # Output : [('Neutron tube', 'https://en.wikipedia.org/wiki/Neutron_generator')]

    response = requests.get(wiki_url) # Fetch HTML content
    soup = BeautifulSoup(response.text, 'html.parser') # Parses the HTML to be able to extract links

    links = [] # storage for extracted text with links and the link itself
    seen_links = set() # for avoiding duplicates
    wiki_link_pattern = re.compile(r'^/wiki/[^:]*$')  # Pattern to match /wiki/ followed by any characters except ':'

    for link in soup.select("#mw-content-text a[href]"): # finds <a> tags inside the body
        href = link['href']
        if wiki_link_pattern.match(href):  # Ensure the link matches the pattern
            text = link.get_text(strip=True) # extracts the visible text inside the <a>
            full_url = "https://en.wikipedia.org" + href # converts to full wikipedia url
            normalized_href = normalize_url(full_url)  # Normalize URL to remove duplicates

            if text and normalized_href not in seen_links: # Add when not yet added
                seen_links.add(normalized_href)
                links.append((text, full_url))
    
    return links

def normalize_url(url):
    # prevents duplicate URLs when comparing links
    # ensures uniformity in URL formatting
    parsed_url = urlparse(url)
    return unquote(f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}")  # Remove fragment

def get_wikipedia_title(url): # Extracts the title of the wikipedia link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find("h1", {"id": "firstHeading"}).text.strip()

def spacy_similarity(title1, title2): # compuetes relationship of two articles from highlighted text (with href) to the target title 
    """Computes similarity between two Wikipedia article titles using SpaCy."""
    doc1 = nlp(title1)
    doc2 = nlp(title2)
    return doc1.similarity(doc2)

def find_wiki_path_bfs(base_url, target_url): # Prints the Path from base wikipedia article to target wikipedia article
    base_title = get_wikipedia_title(base_url)
    target_title = get_wikipedia_title(target_url)

    queue = deque([(base_url, [])])  # base url and a list of article titles (link texts) forming the path from base_url to current_url
    visited = set()
    while queue:
        current_url, path = queue.popleft() # removes the first url in the queue
        print("\n\n\nCurrently visiting path:")
        print(" -> ".join([base_title] + path) if path else base_title) # prints the current path formed
        
        # input("Press enter") # Uncomment if you want step by step process
        
        if current_url in visited: # do not reexplore if already visited
            continue
        visited.add(current_url)

        print("Gathering wikilinks and ranking them...")
        links = extract_wikilinks(current_url) # Extract wiki links from the current page
        
        ranked_links = []
        for text, link in links:
            similarity = spacy_similarity(text, target_title)
            ranked_links.append((text, link, similarity))

        # Sort links based on similarity (higher first)
        ranked_links.sort(key=lambda item: item[2], reverse=True)
        
        # Uncomment the code below to see the ranked wikilinks in the visited article based on spacy similarity to target title
        print(f"Wikilinks in {current_url}:")
        for text, link, _ in ranked_links:
            print(f"Highlighted Text: {text}\t\tLink: {link}")

        for text, link, _ in ranked_links:
            if normalize_url(link) == normalize_url(target_url):
                print("\n*** Path Found! ***")
                print(" -> ".join([base_title] + path + [text]))
                return
            
            if link not in visited:
                queue.append((link, path + [text]))  # Add link and updated path

    print("\nNo path found.")

def find_wiki_path_dfs(base_url, target_url):
    base_title = get_wikipedia_title(base_url)
    target_title = get_wikipedia_title(target_url)

    stack = [(base_url, [])]  # Stack stores (current_url, path)
    visited = set()

    while stack:
        current_url, path = stack.pop()  # DFS: Pop from end (Last In, First Out)

        print("\n\n\nCurrently visiting path:")
        print(" -> ".join([base_title] + path) if path else base_title)

        # input("Press enter")  # Uncomment for step-by-step execution

        if current_url in visited:
            continue
        visited.add(current_url)

        print("Gathering wikilinks and ranking them...")
        links = extract_wikilinks(current_url)  # Extract links from current page

        ranked_links = []
        for text, link in links:
            similarity = spacy_similarity(text, target_title)
            ranked_links.append((text, link, similarity))

        # Sort links based on similarity (higher first) to guide DFS 
        ranked_links.sort(key=lambda item: item[2])

        # Uncomment to see ranked links in the current article
        print(f"Wikilinks in {current_url}:")
        for text, link, _ in ranked_links:
            print(f"Highlighted Text: {text}\t\tLink: {link}")

        for text, link, _ in ranked_links:
            if normalize_url(link) == normalize_url(target_url):
                print("\n*** Path Found! ***")
                print(" -> ".join([base_title] + path + [text]))
                return

            if link not in visited:
                stack.append((link, path + [text]))  # Push to stack for DFS

    print("\nNo path found.")


if __name__ == "__main__":
    base_url = 'https://en.wikipedia.org/wiki/Thought_experiment'
    target_url = 'https://en.wikipedia.org/wiki/Medical_ultrasound'
    
    choice = int(input("Enter 1 to perform BFS, 2 to perform DFS: "))
    if choice == 1:
        find_wiki_path_bfs(base_url, target_url)
    elif choice==2:
        find_wiki_path_dfs(base_url, target_url)