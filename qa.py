import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file_path)
from components.q2intent import intent_extraction
from components.search_engine import SearchEngine
from components.answer_generation import AnswerGenerator
from genai.itf import OpenAIITF
from agent_io.io_ops import read_input, write_output, append_input
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

def unit_test_mode():
    '''
        file I/O based unit test mode
    '''
    work_items = read_input()
    
    for work_item in work_items:
        try:
            work_item["answer"] = query(work_item["question"])
        except Exception as e:
            from traceback import format_exc
            stack_info = format_exc()
            work_item["answer"] = f"Error: {str(e)}\n{stack_info}"
    
    write_output(work_items)
    

def integrated_mode(question = None):
    '''
        file io will be used as logs

        Input
        -----
        qa.py -q <question>

        Side Effect
        -----------
        i/o will be loged at agent_input.json and agent_output.json under `io_dir`
    '''
    def _read_qa_from_cmd():
        import argparse
        # read parameters
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("-q", "--question", type=str, required=True)
        args = parser.parse_args()
        question = args.question
        try:
            answer = query(question)
        except Exception as e:
            from traceback import format_exc
            stack_info = format_exc()
            answer = f"Error: {str(e)}\n{stack_info}"
        return question, answer
    if question is None:
        question, answer = _read_qa_from_cmd()
    else:
        try:
            answer = query(question)
        except Exception as e:
            from traceback import format_exc
            stack_info = format_exc()
            answer = f"Error: {str(e)}\n{stack_info}"
    # log the question and answer
    work_item = {
        "question": question,
        "enable": True,
        "answer": answer
    }
    # log the I/O
    write_output([append_input(work_item)])


if __name__ == '__main__':
    integrated_mode()

