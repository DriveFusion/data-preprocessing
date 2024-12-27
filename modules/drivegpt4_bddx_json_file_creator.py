
import os

from modules.json_file_creator import JsonFileCreator


class LlamaDriveGPT4BDDXJsonFileCreator(JsonFileCreator):
    
    
    def __init__(self, img_path: str=''):
        super().__init__(img_path)
    

    def format_to_train_single_question(self, data: list, token: str='') -> list:
        json_data = []
        for item in data:
            conv = item['conversations']
            for i in range(0, len(conv)-1, 2):
                segment_data = {
                    'messages': [],
                    'images': []
                }
                img_name = item['image'].replace('.png', '')
                for idx in item['idx_list']:
                    segment_data['images'].append(
                        os.path.join(self.img_path, img_name + f'_{idx}.png')
                    )
                if conv[i]['from'] == 'human' and conv[i+1]['from'] == 'gpt':
                    question = conv[i]['value']
                    answer = conv[i+1]['value']
                    segment_data['messages'].append({
                        'content': token * len(segment_data['images']) + question,
                        'role': 'user'
                    })
                    segment_data['messages'].append({
                        'content': answer,
                        'role': 'assistant'
                    })
                    json_data.append(segment_data)

        return json_data


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
    

    def format_to_train_single_question(self, data: list, token: str='') -> list:
        json_data = []
        for item in data:
            conv = item['conversations']
            for i in range(0, len(conv)-1, 2):
                segment_data = {
                    'id': item['id'],
                    'image': [],
                    'conversations': []
                }
                img_name = item['image'].replace('.png', '')
                for idx in item['idx_list']:
                    segment_data['image'].append(
                        os.path.join(self.img_path, img_name + f'_{idx}.png')
                    )
                if conv[i]['from'] == 'human' and conv[i+1]['from'] == 'gpt':
                    question = conv[i]['value']
                    answer = conv[i+1]['value']
                    segment_data['conversations'].append({
                        'from': 'human',
                        'value': token * len(segment_data['image']) + question
                    })
                    segment_data['conversations'].append({
                        'from': 'gpt',
                        'value': answer,
                    })
                    json_data.append(segment_data)

        return json_data
        

    def format_to_train_mutli_question(self, data: list) -> list:
        json_data = []
        visited_imgs = {}
        for item in data:
            segment_data = {
                'id': item['id'],
                'image': [],
                'conversations': []
            }
            img_name = item['image'].replace('.png', '')
            if img_name in visited_imgs:
                img_idx = visited_imgs[img_name]
                for conv in item['conversations']:
                    if conv['from']  == 'human':
                        json_data[img_idx]['conversations'].append({
                            'from': 'human',
                            'value': conv['value']
                        })
                    else:
                        json_data[img_idx]['conversations'].append({
                            'from': 'gpt',
                            'value': conv['value']
                        })
            else:
                for idx in item['idx_list']:
                    segment_data['image'].append(
                        os.path.join(self.img_path, img_name + f'_{idx}.png')
                    )
                for conv in item['conversations']:
                    if conv['from'] == 'human':
                        segment_data['conversations'].append({
                            'from': 'human',
                            'value': conv['value']
                        })
                    else:
                        segment_data['conversations'].append({
                            'from': 'gpt',
                            'value': conv['value']
                        })
                json_data.append(segment_data)
                visited_imgs[img_name] = len(json_data) - 1

        return json_data
    
    
    def format_to_evaluate(self, data: list) -> list:
        super().format_to_evaluate(data)
    

    def save_json(self, json_data: list, json_name: str, output_path: str) -> None:
        super().save_json(json_data, json_name, output_path)