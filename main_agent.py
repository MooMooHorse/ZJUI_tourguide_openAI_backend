import json
import paramiko
import time
from qa import integrated_mode

def read_users_data():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the remote server
        ssh.connect('47.96.152.177', username='root', password='JXBjxb123')
        
        # Read the users.json file
        stdin, stdout, stderr = ssh.exec_command('cat ~/ECE445/data/users.json')
        users_data = json.loads(stdout.read().decode('utf-8'))
        # if not users_data:
        #     raise Exception("Failed to read users data.")
        return users_data
    except paramiko.ssh_exception.AuthenticationException as e:
        print("Authentication failed:", e)
        return None
    except paramiko.ssh_exception.SSHException as e:
        print("SSH connection failed:", e)
        return None
    finally:
        ssh.close()

def write_users_data(data):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        ssh.connect('47.96.152.177', username='root', password='JXBjxb123')
        
        # Write the users.json file
        stdin, stdout, stderr = ssh.exec_command('echo \'{}\' > ~/ECE445/data/users.json'.format(json.dumps(data)))
        
        print("Users data written successfully.")
    except paramiko.ssh_exception.AuthenticationException as e:
        print("Authentication failed:", e)
        return None
    except paramiko.ssh_exception.SSHException as e:
        print("SSH connection failed:", e)
        return None
    finally:
        ssh.close()

def send_message_to_server(msg, ans):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        ssh.connect('47.96.152.177', username='root', password='JXBjxb123')

        # Construct the message to be sent
        message = json.dumps(msg)
        answer = json.dumps(ans)
        # Send the message to the server
        stdin, stdout, stderr = ssh.exec_command('echo {} >> ~/ECE445/data/messages.txt'.format(answer))
        # stdin, stdout, stderr = ssh.exec_command('echo \'{}\' > ~/ECE445/data/users.json'.format(message))


        print("Message sent successfully.")
    except paramiko.ssh_exception.AuthenticationException as e:
        print("Authentication failed:", e)
    except paramiko.ssh_exception.SSHException as e:
        print("SSH connection failed:", e)
    finally:
        ssh.close()


def print_users_data(users_data):
    for user in users_data:
        print(user)
    return


from typing import Tuple, List
def check_if_new_question(user, q_ID) -> Tuple[str, bool, str]:
    '''
        every time we poll, we check if the question is new. If it is new, we lateral to AI agent to answer the question.
        Return
        ------
        Question to answer
            str

        If the answer is new
            bool
        
        location of the user
    '''
    # gps = [user["gps_lat"], user["gps_lon"]]
    gps = [0, 0]
    if user["questionID"] == q_ID[user["userID"]]:
        print(q_ID[user["userID"]], user["questionID"])
        # process the question only if the instruction is "Submit"
        q_ID[user["userID"]] += 1
        if user["instruction"] != "Submit":
            return None, False, None
        else:
            return user["question"], True, user["uav_location"]

    return None, False, None

def main():
    users_data = read_users_data()
    q_ID = {}
    location_dict = {"RC 1": 0, 
                    "Business Street": 1, 
                    "North Teaching Building B": 2, 
                    "Luckin Coffee": 3, 
                    "Library": 4, 
                    "Clock Tower": 5, 
                    "Dining Hall": 6, 
                    "Qizhen Lake": 7}
    
    while(1):
        time.sleep(1)
        users_data = read_users_data()

        for user in users_data:
            if user["userID"] not in q_ID:
                q_ID[user["userID"]] = 0
            
            # print(q_ID[user["userID"]], user["questionID"])

            question, isNewQuestion, cur_loc = check_if_new_question(user, q_ID)  
            # convert index of location to string
            # uav_index should be the index of the location of the UAV

            '''
            Here is the place to lateral to the AI agent to answer the question
            '''    
            if isNewQuestion:
                print("New question:", question)
                # send the question to the AI agent
                ans, metadata = integrated_mode(question, cur_loc)
                if "operation" in metadata.keys():
                    operation = metadata["operation"]
                else:
                    operation = None
                # construct the message to be sent, there should be a newline character between the user and the answer
                user['answer'] = ans

                send_message_to_server(users_data, ans)

                if operation is not None:
                    # current version only handles the first operation
                    print(f'''receiving operation: {operation[0]}''')
                    operation = json.loads(operation[0])
                    user['instruction'] = list(operation['command'].keys())[0]
                    if operation['location'] is not None:
                        user['destination'] = operation['location']
                    user['questionID'] = user['questionID'] + 1
                    write_users_data(users_data)
    return


if __name__ == "__main__":
    main()

