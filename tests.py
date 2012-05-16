import os
import unittest
import uuid

from geogotchi import Geogotchi
from geogotchi import errors
from geogotchi.constants import DEFAULT_USERNAME

latlons = {
        "sthlm": (59.333, 18.065),
        "gbg": (57.707, 11.967),
        "malmo": (55.606, 13.001),
        "uppsala": (59.859, 17.645),
        "lkpg": (58.411, 15.622),
        }
username = os.environ.get("GEOGOTCHI_USERNAME", DEFAULT_USERNAME)
gg = Geogotchi(username=username)

def get_random_string():
    return uuid.uuid4().hex


class TestGeogotchi(unittest.TestCase):

    def test_invalid_username(self):
        sthlm = latlons["sthlm"]
        gg_invalid = Geogotchi(username=get_random_string())
        self.assertRaises(errors.AuthorizationException,
                          gg_invalid.find_nearby_toponym, sthlm)

    def test_find_nearby_place(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_place(sthlm)
        names = [n["name"] for n in nearby]
        self.assertTrue("Stockholm" in names)

    def test_find_nearby_toponym(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_toponym(sthlm)
        names = [n["name"] for n in nearby]
        self.assertTrue("Stockholm" in names)

    def test_find_nearby_wikipedia_default(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_wikipedia(sthlm)

    def test_find_nearby_wikipedia_sort_distance(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_wikipedia(sthlm, rank_weight=0)
        min_dist = min(n["distance"] for n in nearby)
        self.assertEqual(nearby[0]["distance"], min_dist)
        max_dist = max(n["distance"] for n in nearby)
        self.assertEqual(nearby[-1]["distance"], max_dist)

    def test_find_nearby_wikipedia_sort_rank(self):
        sthlm = latlons["sthlm"]
        nearby = gg.find_nearby_wikipedia(sthlm, distance_weight=0)
        max_rank = max(n["rank"] for n in nearby)
        self.assertEqual(nearby[0]["rank"], max_rank)
        min_rank = min(n["rank"] for n in nearby)
        self.assertEqual(nearby[-1]["rank"], min_rank)

    def test_find_nearby_toponym_with_radius_and_max_rows(self):
        sthlm = latlons["sthlm"]
        max_rows = 3
        nearby = gg.find_nearby_toponym(sthlm, radius=5, max_rows=max_rows)
        self.assertEqual(max_rows, len(nearby))