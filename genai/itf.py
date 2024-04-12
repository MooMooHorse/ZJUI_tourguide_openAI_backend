from typing import Dict, List
import os
import sys
import numpy as np
from tqdm import tqdm 
cur_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname((cur_dir)))
from paths import openai_config_path, openai_env_path
from genai.logger import OpenAI_Logger

class OpenAIITF():
    def __init__(self):
        self.initialize_env()
        self.logger = OpenAI_Logger()
        
    def get_chat_completion(self, messages, model="gpt-3.5-turbo", max_tokens=150, temperature=0.7, 
                            top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, 
                            stop=None):
        """
            Returns the completion of a chat given a list of messages.
            Source:
                https://platform.openai.com/docs/guides/text-generation/managing-tokens
        """
        from openai import OpenAI
        client = OpenAI()
        return client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop
        )
    def get_embeddings(self, texts: List[str], model="text-embedding-3-small") -> np.ndarray:
        '''
        Get the embeddings of the texts using the model specified.
        
        Source:
            https://platform.openai.com/docs/guides/embeddings/use-cases
        '''
        def _get_embedding(text, client, model):
            text = text.replace("\n", " ")
            return client.embeddings.create(input = [text], model=model).data[0].embedding
        from openai import OpenAI
        client = OpenAI()
        embeddings = []
        for text in texts:
            embeddings.append(_get_embedding(text, client, model))
        return np.array(embeddings)
    
    def get_chat_completion_content(self, messages, model="gpt-3.5-turbo", max_tokens=150, temperature=0.7,
                                    top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0, stop=None):
        """
            Returns the content of the completion of a chat given a list of messages.

            Side-effect
            -----------
            get_chat_completion() might throw an exception, it MUST be handled by the caller.

            This allows customized error handling to help the experimentations.
        """
        completion =  self.get_chat_completion(messages, model, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, stop)
        content = completion.choices[0].message.content
        self.logger.log_message(str(completion))
        self.logger.update_statistics(completion.usage.total_tokens, 
                                      completion.usage.completion_tokens, 
                                      completion.usage.prompt_tokens,
                                      is_called=1)
        return content
    
    def initialize_env(self):
        """
            Initializes the OpenAI environment.
            
            Side-effect
            -----------
            Sets the environment variable OPENAI_API_KEY.
        """
        import openai, json
        with open(openai_config_path, "r") as f:
            config = json.load(f)
        with open(openai_env_path, "r") as f:
            env = json.load(f)

        openai.api_key = config["api_key"]
        # set the environment variable
        os.environ["https_proxy"] = env["https_proxy"]
        os.environ["OPENAI_API_KEY"] = config["api_key"]

    
def test_1():
    itf = OpenAIITF()
    itf.initialize_env()
    messages = [
        {"role": "system", "content" : "Hello, how are you doing today?"}
    ]
    print(messages)
    print(itf.get_chat_completion_content(messages, temperature=0))

if __name__ == '__main__':
    test_1()

