# Wiki-Race Project

## Overview
This project implements a Wikipedia link traversal system using **BFS (Breadth-First Search) and DFS (Depth-First Search)** to determine the shortest hyperlink path between two Wikipedia articles. The program extracts Wikipedia links using **BeautifulSoup**, ranks them using **SpaCy NLP similarity analysis**, and applies **BFS and DFS** for pathfinding.

## How to Use

### 1. Clone the Repository
```
git clone https://github.com/DaRainFlavor/BFS-DFS-Wikirace.git
cd BFS-DFS-Wikirace

### 2. Install Dependencies
```
pip install -r requirements.txt

### 3. Download SpaCy Language Models
```
python -m spacy download en_core_web_md
python -m spacy download en_core_web_lg

## Example Usage
Modify the Language Model in wikirace.py
```
nlp = spacy.load("en_core_web_md")  # or use "en_core_web_lg" for better context

Edit this to specify the starting and target Wikipedia articles:
```
base_url = 'https://en.wikipedia.org/wiki/Thought_experiment'
target_url = 'https://en.wikipedia.org/wiki/Medical_ultrasound'
