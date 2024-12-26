import pandas as pd

import os

from modules.json_file_creator import JsonFileCreator


class LlamaLingoJsonFileCreator(JsonFileCreator):


    def __init__(self, img_path: str=''):
        super().__init__(img_path)

    
    def format_to_train_single_question(self, data: pd.DataFrame, token: str='') -> list:
        json_data = []
        for _, row in data.iterrows():
            imgs = [os.path.join(self.img_path, img) for img in row['images']]
            segment_data = {
                'messages': [],
                'images': imgs
            }
            segment_data['messages'].append({
                'content': token * len(imgs) + row['question'],
                'role': 'user'
            })
            segment_data['messages'].append({
                'content': row['answer'],
                'role': 'assistant'
            })
            json_data.append(segment_data)
        
        return json_data
    
    
    def format_to_train_mutli_question(self, data: pd.DataFrame) -> list:
        json_data = []
        for _, group in data:
            imgs = [os.path.join(self.img_path, img) for img in group['images'].iloc[0]]
            segment_data = {
                'messages': [],
                'images': imgs
                # 'images': group['images'].iloc[0].tolist() 
                #           if isinstance(group['images'].iloc[0], (list, np.ndarray)) 
                #           else group['images'].iloc[0],
            }
            
            for _, row in group.iterrows():                
                segment_data['messages'].append({
                    'content': row['question'],
                    'role': 'user'
                })                
                segment_data['messages'].append({
                    'content': row['answer'],
                    'role': 'assistant'
                })       
            json_data.append(segment_data)                
        
        return json_data
    
    
    def format_to_evaluate(self, data: pd.DataFrame) -> list:
        json_data = []
        for _, row in data.iterrows():
            message = []
            content = []
            for img in row['images']:
                content.append({
                    'type': 'image',
                    'image': img
                })
            content.append({
                'type': 'text',
                'text': row['question'],
                'answer': row['answer']
            })
            message.append({
                'role': 'user',
                'content': content
            })
            json_data.append(message)
        
        return json_data
        
    
    def save_json(self, json_data: list, json_name: str, output_path: str) -> None:
        super().save_json(json_data, json_name, output_path)
        
    
    
class LlavaLingoJsonFileCreator(LlamaLingoJsonFileCreator, JsonFileCreator):
    
    
    def __init__(self, img_path: str=''):
        super().__init__(img_path)
    
        
    def format_to_train_single_question(self, data: pd.DataFrame, token: str='') -> list:
        json_data = []
        for _, row in data.iterrows():
            imgs = [os.path.join(self.img_path, img) for img in row['images']]
            segment_data = {
                'id': row['segment_id'],
                'image': imgs,
                'conversations': []
            }
            segment_data['conversations'].append({
                'from': 'human',
                'value': token * len(imgs) + row['question'],
            })
            segment_data['conversations'].append({
                'from': 'gpt',
                'value': row['answer'],
            })
            json_data.append(segment_data)
        
        return json_data
    
    
    def format_to_train_mutli_question(self, data: pd.DataFrame, token: str='') -> list:
        json_data = []
        for segment_id, group in data:
            imgs = [os.path.join(self.img_path, img) for img in group['images'].iloc[0]]
            segment_data = {
                'id': segment_id,
                'image': imgs,
                'conversations': []
                # 'images': group['images'].iloc[0].tolist() 
                #           if isinstance(group['images'].iloc[0], (list, np.ndarray)) 
                #           else group['images'].iloc[0],
            }
            
            for _, row in group.iterrows():                
                segment_data['conversations'].append({
                    'from': 'human',
                    'value': token * len(imgs) + row['question'],
                })                
                segment_data['conversations'].append({
                    'from': 'gpt',
                    'value': row['answer'],
                })       
            json_data.append(segment_data)                
        
        return json_data
    
    
    def format_to_evaluate(self, data: pd.DataFrame) -> list:
        super().format_to_evaluate(data)
        
    
    def save_json(self, json_data: list, json_name: str, output_path: str) -> None:
        super().save_json(json_data, json_name, output_path)