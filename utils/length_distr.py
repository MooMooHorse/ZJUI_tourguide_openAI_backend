import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from components.q2intent import intent_extraction
from components.search_engine import SearchEngine
from components.answer_generation import AnswerGenerator
from genai.itf import initialize_env
from openai import OpenAI
from paths import data_dir
from matplotlib import pyplot as plt
# Define path to the directory
directory_path = data_dir

# List all files in the directory
files = os.listdir(directory_path)

# Initialize a dictionary to store text lengths
text_lengths = []

def extract_text_from_pdf(file_path):
    import PyPDF2
    text = ''
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

# Loop over each file in the directory
for file_name in files:
    # Get the path to the file
    file_path = os.path.join(directory_path, file_name)
    # Check if it's a file and not a directory
    if os.path.isfile(file_path):
        try:
            if file_path.endswith('.txt'):
                # Open and read the file with UTF-8 encoding
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    word_count = len(text.split())
                    text_lengths.append(word_count)
            elif file_path.endswith('.pdf'):
                # Extract text from PDF files
                text = extract_text_from_pdf(file_path)
                word_count = len(text.split())
                text_lengths.append(word_count)
            
        except UnicodeDecodeError:
            # Try a different encoding if UTF-8 fails
            with open(file_path, 'r', encoding='latin-1') as file:
                text = file.read()
                word_count = len(text.split())
                text_lengths.append(word_count)
print(text_lengths)
# Plotting the text length distribution
plt.figure(figsize=(10, 6))
plt.hist(text_lengths, bins=30, color='skyblue', alpha=0.7)
plt.title('Distribution of Text Lengths (in Words)')
plt.xlabel('Number of Words')
plt.ylabel('Number of Documents')
plt.grid(True)
plt.savefig('hhh.png')