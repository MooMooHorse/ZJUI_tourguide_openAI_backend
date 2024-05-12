import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from genai.itf import OpenAIITF
from paths import io_dir
import json
from typing import Literal, List

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

def append_input(work_item:dict, input_fname:str = "agent_input.json") -> dict:
    '''
    Append One work item to the input file and return the work item with q_id updated
    Parameters
    ----------
    work_item: dict
        {
            "q_id": <int>,
            "question": <str>,
            "enable": <bool>
        }
    '''
    fpath = os.path.join(io_dir, input_fname)
    with open(fpath, 'r') as f:
        questions = json.load(f)
    max_q_id = max([question["q_id"] for question in questions])
    _work_item = {
        "q_id": max_q_id + 1,
        "question": work_item["question"],
        "metadata": work_item["metadata"],
        "enable": False
    }
    questions.append(_work_item)
    with open(fpath, 'w') as f:
        json.dump(questions, f)
    work_item.update({"q_id": max_q_id + 1})
    return work_item
    
def append_output(work_item:dict, output_fname:str = "agent_output.json") -> None:
    '''
    Append One work item to the output file
    Parameters
    ----------
    work_item: dict
        {
            "q_id": <int>,
            "question": <str>,
            "enable": <bool>,
            "answer": <str>
        }
    '''
    fpath = os.path.join(io_dir, output_fname)
    with open(fpath, 'r') as f:
        questions = json.load(f)
    questions.append(work_item)
    with open(fpath, 'w') as f:
        json.dump(questions, f)