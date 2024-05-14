import os
cur_dir = os.path.abspath(os.path.dirname(__file__))

data_dir = os.path.join(cur_dir, 'data') # paths containing data
openAI_dir = os.path.join(cur_dir, 'genai') # paths containing openai scripts
prompt_dir = os.path.join(openAI_dir, 'prompts') # paths containing openai prompt
openai_config_path = os.path.join(openAI_dir, 'config.json') # paths containing openai config
openai_env_path = os.path.join(openAI_dir, 'env.json') # paths containing openai
openai_log_dir = os.path.join(openAI_dir, 'logs') # paths containing openai logs
test_dir = os.path.join(cur_dir, 'test') # paths containing test
io_dir = os.path.join(cur_dir, 'agent_io') # paths containing io
agents_config_dir = os.path.join(cur_dir, 'agents', 'config') # paths containing agents config
agent_mem_dir = os.path.join(cur_dir, 'agents', 'memory') # paths containing agents memory
image_proc_dir = os.path.join(cur_dir, 'img_processing', 'testing_imgs')
tagged_image_dir = os.path.join(cur_dir, 'img_processing', 'tagged_imgs')
input_image_dir = os.path.join(cur_dir, 'img_processing', 'input_imgs')
img_checkpoint_dir = os.path.join(cur_dir, 'img_processing', 'checkpoints')
img_proc_dir = os.path.join(cur_dir, 'img_processing')