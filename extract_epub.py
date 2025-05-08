from ebooklib import epub
from bs4 import BeautifulSoup
import json
from jsonschema import validate
import ebooklib
import re
import os
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

def extract_text_from_epub(epub_file_path, output_file_path):
    book = epub.read_epub(epub_file_path)
    text = ""

    for item in book.get_items():
        # Use ebooklib.ITEM_DOCUMENT instead of epub.ITEM_DOCUMENT
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text += soup.get_text()

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(text)

def parse_glossary(text):
    # Example pattern to match glossary entries
    pattern = re.compile(r"(\w+\s\w+)(\s\d{3,4})?")
    matches = pattern.findall(text)
    philosophers = []

    for match in matches:
        name, year = match
        philosopher_data = {
            "name": name.strip(),
            "birth_year": int(year) if year else None,
            # Add more fields as needed
        }
        philosophers.append(philosopher_data)

    return philosophers

# Load the NER model and tokenizer
ner_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
ner_model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
ner_pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)

# Function to use NER model to extract entities
def extract_entities(text):
    ner_results = ner_pipeline(text)
    entities = []
    for entity in ner_results:
        if entity['entity'].startswith('B-PER') or entity['entity'].startswith('I-PER'):
            entities.append(entity['word'])
    return entities

# Replace these paths with the actual paths to your files
epub_file_path = "/Users/colinaulds/Downloads/Inventing Knowledge_ A Global and Historical Introduction to Philosophy.epub"
output_file_path = "/Users/colinaulds/Downloads/inventing_knowledge.txt"

extract_text_from_epub(epub_file_path, output_file_path)

# Load the JSON schema
with open('philosophy_schema.json', 'r') as schema_file:
    schema = json.load(schema_file)

# Ensure the outputs directory exists
os.makedirs('outputs', exist_ok=True)

def create_json_objects(text, schema):
    # Example pattern to match philosopher entries
    pattern = re.compile(r"(\w+\s\w+)(\s\d{3,4})?")
    matches = pattern.findall(text)
    philosophers = []

    for match in matches:
        name, year = match
        philosopher_data = {
            "name": name.strip(),
            "birth_year": int(year) if year else None,
            "death_year": None,  # Placeholder, to be enriched later
            "birth_location": None,  # Placeholder
            "death_location": None,  # Placeholder
            "major_events": [],  # Placeholder
            # Add more fields as needed
        }
        # Validate against schema
        try:
            validate(instance=philosopher_data, schema=schema)
            philosophers.append(philosopher_data)
        except Exception as e:
            print(f"Validation error for {name}: {e}")

    return philosophers

# Example usage
with open(output_file_path, "r", encoding="utf-8") as file:
    text_content = file.read()
    # Use NER to extract philosopher names
    philosopher_names = extract_entities(text_content)
    print(philosopher_names)  # For demonstration purposes
    # Create JSON objects
    philosophers = create_json_objects(text_content, schema)
    
    # Save JSON objects
    for i, philosopher in enumerate(philosophers):
        output_path = os.path.join('outputs', f'philosopher_{i}.json')
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(philosopher, json_file, ensure_ascii=False, indent=4)
        print(f'Saved: {output_path}')  # For demonstration purposes
