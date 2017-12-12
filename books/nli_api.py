import logging

import requests

logger = logging.getLogger(__name__)

# Docs: http://iiif.nli.org.il/imageapi.html
API_ENDPOINT = "http://iiif.nli.org.il/IIIFv21/"

MANIFEST_URL = API_ENDPOINT + "DOCID/{}/manifest"
IMG_URL = API_ENDPOINT + "{id}/{region}/{size}/{rotation}/default.jpg"


def get_manifest(doc_id):
    url = MANIFEST_URL.format(doc_id)
    logger.debug(f"Getting {url}")
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def get_pages_from_manifest(doc):
    seqs = doc['sequences']
    assert len(seqs) == 1, len(seqs)
    for i, c in enumerate(seqs[0]['canvases']):
        assert c['@id'].startswith(API_ENDPOINT)
        imgs = c['images']
        assert (len(imgs)) == 1
        yield {
            'ordinal': i + 1,
            'label': c['label'],
            'id': c['@id'][len(API_ENDPOINT):],
            'height': c['height'],
            'width': c['width'],
        }


def get_img_url(img_id, region='full', size='max', rotation='0'):
    return IMG_URL.format(id=img_id, region=region, size=size,
                          rotation=rotation)


def get_thumb_url(img_id, height):
    return get_img_url(img_id, size=f",{height}")
