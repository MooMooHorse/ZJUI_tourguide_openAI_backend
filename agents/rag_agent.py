import sys
import os 
cur_file_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(cur_file_path))
from genai.itf import initialize_env
from openai import OpenAI
from paths import data_dir
class RAGAgent():
    def __init__(self, vector_store_id = None, assistant_id = None):
        initialize_env()
        self.client = OpenAI()
        if assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id)
        else:
            self.assistant = self.client.beta.assistants.create(
                name="Campus Tour Guide assistant",
                instructions="You are an campus tour guide to ZJU-UIUC campus. Use you knowledge base to answer questions about ZJU-UIUC campus.",
                model="gpt-3.5-turbo",
                tools=[{"type": "file_search"}],
            )
        if vector_store_id:
            self.update_vector_store_to_assistant(vector_store_id)
    def create_vector_store(self, file_paths):
        # Create a vector store caled "ZJU-UIUC campus knowledge base"
        vector_store = self.client.beta.vector_stores.create(name="ZJU-UIUC campus knowledge base")
        
        file_streams = [open(path, "rb") for path in file_paths if path.endswith(".pdf") or path.endswith(".txt")]
        # Use the upload and poll SDK helper to upload the files, add them to the vector store,
        # and poll the status of the file batch for completion.
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )
        
        # You can print the status and the file counts of the batch to see the result of this operation.
        print(file_batch.status)
        print(file_batch.file_counts)
        return self.update_vector_store_to_assistant(vector_store.id)
    
    def update_vector_store_to_assistant(self, vector_store_id):
        self.assistant = self.client.beta.assistants.update(
            assistant_id=self.assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
        )
        return vector_store_id

    def query(self, query:str):
        # Use the create and poll SDK helper to create a run and poll the status of
        # the run until it's in a terminal state.

        # Create a thread and attach the file to the message
        thread = self.client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": query
                }
            ]
        )

        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id, assistant_id=self.assistant.id
        )

        messages = list(self.client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

        message_content = messages[0].content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = self.client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))

if __name__ == "__main__":
    
    agent = RAGAgent(vector_store_id='vs_8tnCdtj3clgKx6YpTLK7zAY0', assistant_id='asst_Mtl023T90q5z9CylR5F2V6n6')
    agent.query("How many books are in ZJU-UIUC's library?")