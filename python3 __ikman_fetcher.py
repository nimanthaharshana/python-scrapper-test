import sys
import logging
import json
from fetcher import Fetcher

def fetch(q = 'bmw', p = 1):
    print("QUERY : ", q)
    print("PAGE # : ", p)
    fetch_url = '/en/ads?by_paying_member=0&sort=relevance&buy_now=0&query=' + q + '&page=' + p
    fetcher = Fetcher(fetch_url)
    ads = fetcher.fetchAds()
    index = 0
    ads_json = []
    for ad in ads:
        index = index + 1
        print("FETCHING INDEX : " + str(index))
        ad_element = fetcher.fetchAd(ad)
        ad_json = fetcher.getAdAsJSON(ad, ad_element)
        ads_json.append(ad_json)
    with open('ads.json', 'w') as json_file:
        json.dump(ads_json, json_file, indent=4)
    print("FINAL RESULT AS JSON : ")
    print(str(ads_json))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='fetcher.log', format='%(asctime)s %(levelname)s:%(message)s')
    print("Enter query:")
    q = input()
    print("Enter page number:")
    p = input()
    fetch(q, p)