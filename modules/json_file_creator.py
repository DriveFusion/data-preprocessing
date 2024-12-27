import os
import json
from abc import ABC, abstractmethod


class JsonFileCreator(ABC):
    
    
    def __init__(self, img_path):
        self.img_path = img_path
        
    
    @abstractmethod
    def format_to_train_single_question(self, data, token):
        pass
    
    
    @abstractmethod
    def format_to_train_mutli_question(self, data):
        pass
    
    
    @abstractmethod
    def format_to_evaluate(self, data):
        pass
    

    @abstractmethod
    def save_json(self, json_data, json_name, output_path):
        with open(os.path.join(output_path, json_name), 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)