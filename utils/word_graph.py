import os
import sys
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))

from paths import test_dir
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import re

def draw_word_graph_1():
    fpath = os.path.join(test_dir, 'test_intent.json')
    with open(fpath, 'r') as f:
        data = json.load(f)
    quries = []
    for datum in data:
        quries.append(datum['query'])
    
    # Combine all queries into a single string
    text = ' '.join(quries)

    # Remove special characters and numbers
    text = re.sub(r'[^A-Za-z\s]', '', text)

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    draw_word_graph_1()