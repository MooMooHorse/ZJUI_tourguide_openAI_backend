import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from components.q2intent import intent_extraction
from components.search_engine import SearchEngine
from components.answer_generation import AnswerGenerator
from genai.itf import OpenAIITF
from typing import Tuple    

class LocationQAAgent():
    def __init__(self, location, OpenAI_itf:OpenAIITF = None):
        self.location = location
        self.OpenAI_itf = OpenAI_itf

    def query(self, query:str, intent:int) -> Tuple[str, str]:
        se = SearchEngine()
        ag = AnswerGenerator()
        nodes, responsible_agents = se.search(query, self.location, intent)
        answer = ag.generate(query, nodes, itf=self.OpenAI_itf)
        return answer, str(responsible_agents)