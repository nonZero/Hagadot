# from django.test import TestCase
import json
import unittest
from pathlib import Path

from books.nli_api import get_pages_from_manifest

MANIFEST_FILE = Path(__file__).parent / '../data/manifest.json'


class MyTestCase(unittest.TestCase):
    def test_canvases(self):
        with MANIFEST_FILE.open() as f:
            doc = json.load(f)
        data = list(get_pages_from_manifest(doc))
        assert False, data
