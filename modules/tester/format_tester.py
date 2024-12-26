import json

from utils import remove_tokens_messages


class FormatTester:
    
    
    @staticmethod
    def _consider_llama_or_llava_format(is_llama: bool):
        messages = 'messages' if is_llama == True else 'conversations'
        images = 'images' if is_llama == True else 'image'
        content = 'content' if is_llama == True else 'value'
        role = 'role' if is_llama == True else 'from'
        user = 'user' if is_llama == True else 'human'
        assistant = 'assistant' if is_llama == True else 'gpt'
        
        return messages, images, content, role, user, assistant
    
    
    @staticmethod
    def compare_questions(json_path, questions_list, tokens, is_eval, is_llama):
        messages, _, content, role, user, _ = FormatTester._consider_llama_or_llava_format(is_llama)
        with open(json_path, 'r') as f:
            json_data = json.load(f)

        questions_json = []
        if is_eval == True:
            for data in json_data:
                for message in data:
                    for content in message['content']:
                        if content['type'] == 'text':
                            questions_json.append(content['text'])
        else:
            for data in json_data:
                for message in data[messages]:
                    if message[role] == user:
                        questions_json.append(message[content])


        num_questions = len(questions_list)
        num_questions_json = len(questions_json)
        print(f'Number of questions in the dataset: {num_questions}')
        print(f'Number of questions in the JSON file: {num_questions_json}')
        if sorted(remove_tokens_messages(questions_list, tokens)) == sorted(remove_tokens_messages(questions_json, tokens)):
            print('They have the same questions.\n')
        else:
            print('They do not have the same questions.\n')
    
    
    @staticmethod
    def compare_answers(json_path, answers_list, is_eval, is_llama):
        messages, _, content, role, _, assistant = FormatTester._consider_llama_or_llava_format(is_llama)
        with open(json_path, 'r') as f:
            json_data = json.load(f)

        answers_json = []
        if is_eval == True:
            for data in json_data:
                for message in data:
                    for content in message['content']:
                        if content['type'] == 'text':
                            answers_json.append(content['answer'])
        else:
            for data in json_data:
                for message in data[messages]:
                    if message[role] == assistant:
                        answers_json.append(message[content])
        
        num_answers = len(answers_list)
        num_answers_json = len(answers_json)
        print(f'Number of answers in the dataset: {num_answers}')
        print(f'Number of answers in the JSON file: {num_answers_json}')
        if sorted(answers_list) == sorted(answers_json):
            print('They have the same answers.\n')
        else:
            print('They do not have the same answers.\n')
    
    
    @staticmethod
    def compare_videos(json_path, videos_list, to_remove, is_eval, is_llama):
        _, images, _, _, _, _ = FormatTester._consider_llama_or_llava_format(is_llama)
        
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        
        videos_json = set()
        if is_eval == True:
            for data in json_data:
                for message in data:
                    for content in message['content']:
                        if content['type'] == 'image':
                            videos_json.add(remove_tokens_messages(content['image'], to_remove))
                            break
        else:
            for data in json_data:
                videos_json.add(remove_tokens_messages(data[images], to_remove)[0])
                            
        num_videos = len(videos_list)
        num_videos_json = len(videos_json)
        print(f'Number of videos in the dataset: {num_videos}')
        print(f'Number of videos in the JSON file: {num_videos_json}')
        if sorted(videos_list) == sorted(videos_json):
            print('They have the same videos.\n')
        else:
            print('They do not have the same videos.\n')
            print(f'Real videos: {sorted(videos_list)}\n')
            print(f'Copied videos: {sorted(videos_json)}')