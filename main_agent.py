import json
import paramiko
import time

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

def send_message_to_server(msg):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        ssh.connect('47.96.152.177', username='root', password='JXBjxb123')

        # Construct the message to be sent
        message = json.dumps(msg)

        # Send the message to the server
        stdin, stdout, stderr = ssh.exec_command('echo {} >> ~/ECE445/data/messages.txt'.format(message))

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
def check_if_new_question(user, q_ID) -> Tuple[str, bool, List]:
    '''
        every time we poll, we check if the question is new. If it is new, we lateral to AI agent to answer the question.
        Return
        ------
        Question to answer
            str

        If the answer is new
            bool
        
        gps of the client
            List
    '''
    # gps = [user["gps_lat"], user["gps_lon"]]
    gps = [0, 0]
    if user["questionID"] == q_ID[user["userID"]]:
        # process the question only if the instruction is "Submit"
        q_ID[user["userID"]] += 1
        if user["instruction"] != "Submit":
            return None, False, None
        else:
            return user["question"], True, gps

    return None, False, None

def main():
    users_data = read_users_data()
    ans = "Here is the answer to your question."
    q_ID = {}
    while(1):
        time.sleep(1)
        users_data = read_users_data()

        for user in users_data:
            if user["userID"] not in q_ID:
                q_ID[user["userID"]] = 0
            
            # print(q_ID[user["userID"]], user["questionID"])

            question, isNewQuestion, gps = check_if_new_question(user, q_ID)  

            '''
            Here is the place to lateral to the AI agent to answer the question
            '''    
            if isNewQuestion:
                print("New question:", question)
                # send the question to the AI agent
                ans = "Here is the answer to your question."  # replace this with the answer from the AI agent
                print(ans)
            
                # send the answer to the server
                send_message_to_server(ans)     
            
    return


if __name__ == "__main__":
    main()

