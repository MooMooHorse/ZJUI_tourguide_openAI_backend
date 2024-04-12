import os
import sys
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))

from paths import test_dir
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import re
from collections import Counter

def plot_intent_distr():
    fpath = os.path.join(test_dir, 'test_intent.json')

    with open(fpath, 'r') as f:
        data = json.load(f)
    answers = []
    for datum in data:
        answers.append(datum['answer'])

    # Count the frequency of each answer
    answer_counts = Counter(answers)

    # Prepare data for plotting
    categories = ['0', '1', '2']  # Categories for drone commands, location-dependent, and location-independent queries
    counts = [answer_counts[0], answer_counts[1], answer_counts[2]]

    # Create the bar chart
    plt.figure(figsize=(8, 6))
    plt.bar(categories, counts, color=['blue', 'green', 'red'])
    plt.xlabel('Answer Category')
    plt.ylabel('Number of Queries')
    plt.title('Distribution of Queries by Answer Category')
    plt.xticks(categories)
    plt.grid(axis='y', linestyle='--', linewidth=0.7)

    # Show the plot
    plt.show()
if __name__ == '__main__':
    plot_intent_distr()