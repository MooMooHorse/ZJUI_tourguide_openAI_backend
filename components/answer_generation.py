import os
import sys
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from genai.itf import OpenAIITF
from paths import prompt_dir, agent_mem_dir
from typing import List
import json

class AnswerGenerator():
    def __init__(self):
        pass

    def generate(self, question:str, related_nodes: List[dict], itf:OpenAIITF = None, iter = 1, prompt_name:str = "get_answer.prompt") -> str:
        '''
            Generate the answer to the question based on the related nodes

            Returns
            -------
            str
                The answer to the question

            Side-Effect
            ------------
            Caller need to use try-except block to handle the exception thrown by get_chat_completion_content() and completion conversion
        '''
        agent_memory_path = os.path.join(agent_mem_dir, f"agent_memory_{iter}.json")
        with open(agent_memory_path, 'r') as f:
            historical_qa = f.read()
        
        if itf is None:
            itf = OpenAIITF()
        
        with open(os.path.join(prompt_dir, prompt_name), 'r') as f:
            prompt = f.read()

        message_list = [
            {
                "role": "system",
                "content": prompt + "\n Below is a list of reference nodes"
            },
            {
                "role": "user",
                "content": str(related_nodes)
            },
            {
                "role": "system",
                "content": "Below is a list of historical QAs asked by user and answered by you."
            },
            {
                "role": "user",
                "content": historical_qa
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

        completion = itf.get_chat_completion_content(messages=message_list, temperature=0, model = 'gpt-4')

        with open(agent_memory_path, 'w') as f:
            f.write(json.dumps({
                "question": question,
                "answer": completion
            }))
        
        return completion
    
    