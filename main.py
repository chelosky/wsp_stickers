import os
import json

BASE_URL = 'https://raw.githubusercontent.com/chelosky/wsp_stickers/main';
STICKERS_NAME = {
    'nagatoro': "Please Don't Bully Me, Nagatoro"
}
STICKER_FOLDER = 'stickers';
JSON_FILE_NAME = 'data.json'
folder_path = "{os_path}/{sticker_folder}".format(os_path=os.getcwd(), sticker_folder=STICKER_FOLDER)

def generate_data():
    sub_folders_paths = [{ 'path': os.path.join(folder_path, name), 'name': name } for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

    for sub_folder_path in sub_folders_paths:
        unsorted_sticker_packs_paths =[{ 'path': os.path.join(sub_folder_path.get('path'), name), 'id': name } for name in os.listdir(sub_folder_path.get('path')) if os.path.isdir(os.path.join(sub_folder_path.get('path'), name))]
        sticker_packs_paths = sorted(unsorted_sticker_packs_paths,key=lambda x: int(x.get('id')))
        for sticker_pack_path in sticker_packs_paths:
            base_sticker_url = '/'.join([BASE_URL, sub_folder_path.get('name'), sticker_pack_path.get('id')])
            stickers = [ '/'.join([base_sticker_url, name]) for name in os.listdir(sticker_pack_path.get('path')) if name.split('.')[-1] == 'webp']
            icon = '/'.join([base_sticker_url, 'icon.png'])
            sticker_pack_path['stickers'] = stickers
            sticker_pack_path['icon'] = icon
            sticker_pack_path['name'] = "{sticker_pack_name} PACK {pack_id}".format(sticker_pack_name=sub_folder_path.get('name').upper(), pack_id=sticker_pack_path.get('id'))
            sticker_pack_path['id'] =  "{sticker_pack_name}_{pack_id}".format(sticker_pack_name=sub_folder_path.get('name'), pack_id=sticker_pack_path.get('id'))
            del sticker_pack_path['path']
        sub_folder_path['name'] = STICKERS_NAME.get(sub_folder_path.get('name'))
        sub_folder_path['packs'] = sticker_packs_paths
        del sub_folder_path['path']
    return sub_folders_paths

def generate_json_file(data):
    with open(JSON_FILE_NAME, "w") as outfile:
        outfile.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    response = generate_data()
    generate_json_file(response)