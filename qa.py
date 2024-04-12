import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file_path)
from components.q2intent import intent_extraction
from components.search_engine import SearchEngine
from components.answer_generation import AnswerGenerator
from genai.itf import OpenAIITF
from paths import io_dir
import json

from typing import Literal, List

Location = Literal["ZJUI Building", "Dining Hall", "Convenience Shop", "Library", "North teaching building", "bell tower", "Print shop"]

def query(query:str, location:Location="ZJUI Building") -> str:
    itf = OpenAIITF()
    se = SearchEngine()
    ag = AnswerGenerator()
    intent = intent_extraction(query, itf=itf)
    nodes = se.search(query, location, intent)
    answer = ag.generate(query, nodes, itf=itf)
    return answer

def read_input(input_fname:str = "agent_input.json") -> List[dict]:
    '''
    Return
    ------
    work_items: List[dict]
        [
            {
                "q_id": <int>,
                "question": <str>,
                "enable": <bool>
            }
        ]
    '''
    fpath = os.path.join(io_dir, input_fname)
    with open(fpath, 'r') as f:
        questions = json.load(f)
    work_items = []
    for question in questions:
        if question["enable"] == True:
            work_items.append(question)
    return work_items

def write_output(work_items:List[dict], output_fname:str = "agent_output.json") -> None:
    '''
    Parameters
    ----------
    work_items: List[dict]
        [
            {
                "q_id": <int>,
                "question": <str>,
                "enable": <bool>,
                "answer": <str>
            }
        ]
    '''
    fpath = os.path.join(io_dir, output_fname)
    with open(fpath, 'w') as f:
        json.dump(work_items, f)

if __name__ == '__main__':
    work_items = read_input()
    
    for work_item in work_items:
        try:
            work_item["answer"] = query(work_item["question"])
        except Exception as e:
            from traceback import format_exc
            stack_info = format_exc()
            work_item["answer"] = f"Error: {str(e)}\n{stack_info}"
    
    write_output(work_items)

