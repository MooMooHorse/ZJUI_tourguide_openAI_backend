import os
cur_dir = os.path.abspath(os.path.dirname(__file__))

data_dir = os.path.join(cur_dir, 'data') # paths containing data
openAI_dir = os.path.join(cur_dir, 'genai') # paths containing openai scripts
prompt_dir = os.path.join(openAI_dir, 'prompts') # paths containing openai prompt
openai_config_path = os.path.join(openAI_dir, 'config.json') # paths containing openai config
openai_log_dir = os.path.join(openAI_dir, 'logs') # paths containing openai logs