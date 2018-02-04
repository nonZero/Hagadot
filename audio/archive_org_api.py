import requests
from urllib.parse import quote, quote_plus


def get_audio_info(details_url, format="VBR MP3"):
    id = details_url.split("/")[-1]
    metadata_url = "http://archive.org/metadata/" + id

    data = requests.get(metadata_url).json()

    for d in data['files']:
        if d['format'] == format:
            name = quote(d['name'])
            return {
                'title': data['metadata']['title'],
                'description': data['metadata']['description'],
                'url': f'http://archive.org/download/{id}/{name}',
                'length': d['length'],
            }

    return None
