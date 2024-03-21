import os
import sys
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from genai.itf import OpenAIITF
from paths import prompt_dir, data_dir
import json
from typing import List

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

    def search(self, question:str, cur_location:str, type:int) -> List[dict]:
        '''
        If type is 0, return None
        If type is 1, get the nodes w/ location queried by get_location
        If type is 2, get the nodes w/ cur_location

        Return
        ------
        List[dict]: nodes

        '''
        if type == 0:
            return None
        
        candidates_locations = []
        files = os.listdir(data_dir)
        node_files = [file for file in files if file.endswith('.json')]
        nodes = []

        for file in node_files:
            with open(os.path.join(data_dir, file), 'r') as f:
                node = json.load(f)
                candidates_locations.append(node['location'])

        if type == 1:
            locations = json.loads(self.get_location(question, candidates_locations))
        elif type == 2:
            locations = [cur_location]
        
        for i in range(len(locations)):
            locations[i] = locations[i].lower().replace(' ', '')

        
        for file in node_files:
            with open(os.path.join(data_dir, file), 'r') as f:
                node = json.load(f)
                if node['location'].lower().replace(' ','') in locations:
                    with open(os.path.join(data_dir, node['text']), 'r') as f1:
                        text = f1.read()
                    node['text'] = text
                    nodes.append(node)
                    
        return nodes


