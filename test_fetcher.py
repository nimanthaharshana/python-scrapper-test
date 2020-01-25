import unittest
from fetcher import Fetcher


class TestFetcher(unittest.TestCase):

    def setUp(self):
        q = 'bmw'
        p = '1'
        self.fetch_url = '/en/ads?by_paying_member=0&sort=relevance&buy_now=0&query=' + q + '&page=' + p
        self.fetcher = Fetcher(self.fetch_url)

    def test_fetch_ads(self):
        ads = self.fetcher.fetchAds()
        self.assertIsNotNone(ads)

    def test_fetch_ad(self):
        ads = self.fetcher.fetchAds()
        ad_element = None
        if(ads):
            ad = ads[0]
            ad_element = self.fetcher.fetchAd(ad)
            self.assertIsNotNone(ad_element)
        else:
            self.assertIsNone(ad_element)


