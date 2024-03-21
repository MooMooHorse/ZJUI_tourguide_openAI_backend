import os
import sys
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from genai.itf import OpenAIITF
from paths import prompt_dir
from typing import List

class AnswerGenerator():
    def __init__(self):
        pass

    def generate(question:str, related_nodes: List[dict], itf:OpenAIITF = None, prompt_name:str = "get_answer.prompt") -> str:
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
                "content": "\nQuestion: "
            },
            {
                "role": "user",
                "content": question
            }
        ]

        completion = itf.get_chat_completion_content(messages=message_list)
        
        return completion
    
    