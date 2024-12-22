import os
import json
from abc import ABC, abstractmethod


class JsonFileCreator(ABC):
        
    
    @abstractmethod
    def format_to_train(self, data):        
        pass
    
    
    @abstractmethod
    def format_to_evaluate(self, data):
        pass
    

    @abstractmethod
    def save_json(self, json_data, json_name, output_path):
        with open(os.path.join(output_path, json_name), 'w') as f:
            json.dump(json_data, f, indent=4)