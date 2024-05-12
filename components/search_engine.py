import os
import sys
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from genai.itf import OpenAIITF
from paths import prompt_dir, data_dir
import json
from typing import List, Tuple


class SearchEngine():
    def __init__(self):
        pass
    
    def get_location(self, question:str, candidate_locations:List[str], itf:OpenAIITF = None, prompt_name = 'associate_location.prompt') -> str:
        if itf is None:
            itf = OpenAIITF()

        with open(os.path.join(prompt_dir, prompt_name), 'r') as f:
            prompt = f.read()
        message_list = [
            {
                "role": "system",
                "content": prompt + '\n Below is a list of candidates locations'
            },
            {
                "role": "user",
                "content": str(candidate_locations)
            },
            {
                "role": "system",
                "content": "\nQuestion: "
            },
            {
                "role": "user",
                "content": question
            }
        ]
        return itf.get_chat_completion_content(message_list, temperature=0)

    def search(self, question:str, cur_location:str, type:int) -> Tuple[List[dict], List[str]]:
        '''
        If type is 0, return None
        If type is 1, get the nodes w/ location queried by get_location
        If type is 2, get the nodes w/ cur_location

        Return
        ------
        List[dict]: nodes

        '''
        def _sanity_chk_locations(locations:List[str], _candidates:List[str]) -> bool:
            candidates = _candidates.copy()
            # if locations not a list, return False
            if not isinstance(locations, list):
                return False
            for index, candidate in enumerate(candidates):
                candidates[index] = candidate.lower().replace(' ', '')
            
            for location in locations:
                if location.lower().replace(' ','') not in candidates:
                    return False
            return True

        if type == 0:
            return None, []
        
        candidates_locations = []
        files = os.listdir(data_dir)
        node_files = [file for file in files if file.endswith('.json')]
        nodes = []

        for file in node_files:
            with open(os.path.join(data_dir, file), 'r') as f:
                node = json.load(f)
                candidates_locations.append(node['location'])
        q_locations = json.loads(self.get_location(question, candidates_locations))

        if type == 1 or cur_location in q_locations:
            locations = q_locations
        elif type == 2:
            locations = [cur_location] + q_locations
            
        
        # log choosing candidate locations
        print(f"Choosing candidate locations: {locations} among {candidates_locations}")

        if not _sanity_chk_locations(locations, candidates_locations):
            return []
        

        for i in range(len(locations)):
            locations[i] = locations[i].lower().replace(' ', '')
        responsible_agents = []
        for file in node_files:
            with open(os.path.join(data_dir, file), 'r') as f:
                node = json.load(f)
                if node['location'].lower().replace(' ','') in locations:
                    print(node['text'], node["responsible_agent"])
                    responsible_agents.append(node["responsible_agent"])
                    with open(os.path.join(data_dir, node['text']), 'r', encoding='utf-8') as f1:
                        text = f1.read()
                    node['text'] = text
                    nodes.append(node)
        

        return nodes, responsible_agents


