
import os

from modules.json_file_creator import JsonFileCreator


class LlamaDriveGPT4BDDXJsonFileCreator(JsonFileCreator):
    
    
    def __init__(self, img_path: str=''):
        super().__init__(img_path)
    

    def format_to_train_single_question(self, data: list, token: str='') -> list:
        json_data = []
        


    def format_to_train_mutli_question(self, data: list) -> list:
        json_data = []
        visited_imgs = {}
        for item in data:
            segment_data = {
                'messages': [],
                'images': []
            }
            img_name = item['image'].replace('.png', '')
            if img_name in visited_imgs:
                img_idx = visited_imgs[img_name]
                for conv in item['conversations']:
                    if conv['from']  == 'human':
                        json_data[img_idx]['messages'].append({
                            'content': conv['value'],
                            'role': 'user'
                        })
                    else:
                        json_data[img_idx]['messages'].append({
                            'content': conv['value'],
                            'role': 'assistant'
                        })
            else:
                for idx in item['idx_list']:
                    segment_data['images'].append(
                        os.path.join(self.img_path, img_name + f'_{idx}.png')
                    )
                for conv in item['conversations']:
                    if conv['from'] == 'human':
                        segment_data['messages'].append({
                            'content': conv['value'],
                            'role': 'user'
                        })
                    else:
                        segment_data['messages'].append({
                            'content': conv['value'],
                            'role': 'assistant'
                        })
                json_data.append(segment_data)
                visited_imgs[img_name] = len(json_data) - 1

        return json_data
    
    
    def format_to_evaluate(self, data: list) -> list:
        json_data = []
        for item in data:
            message = []
            content = []
            for idx in item['idx_list']:
                content.append({
                    'type': 'image',
                    'image': item['image'].replace('.png', '') + f'_{idx}.png'
                })
            for conv in item['conversations']:
                if conv['from'] == 'human':    
                    content.append({
                        'type': 'text',
                        'text': conv['value']
                    })
                else:
                    content[-1]['answer'] = conv['value']
                    
            message.append({
                'role': 'user',
                'content': content
            })
            json_data.append(message)
        
        return json_data
    

    def save_json(self, json_data: list, json_name: str, output_path: str) -> None:
        super().save_json(json_data, json_name, output_path)


class LlavaDriveGPT4BDDXJsonFileCreator(LlamaDriveGPT4BDDXJsonFileCreator, JsonFileCreator):
    
    
    def __init__(self, img_path: str=''):
        super().__init__(img_path)
    

    def format_to_train(self, data: list) -> list:
        json_data = []
        visited_imgs = {}
        for item in data:
            segment_data = {
                'id': '', # Need to be added
                'messages': [],
                'images': []
            }
            img_name = item['image'].replace('.png', '')
            if img_name in visited_imgs:
                img_idx = visited_imgs[img_name]
                for conv in item['conversations']:
                    if conv['from']  == 'human':
                        json_data[img_idx]['messages'].append({
                            'content': conv['value'],
                            'role': 'user'
                        })
                    else:
                        json_data[img_idx]['messages'].append({
                            'content': conv['value'],
                            'role': 'assistant'
                        })
            else:
                for idx in item['idx_list']:
                    segment_data['images'].append(
                        os.path.join(self.img_path, img_name + f'_{idx}.png')
                    )
                for conv in item['conversations']:
                    if conv['from'] == 'human':
                        segment_data['messages'].append({
                            'content': conv['value'],
                            'role': 'user'
                        })
                    else:
                        segment_data['messages'].append({
                            'content': conv['value'],
                            'role': 'assistant'
                        })
                json_data.append(segment_data)
                visited_imgs[img_name] = len(json_data) - 1

        return json_data
    
    
    def format_to_evaluate(self, data: list) -> list:
        json_data = []
        for item in data:
            message = []
            content = []
            for idx in item['idx_list']:
                content.append({
                    'type': 'image',
                    'image': item['image'].replace('.png', '') + f'_{idx}.png'
                })
            for conv in item['conversations']:
                if conv['from'] == 'human':    
                    content.append({
                        'type': 'text',
                        'text': conv['value']
                    })
                else:
                    content[-1]['answer'] = conv['value']
                    
            message.append({
                'role': 'user',
                'content': content
            })
            json_data.append(message)
        
        return json_data
    

    def save_json(self, json_data: list, json_name: str, output_path: str) -> None:
        super().save_json(json_data, json_name, output_path)