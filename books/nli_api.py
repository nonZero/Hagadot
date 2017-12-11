import requests

MANIFEST_URL = "http://iiif.nli.org.il/IIIFv21/DOCID/{}/manifest"

# http://iiif.nli.org.il/imageapi.html
IMG_API_URL = "http://iiif.nli.org.il/IIIFv21/"

IMG_URL = "http://iiif.nli.org.il/IIIFv21/{id}/{region}/{size}/{rotation}/default.jpg"


def get_manifest(doc_id):
    r = requests.get(MANIFEST_URL.format(doc_id))
    r.raise_for_status()
    return r.json()


def get_pages_from_manifest(doc):
    seqs = doc['sequences']
    # assert len(seqs) == 1, len(seqs)
    for i, c in enumerate(seqs[0]['canvases']):
        assert c['@id'].startswith(IMG_API_URL)
        imgs = c['images']
        assert (len(imgs)) == 1
        yield {
            'ordinal': i + 1,
            'label': c['label'],
            'id': c['@id'][len(IMG_API_URL):],
            'height': c['height'],
            'width': c['width'],
        }


def get_img_url(img_id, region='full', size='max', rotation='0'):
    return IMG_URL.format(id=img_id, region=region, size=size,
                          rotation=rotation)


def get_thumb_url(img_id, height):
    return get_img_url(img_id, size=f",{height}")
