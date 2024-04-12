import os
import sys
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))

import json
from components.q2intent import intent_extraction
from components.search_engine import SearchEngine
from components.answer_generation import AnswerGenerator
from genai.itf import OpenAIITF
from paths import test_dir

from components.q2intent import intent_extraction

def test_intent_extraction():
    itf = OpenAIITF()
    se = SearchEngine()
    queries = []
    fpath = os.path.join(test_dir, 'test_intent.json')
    with open(fpath, 'r') as f:
        data = json.load(f)
    for datum in data:
        queries.append((datum['query'], datum['answer']))
    score = 0
    for query, gt in queries:
        intent = intent_extraction(query, itf=itf)
        if intent != gt:
            print(f"Failed for query: {query}")
            print(f"Expected: {gt}")
            print(f"Got: {intent}")
        else:
            print(f"Passed for query: {query}")
            score += 1

    print(f"Score: {score}/{len(queries)}")

if __name__ == '__main__':
    test_intent_extraction()