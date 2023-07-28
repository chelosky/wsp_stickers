from dotenv import load_dotenv
from datetime import datetime
import os
import json
import redis

load_dotenv()

BASE_URL = 'https://raw.githubusercontent.com/chelosky/wsp_stickers/main/stickers';
STICKERS_NAME = {
    'nagatoro': "Please Don't Bully Me, Nagatoro"
}
REDIS_PREFIX_KEYS = {
    'review-count': 'rev-count',
    'review-sum': 'rev-sum',
    'download-count': 'download'
}
DEFAULT_PACK_INFO_VALUES = {
    'active': False,
    'animated': False,
    'description': 'Nagatoro Pack',
    'version': '1.0.0',
    'lastChangedAt': datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
}

STICKER_FOLDER = 'stickers';
PACK_INFO_FILE_NAME = 'pack_info.json'
JSON_FILE_NAME = 'data.json'
folder_path = "{os_path}/{sticker_folder}".format(os_path=os.getcwd(), sticker_folder=STICKER_FOLDER)

def generate_data(redisClient):
    app_packs = [{ 'path': os.path.join(folder_path, name), 'name': name } for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

    for app_pack in app_packs:
        unsorted_sticker_packs =[{ 'path': os.path.join(app_pack.get('path'), name), 'id': name } for name in os.listdir(app_pack.get('path')) if os.path.isdir(os.path.join(app_pack.get('path'), name))]
        sticker_packs = sorted(unsorted_sticker_packs,key=lambda x: int(x.get('id')))
        
        for sticker_pack in sticker_packs:
            file_path = sticker_pack.get('path')
            del sticker_pack['path']
            pacK_info = get_pack_information(file_path)
            base_sticker_url = '/'.join([BASE_URL, app_pack.get('name'), sticker_pack.get('id')])
            version = next(iter([ name.replace('.version', '') for name in os.listdir(file_path) if name.endswith('.version')]), None)
            stickers = [ { 'url': '/'.join([base_sticker_url, name]), 'size': os.stat(os.path.join(file_path, name)).st_size } for name in os.listdir(file_path) if name.endswith(".webp")]
            icon = '/'.join([base_sticker_url, 'icon.png'])
            sticker_pack['stickers'] = sorted(stickers, key=lambda x: int(x.get('url').split('/')[-1].split('.')[0]))
            sticker_pack['icon'] = icon
            sticker_pack['version'] = pacK_info.get('version')
            sticker_pack['animated'] = pacK_info.get('animated')
            name = "{sticker_pack_name} Pack {pack_id}".format(sticker_pack_name=app_pack.get('name').capitalize(), pack_id=sticker_pack.get('id'))
            sticker_pack['name'] = name
            pack_id =  "{sticker_pack_name}-{pack_id}".format(sticker_pack_name=app_pack.get('name').lower(), pack_id=sticker_pack.get('id'))
            sticker_pack['packId'] = pack_id
            sticker_pack['active'] = pacK_info.get('active')
            sticker_pack['lastChangedAt'] = pacK_info.get('lastChangedAt')
            sticker_pack['id'] =  sticker_pack.get('id')
        
            total_downloads = redisClient.get('{key}-{id}'.format(key=REDIS_PREFIX_KEYS['download-count'], id=pack_id))
            total_votes = redisClient.get('{key}-{id}'.format(key=REDIS_PREFIX_KEYS['review-count'], id=pack_id))
            sum_votes = redisClient.get('{key}-{id}'.format(key=REDIS_PREFIX_KEYS['review-sum'], id=pack_id))

            sticker_pack['downloads'] = int(total_downloads) if total_downloads != None else 0
            sticker_pack['voteCount'] = int(total_votes) if total_votes != None else 0
            sticker_pack['voteSum'] = int(sum_votes) if total_votes != None else 0
            sticker_pack['voteAverage'] = round(float(sticker_pack['voteSum'])/(int(total_votes) if total_votes != None else 1), 1)
            generate_json_file(file_path, sticker_pack)

        app_pack['id'] = app_pack.get('name')
        app_pack['name'] = STICKERS_NAME.get(app_pack.get('name'))
        original_sticker_packs = list(sticker_packs)
        app_pack['packs'] = list(map(map_to_app_file, sticker_packs))
        app_pack_path = app_pack.get('path')
        del app_pack['path']
        generate_json_file(app_pack_path, app_pack)
        app_pack['packs'] = original_sticker_packs
    
    return app_packs

def map_to_app_file(data):
    MAX_STICKERS = 5
    response = data.copy()
    response['stickers'] = response.get('stickers')[0:MAX_STICKERS]
    return response;

def generate_json_file(path, data, file_name = JSON_FILE_NAME):
    with open(os.path.join(path, file_name), "w") as outfile:
        outfile.write(json.dumps(data, indent=4))

def get_pack_information(path, file_name = PACK_INFO_FILE_NAME):
    file_path = os.path.join(path, file_name)
    pack_info = DEFAULT_PACK_INFO_VALUES;

    if not (os.path.isfile(file_path)):
        return pack_info

    with open(file_path, 'r') as f:
        pack_info = json.load(f)
    
    return {
        'active': pack_info.get('active') if pack_info.get('active') != None else DEFAULT_PACK_INFO_VALUES.get('active'),
        'version': pack_info.get('version') if pack_info.get('version') != None else DEFAULT_PACK_INFO_VALUES.get('version'),
        'animated': pack_info.get('animated') if pack_info.get('animated') != None else DEFAULT_PACK_INFO_VALUES.get('animated'),
        'description': pack_info.get('description') if pack_info.get('description') != None else DEFAULT_PACK_INFO_VALUES.get('description'),
        'lastChangedAt': pack_info.get('lastChangedAt') if pack_info.get('lastChangedAt') != None else DEFAULT_PACK_INFO_VALUES.get('lastChangedAt')
    }

def generate_redis_connection():
    return redis.Redis(
        host=os.environ["REDIS_HOST"], 
        port=os.environ["REDIS_PORT"], 
        username=os.environ["REDIS_USERNAME"],
        password=os.environ["REDIS_PASSWORD"],
        decode_responses=True
    )

if __name__ == '__main__':
    redis = generate_redis_connection()
    data = generate_data(redis)
    generate_json_file('.', data)
