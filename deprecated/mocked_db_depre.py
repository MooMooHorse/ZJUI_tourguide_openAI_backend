# import os
# import sys
# cur_file_path = os.path.abspath(os.path.dirname(__file__))
# sys.path.append(os.path.dirname(cur_file_path))
# from genai.itf import OpenAIITF
# from paths import prompt_dir, data_dir
# import json
# from tqdm import tqdm
# class MockedDB():
#     def __init__(self):
#         pass

#     def vectorize_nodes(self, itf: OpenAIITF = None):
#         '''
#             Vectorize the nodes in the data directory.
            
#             Side-Effect
#             ------------
#             The .json node files in the data directory will be modified.
#         '''
#         files = os.listdir(data_dir)
#         if itf is None:
#             itf = OpenAIITF()
#         for file in tqdm(files, desc="Vectorizing nodes"):
#             if file.endswith(".json"):
#                 with open(os.path.join(data_dir, file), 'r') as f:
#                     node = json.load(f)
                
#                 node['location_embedding'] = itf.get_embeddings([node['location']])[0]
#                 node['keyword_embedding'] = itf.get_embeddings([node['keyword']])[0] 
#                 node['outlook_embedding'] = itf.get_embeddings([node['outlook']])[0]

#                 with open(os.path.join(data_dir, file), 'w') as f:
#                     json.dump(node, f)
    


#     def retrieve_nodes(self, embedding_field = 'keyword_embedding', itf: OpenAIITF = None):
#         '''
#             Retrieve the nodes in the data directory.
            
#             Returns
#             -------
#             List[Dict]
#                 A list of nodes in the data directory.
#         '''
#         files = os.listdir(data_dir)
#         if itf is None:
#             itf = OpenAIITF()
#         nodes = []
#         for file in tqdm(files, desc="Retrieving nodes"):
#             if file.endswith(".json"):
#                 with open(os.path.join(data_dir, file), 'r') as f:
#                     node = json.load(f)
#                 nodes.append(node)
        
