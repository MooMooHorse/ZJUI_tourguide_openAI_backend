import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file_path)
from components.q2intent import intent_extraction
from components.search_engine import SearchEngine
from components.answer_generation import AnswerGenerator
from agents.location_qa_agents import LocationQAAgent
from genai.itf import OpenAIITF
from agent_io.io_ops import read_input, write_output, append_input
from agents.uav_op_agent import UAVOPAgent
from paths import data_dir
import json

from typing import Literal, List, Tuple

Location = Literal["ZJUI Building", "Dining Hall", "Convenience Shop", "Library", "North teaching building", "bell tower", "Print shop", "Lake"]


def associate_q_w_request(question:str, cur_location:str, locations:List[str]) -> str:
    '''
    If the question is asociated with the current location of user.
    '''
    question = question + f''' I'm currently at {cur_location}.''' 
    return question

def ground_locations(location:str):
    '''
        Limit the locations to all locations with agents in the system
    '''
    candidates_locations = []
    files = os.listdir(data_dir)
    node_files = [file for file in files if file.endswith('.json')]

    for file in node_files:
        with open(os.path.join(data_dir, file), 'r') as f:
            node = json.load(f)
            candidates_locations.append(node['location'].lower().strip().replace(' ', ''))
    
    if location.lower().strip().replace(' ', '') not in candidates_locations:
        location = "ZJUI Building"
    return location

def query(query:str, location:Location="ZJUI Building") -> Tuple[str, dict]:
    '''
    Input
    -----
    query: str
        query to be answered
    location: Location
        current location of the user

    Output
    ------
    answer: str
        answer to the query
    meta: dict
        meta data
        {
            "operation": [<OPERATION_1>, ...]
        }
    '''
    itf = OpenAIITF()
    intent = intent_extraction(query, itf)

    location = ground_locations(location)

    print(f'''current location: {location}''')

    if intent == 2: # intent related to cur location
        query = associate_q_w_request(query, location, [location])

    if intent == 1 or intent == 2:
        agent = LocationQAAgent(location, itf)
        answer, agents_involved = agent.query(query, intent)
    else:
        agent = UAVOPAgent(itf)
        answer = agent.query(query)
        agents_involved = "[UAV Operation Agent]"
        if answer is None:
            return "Illegal Command to UAV Operation Agent", {}
    return f'''You answer is composed by the following agents: {agents_involved}\n{answer}''', {
        "operation": [answer]
    }



def unit_test_mode():
    '''
        file I/O based unit test mode
    '''
    work_items = read_input()
    
    for work_item in work_items:
        try:
            work_item["answer"], metadata = query(work_item["question"])
        except Exception as e:
            from traceback import format_exc
            stack_info = format_exc()
            work_item["answer"] = f"Error: {str(e)}\n{stack_info}"
    
    write_output(work_items)
    

def integrated_mode(question = None, cur_loc = "ZJUI Building") -> Tuple[str, dict]:
    '''
        file io will be used as logs

        Input
        -----
        qa.py -q <question>

        Side Effect
        -----------
        i/o will be loged at agent_input.json and agent_output.json under `io_dir`
    '''
    def _read_q_from_cmd():
        import argparse
        # read parameters
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("-q", "--question", type=str, required=True)
        args = parser.parse_args()
        question = args.question
        return question
    if question is None:
        question = _read_q_from_cmd()
    try:
        answer, metadata = query(question, location=cur_loc)
    except Exception as e:
        from traceback import format_exc
        stack_info = format_exc()
        answer = f"Error: {str(e)}\n{stack_info}"
        print(answer)
    # log the question and answer
    work_item = {
        "question": question,
        "enable": True,
        "answer": answer,
        "metadata": metadata
    }
    # log the I/O
    write_output([append_input(work_item)])
    return answer, metadata

if __name__ == '__main__':
    integrated_mode()

