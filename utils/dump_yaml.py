import yaml

command_dict = {"Default": 0, "Takeoff": 1, "Land": 2, "Start":3, "Stop": 4, "Continue": 5}
location_dict = {"RC 1": 0, 
                 "Business Street": 1, 
                 "North Teaching Building B": 2, 
                 "Luckin Coffee": 3, 
                 "Library": 4, 
                 "Clock Tower": 5, 
                 "Dining Hall": 6, 
                 "Qizhen Lake": 7
                }

data = {'command': command_dict, 'location': location_dict}

with open('data.yaml', 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)