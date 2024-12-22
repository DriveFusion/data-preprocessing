import numpy as np
import pandas as pd

from modules.json_file_creator import JsonFileCreator


class LingoJsonFileCreator(JsonFileCreator):

    
    def format_to_train(self, data: pd.DataFrame) -> list:
        json_data = []
        for _, group in data:
            segment_data = {
                'messages': [],
                'images': group['images'].iloc[0].tolist() 
                          if isinstance(group['images'].iloc[0], (list, np.ndarray)) 
                          else group['images'].iloc[0],
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