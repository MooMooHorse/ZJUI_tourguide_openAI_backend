import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file_path)
from components.q2intent import intent_extraction
from components.search_engine import SearchEngine
from components.answer_generation import AnswerGenerator
from genai.itf import OpenAIITF

from typing import Literal

Location = Literal["ZJUI Building", "Dining Hall", "Convenience Shop", "Library", "North teaching building", "bell tower", "Print shop"]

def query(query:str, location:Location="ZJUI Building") -> str:
    itf = OpenAIITF()
    se = SearchEngine()
    ag = AnswerGenerator()
    intent = intent_extraction(query, itf=itf)
    nodes = se.search(query, location, intent)
    answer = ag.generate(query, nodes, itf=itf)
    return answer

if __name__ == '__main__':
    query_str = "Tell me the history of the ZJUI building"
    print(query(query_str, location="bad location"))

