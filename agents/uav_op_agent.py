import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from genai.itf import initialize_env
from openai import OpenAI
from paths import data_dir, agents_config_dir
from genai.itf import OpenAIITF
from paths import prompt_dir
import re
import json

class UAVOPAgent():
    def __init__(self, OpenAI_itf:OpenAIITF = None):
        self.OpenAI_itf = OpenAI_itf

    def query(self, query:str, prompt = 'uav_op_agent.prompt'):
        with open(os.path.join(prompt_dir, prompt), 'r') as f:
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
        return self.ground_result(self.OpenAI_itf.get_chat_completion_content(message_list, temperature=0))
    def ground_result(self, result:str):
        '''
            We first only look at the content in the first { and last }.
            We then use regex to extract the command and location from the content.
            We then check if the command and location are in the command dict and location dict.
            The result  should be in the following format
            {
                "command": <COMMAND>,
                "location": <LOCATION>
            }

            The location is null when the command is not related to the location.

            The command is Default when 
            1. the command is not in the command dict
            2. there are more than one command in the question

            The value of <COMMAND>, <LOCATION> can be 
            
            command = {"Default": 0, "Takeoff": 1, "Land": 2, "Start":3, "Stop": 4, "Continue": 5}

            location = {"RC 1": 0, 
                     "Business Street": 1, 
                     "North Teaching Building B": 2, 
                     "Luckin Coffee": 3, 
                     "Library": 4, 
                     "Clock Tower": 5, 
                     "Dining Hall": 6, 
                     "Qizhen Lake": 7
            }

            Examples
            --------
            {
                "command": {"Start": 3}
                "location": {"North Teaching Building B": 2}
            }

            {
                "command": {"Default": 0}
                "location": null
            }

        '''

        # Extract the content in the first { and last }
        content = result[result.find('{')+1:result.rfind('}')]
        # Extract the command and location
        command = None
        location = None
        try:
            command = re.search(r'"command":\s*{"(.*?)"', content).group(1)
        except:
            return None
        try:
            location = re.search(r'"location":\s*{"(.*?)"', content).group(1)
        except:
            location = None

        import yaml

        with open(os.path.join(agents_config_dir, 'uav_op_agent.yaml'), 'r') as infile:
            data = yaml.safe_load(infile)

        command_dict = data['command']
        location_dict = data['location']
        if command not in command_dict:
            return None
        if location is not None and location not in location_dict:
            return None
        command = {command: command_dict[command]}

        if location is None:
            return json.dumps({"command": command, "location": None})
        else:
            return json.dumps({"command": command, "location": {location: location_dict[location]}})
        

if __name__ == "__main__":
    itf = OpenAIITF()
    agent = UAVOPAgent("ZJUI Building", itf)
    print(agent.query("Take off the drone"))
    print(agent.query("Land the drone"))
    print(agent.query("Fly the drone to the library"))
