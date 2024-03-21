import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file_path)
from components.q2intent import intent_extraction
from components.serch_engine import SearchEngine
from components.answer_generation import AnswerGenerator
from genai.itf import OpenAIITF
if __name__ == '__main__':
    query = "Tell me the history of the ZJUI building"
    itf = OpenAIITF()
    se = SearchEngine()
    ag = AnswerGenerator()
    intent = intent_extraction(query, itf=itf)
    print(intent)
    nodes = se.search(query, "ZJUI Building", intent)
    print(nodes)
    answer = ag.generate(query, nodes, itf=itf)
    print(answer)

