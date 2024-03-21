from typing import Dict
import os
import sys
cur_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname((cur_dir)))
from paths import openai_log_dir
import json, datetime


class OpenAI_Logger():
    def __init__(self):
        now = datetime.datetime.now()
        log_dir = os.path.join(openai_log_dir, now.strftime("%Y-%m-%d-%H-%M-%S"))
        os.makedirs(log_dir, exist_ok=True)
        self.call_trace_file = os.path.join(log_dir, 'call_trace.txt') # upon each openAI call, we append the return object to this file
        self.statistics_file = os.path.join(log_dir, 'statistics.json') # upon each openAI call, we update the statistics in this file
        with open(self.statistics_file, 'w') as f:
            json.dump({
                'total_calls': 0,
                'total_tokens_used': 0,
                'total_completion_tokens': 0,
                'total_prompt_tokens': 0
            }, f)

    def update_statistics(self, tokens_used, completion_tokens, prompt_tokens
                          , is_called = 1):
        with open(self.statistics_file, 'r') as f:
            statistics = json.load(f)
        statistics['total_calls'] += is_called
        statistics['total_tokens_used'] += tokens_used
        statistics['total_completion_tokens'] += completion_tokens
        statistics['total_prompt_tokens'] += prompt_tokens
        with open(self.statistics_file, 'w') as f:
            json.dump(statistics, f)

    def log_message(self, message:str):
        with open(self.call_trace_file, 'a') as f:
            f.write(message)
    