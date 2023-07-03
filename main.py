import os
import json

BASE_URL = 'https://raw.githubusercontent.com/chelosky/wsp_stickers/main/stickers';
STICKERS_NAME = {
    'nagatoro': "Please Don't Bully Me, Nagatoro"
}
ANIMATED_PACK_FILE_NAME = 'is_animated.dmy'
STICKER_FOLDER = 'stickers';
JSON_FILE_NAME = 'data.json'
folder_path = "{os_path}/{sticker_folder}".format(os_path=os.getcwd(), sticker_folder=STICKER_FOLDER)

def generate_data():
    app_packs = [{ 'path': os.path.join(folder_path, name), 'name': name } for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

    for app_pack in app_packs:
        unsorted_sticker_packs =[{ 'path': os.path.join(app_pack.get('path'), name), 'id': name } for name in os.listdir(app_pack.get('path')) if os.path.isdir(os.path.join(app_pack.get('path'), name))]
        sticker_packs = sorted(unsorted_sticker_packs,key=lambda x: int(x.get('id')))
        
        for sticker_pack in sticker_packs:
            base_sticker_url = '/'.join([BASE_URL, app_pack.get('name'), sticker_pack.get('id')])
            stickers = [ '/'.join([base_sticker_url, name]) for name in os.listdir(sticker_pack.get('path')) if name.split('.')[-1] == 'webp']
            icon = '/'.join([base_sticker_url, 'icon.png'])
            sticker_pack['stickers'] = sorted(stickers, key=lambda x: int(x.split('/')[-1].split('.')[0]))
            sticker_pack['icon'] = icon
            sticker_pack['animated'] = os.path.isfile(os.path.join(sticker_pack.get('path'), ANIMATED_PACK_FILE_NAME))
            sticker_pack['name'] = "{sticker_pack_name} Pack {pack_id}".format(sticker_pack_name=app_pack.get('name').capitalize(), pack_id=sticker_pack.get('id'))
            sticker_pack['alternativeId'] =  "{sticker_pack_name}_{pack_id}".format(sticker_pack_name=app_pack.get('name').lower(), pack_id=sticker_pack.get('id'))
            sticker_pack['id'] =  int(sticker_pack.get('id'))
            file_path = sticker_pack.get('path')
            del sticker_pack['path']
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

if __name__ == '__main__':
    response = generate_data()
    generate_json_file('.', response)
