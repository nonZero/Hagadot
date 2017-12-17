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
    for i, seq in enumerate(seqs):
        if i > 0 and 'canvases' not in seq:
            # fetch full sequence data
            url = seq['@id']
            logger.debug(f"Getting sequence {url}")
            seq = requests.get(url).json()
        for c in seq['canvases']:
            assert c['@id'].startswith(API_ENDPOINT)
            imgs = c['images']
            assert (len(imgs)) == 1
            yield {
                'label': c['label'],
                'id': c['@id'][len(API_ENDPOINT):],
                'height': c['height'],
                'width': c['width'],
            }


def fix_pages(pages):
    """remove pdfs and add ordinals"""
    i = 1
    for p in pages:
        if p['height'] < 20 or p['width'] < 20:
            # PDF, skip
            logger.warning(f"Dropped page @id {p['id']}")
            continue
        yield dict(ordinal=i, **p)
        i += 1


def get_img_url(img_id, region='full', size='max', rotation='0'):
    return IMG_URL.format(id=img_id, region=region, size=size,
                          rotation=rotation)


def get_thumb_url(img_id, height):
    return get_img_url(img_id, size=f",{height}")
