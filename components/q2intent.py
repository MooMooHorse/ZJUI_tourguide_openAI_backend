import os
import sys
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from genai.itf import OpenAIITF
from paths import prompt_dir

def intent_extraction(query:str, itf:OpenAIITF = None, prompt_name:str = "get_intent.prompt") -> int:
    '''
        extract the intent from query

        Returns
        -------
        int
            1. A command to control the drone. Your output should be 0.
            2. A request or a question whose answer depends on the location of the user. Your output should be 1.
            3. A request or a question whose answer doesn't depend on the location of the user. Your output should be 2.

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
            "content": prompt
        },
        {
            "role": "user",
            "content": query
        }
    ]

    completion = itf.get_chat_completion_content(messages=message_list, temperature=0)
    
    ret_type = int(completion)

    return ret_type