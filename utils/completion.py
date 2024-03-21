import os
import sys
import json
import traceback

from typing import List
cur_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname((cur_dir))))
from genai.itf import OpenAIITF

def get_chat_completion(messages:List, itf: None, max_tokens = 1000, model = 'gpt-3.5-turbo-0125', temperature = 0.7) -> str:
    if itf is None:
        itf = OpenAIITF()
        itf.initialize_env()
    try:
        return itf.get_chat_completion_content(messages, max_tokens=1000, model='gpt-3.5-turbo-0125', temperature = temperature)
    except Exception as e:
        # encapsulate the exception and store it in the log
        error_log = {
            'answer' : 'E',
            'error': str(e),
            'reference': traceback.format_exc()
        }
        return json.dumps(error_log)