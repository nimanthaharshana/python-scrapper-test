import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class Fetcher:

    def __init__(self, fetch_url):
        self.base = "https://ikman.lk"
        self.fetch_url = fetch_url
        logger.info("FETCHING INITIATED FOR THE URL : " + self.base + self.fetch_url)
        print("FETCHING INITIATED FOR THE URL : " + self.base + self.fetch_url)

    def fetchAds(self):
        url = self.base + self.fetch_url
        try:
            # proxies = {
            #     "http": "http://10.10.10.10:8000",
            #     "https": "http://10.10.10.10:8000",
            # }
            request = requests.get(url)
            # request = requests.get(url, proxies=proxies)
            soup = BeautifulSoup(request.content, 'html.parser')
            if (request.status_code == 200):
                ads = soup.find(class_='ad-list--2Y3ql').find_all('a', attrs={'class': 'card-link--3ssYv',
                                                                              'title': self.excludeNonAdElements})
                logger.info("NUMBER OF ADS FETCHED : " + str(len(ads)))
                print("NUMBER OF ADS FETCHED : " + str(len(ads)))
                return ads
            else:
                logger.warn("REQUEST FAILED FOR THE URL : '{url}'")
                print("REQUEST FAILED FOR THE URL : '{url}'")
        except requests.exceptions.ConnectionError:
            logger.warn("REQUEST REFUSED BY THE HOST : " + self.base)
            print("REQUEST REFUSED BY THE HOST : " + self.base)

    def fetchAd(self, ad):
        url = ad['href']
        ad_url = self.base + url
        logger.info("FETCHING AD DETAILS FROM THE URL : " + ad_url)
        print("FETCHING AD DETAILS FROM THE URL : " + ad_url)
        request = requests.get(ad_url)

        if request.status_code == 200:
            soup = BeautifulSoup(request.content, 'html.parser')
            ad_element = soup.find(class_='item-detail')
            title = ad_element.find('div', attrs={"class": "ui-panel-content ui-panel-block"}).h1.text
            try:
                date = ad_element.find("span", attrs={"class": "date"}).text
            except Exception:
                logger.warn("DATE IS NOT AVAILABLE FOR THE AD TITLED : " + str(title))
                date = ''

            try:
                description = ad_element.find("div", attrs={"class": "item-description"}).p.text
            except Exception:
                logger.warn("DESCRIPTION IS NOT AVAILABLE FOR THE AD TITLED : " + str(title))
                description = ''

            try:
                image_urls = []
                imgs = (ad_element.find('div', attrs={"class": "gallery-nav"})).find_all('a')
                for img in imgs:
                    img_url = img.img['src'][2:]
                    image_urls.append(img_url)
            except Exception:
                logger.warn("IMAGES NOT AVAILABLE FOR THE AD TITLED : " + str(title))
                image_urls = []

            try:
                contact = ad_element.find("span", attrs={"class": "h3"}).text
            except Exception:
                logger.warn("CONTACT INFO IS NOT AVAILABLE FOR THE AD TITLED : " + str(title))
                contact = ''

            try:
                category = (ad_element.find('nav', attrs={"class": "ui-crumbs"})).find_all('li')[5].a.span.text
            except Exception:
                logger.warn("CATEGORY IS NOT AVAILABLE FOR THE AD TITLED : " + str(title))
                category = ''

            return {
                'date': date,
                'description': description,
                'image_urls': image_urls,
                'contact': contact,
                'category': category
            }
        else:
            logger.warn("FETCHING AD DETAILS FAILED FOR THE URL : " + ad_url)


    def getAdAsJSON(self, ad, ad_element):
        title = ad.find('span', attrs={"class": "title--3yncE"}).text
        short_description = ad.find('div', attrs={"class": "description--2-ez3"}).text
        # print(ad)
        url = self.base + ad['href']
        price = ad.find('div', attrs={"class": "price--3SnqI color--t0tGX"}).span.text
        # ad_element = self.fetchAd(url)
        ad_json =  {
            'title': title,
            'date': ad_element['date'],
            'short_description': short_description,
            'category': ad_element['category'],
            'url': url,
            'details': {
                'full_description': ad_element['description'],
                'image_urls': ad_element['image_urls'],
                'price': price,
                'contact': ad_element['contact']
            }
        }
        logger.info("AD DETAILS : " + str(ad_json))
        print("AD DETAILS : " + str(ad_json))
        return ad_json

    def excludeNonAdElements(self, title):
        return title != 'Top ad' and title != 'Bump up'

