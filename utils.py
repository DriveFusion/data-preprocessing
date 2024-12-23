from IPython.display import display, HTML

import re
import os
import json
import shutil
import zipfile
import requests


def display_images(imgs, imgs_path):
    html_content = '<div style="display: flex; gap: 10px;">'
    
    for img in imgs:
        img_path = os.path.join(imgs_path, img)
        html_content += f'<img src="{img_path}" style="height: 200px;">'
    
    html_content += '</div>'
    display(HTML(html_content))


def compare_num_questions(json_path, questions_lst, is_eval=False):
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
            for message in data['messages']:
                if message['role'] == 'user':
                    questions_json.append(message['content'])


    num_questions = len(questions_lst)
    num_questions_json = len(questions_json)
    print(f'Number of questions in the dataset: {num_questions}')
    print(f'Number of questions in the JSON file: {num_questions_json}')
    if sorted(questions_lst) == sorted(questions_json):
        print('They have the same questions.\n')
    else:
        print('They do not have the same questions.\n')
        

def compare_num_answers(json_path, answers_lst, is_eval=False):
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
            for message in data['messages']:
                if message['role'] == 'assistant':
                    answers_json.append(message['content'])
    
    num_answers = len(answers_lst)
    num_answers_json = len(answers_json)
    print(f'Number of answers in the dataset: {num_answers}')
    print(f'Number of answers in the JSON file: {num_answers_json}')
    if sorted(answers_lst) == sorted(answers_json):
        print('They have the same answers.\n')
    else:
        print('They do not have the same answers.\n')
    
    
def compare_num_videos(json_path, videos_lst, replace_this='', is_eval=False):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    videos_json = set()
    if is_eval == True:
        for data in json_data:
            for message in data:
                for content in message['content']:
                    if content['type'] == 'image':
                        videos_json.add(content['image'].replace(replace_this, ''))
                        break
    else:
        for data in json_data:
            videos_json.add(data['images'][0].replace(replace_this, ''))
                        
    num_videos = len(videos_lst)
    num_videos_json = len(videos_json)
    print(f'Number of videos in the dataset: {num_videos}')
    print(f'Number of videos in the JSON file: {num_videos_json}')
    if sorted(videos_lst) == sorted(videos_json):
        print('They have the same videos.\n')
    else:
        print('They do not have the same videos.\n')
        print(f'Real videos: {sorted(videos_lst)}\n')
        print(f'Copied videos: {sorted(videos_json)}')
    

def add_token(json_path, token):
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    for data in json_data:
        for message in data['messages']:
            message['content'] = token * len(data['images']) + message['content']
            break
    
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=4)
    

def remove_tokens(json_path, tokens):
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    
    pattern = '|'.join(re.escape(token) for token in tokens)
    for data in json_data:
        for message in data['messages']:
            message['content'] = re.sub(pattern, '', message['content'])

    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=4)


def bdd_x_videos_filtration(text_file_path, 
                            unzip_path,
                            filtered_video_path,
                            download_output_path, 
                            download_link, 
                            dataset_type,
                            download_len,                        
    ):
    os.makedirs(filtered_video_path, exist_ok=True)
    os.makedirs(download_output_path, exist_ok=True)
    os.makedirs(unzip_path, exist_ok=True)
    
    train_path = os.path.join(text_file_path, 'train.txt')
    test_path = os.path.join(text_file_path, 'test.txt')
    val_path = os.path.join(text_file_path, 'val.txt')
    with open(train_path, 'r') as f:
        train_data = f.read().splitlines()
        train_data = [item.split('_')[-1] for item in train_data]
    with open(test_path, 'r') as f:
        test_data = f.read().splitlines()
        test_data = [item.split('_')[-1] for item in test_data]
    with open(val_path, 'r') as f:
        val_data = f.read().splitlines()
        val_data = [item.split('_')[-1] for item in val_data]
    
    data = train_data + test_data + val_data
    print(f'Training data size: {len(train_data)}\nTesting data size: {len(test_data)}\nValidation data size: {len(val_data)}\n')
    print(f'Data size: {len(data)}')
        
    filtered_videos = []
    for i in range(download_len):
        updated_download_link = download_link.replace(f'{dataset_type}_00', f'{dataset_type}_{i:02d}')
        filename = updated_download_link.split('/')[-1]
        file_path = os.path.join(download_output_path, filename)
        
        try:
            print(f'Downloading: {filename}')
            response = requests.get(updated_download_link, stream=True)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f'Downloaded: {file_path}')
            
            print(f"Unzipping: {file_path} to {unzip_path}")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
            print(f"Unzipped: {file_path}")
            
            os.remove(file_path)
            print(f'Deleted zip file: {file_path}')
        except requests.exceptions.RequestException as e:
            print(f'Failed to download {updated_download_link}: {e}')
        except zipfile.BadZipFile as e:
            print(f"Failed to unzip {file_path}: {e}")
        
        moved_videos = 0
        video_folder_path = os.path.join(unzip_path, f'bdd100k/videos/{dataset_type}')
        for video in os.listdir(video_folder_path):
            video_name = video.split('.')[0]
            if video_name in data:
                moved_videos += 1
                current_video_path = os.path.join(video_folder_path, video_name+'.mov')
                if video_name in filtered_videos:
                    filtered_video_dist_path = os.path.join(filtered_video_path, video_name+f'_{len(filtered_videos)}'+'.mov')
                    video_name = video_name + f'_{len(filtered_videos)}'
                else:
                    filtered_video_dist_path = os.path.join(filtered_video_path, video_name+'.mov')
                filtered_videos.append(video_name)
                shutil.move(current_video_path, filtered_video_dist_path)
        shutil.rmtree(video_folder_path)
        print(f'Filtered videos from download {i}: {moved_videos}')
        print(f'Number of filtered videos: {len(filtered_videos)}')
        
    print(f'Finished filtering all videos')
        
        
