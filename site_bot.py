import datetime
import time

from bs4 import BeautifulSoup
from selenium import webdriver


class AmazonBot:

    def __init__(self, mongodb_client):
        self.mongodb_client = mongodb_client
        self.amazon_header = {
            'authority': 'www.amazon.fr',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-gpc': '1',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        # Ajouter ici le chemin vers chromedriver self.driver = webdriver.Chrome(
        # executable_path=r"C:\Users\cedri\Documents\chromedriver_win32\chromedriver.exe") ou bien autre astuce
        # faites un pip install webdriver-manager et a la place du chemin mettez ChromeDriverManager().install() si
        # vous préférez la seconde solution enlever les commentaires des deux prochaines lignes et commentez la ligne
        # 29
        options = webdriver.ChromeOptions()
        # to supress the error messages/logs
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        from webdriver_manager.chrome import ChromeDriverManager
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())

    def getProductUrls(self, category_url: str):
        """
        Permet d'obtenir les urls des produits d'une catégorie
        :param category_url :
        :type category_url :
        :return prduct_urls :
        :rtype list :
        """
        self.driver.get(category_url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        prduct_urls = None
        try:
            products_links = soup.find_all('a', {'class': 'a-link-normal s-no-outline'}, limit=15)
            prduct_urls = [
                f"https://www.amazon.fr{product_link['href']}"
                for product_link in products_links
            ]
        except:
            try:
                products_links = soup.find_all('a', {'class': 'style__overlay__2qYgu ProductGridItem__overlay__1ncmn'}, limit=15)
                prduct_urls = [
                    f"https://www.amazon.fr{product_link['href']}"
                    for product_link in products_links
                ]
            except:
                pass

        finally:
            return prduct_urls

    def getProductTitle(self, soup):
        try:
            return soup.find('span', {'id': 'productTitle'}).get_text().strip()
        except:
            return None

    def getProductRating(self, soup):
        try:
            div_avg_cust_reviews = soup.find('div', {'id': 'averageCustomerReviews'})
            rating = div_avg_cust_reviews.find('span', {'class': 'a-icon-alt'}).get_text().strip().split()[0]
            return float(rating.replace(',', '.'))
        except:
            return None

    def getProductNbReviewers(self, soup):
        try:
            nb_reviewers = soup.find('span', {'id': 'acrCustomerReviewText'}).get_text().strip()
            return int(''.join(nb_reviewers.split()[:-1]))
        except:
            return None

    def getProductPrice(self, soup):
        try:
            price = soup.find('span', {
                'class': 'a-price aok-align-center priceToPay',
                'data-a-color': 'base'}) \
                .find('span', {'class': 'a-offscreen'}) \
                .get_text().strip()
            return float(price.strip().replace(',', '.')[:-1])
        except:
            try:
                price = soup.find('span', {
                    'style': 'font-size:14px;color:#555;line-height:1'}) \
                    .find('span', {'class': 'a-offscreen'}) \
                    .get_text().strip()
                return float(price.strip().replace(',', '.')[:-1])
            except:
                return None

    def getProductLinkReviewers(self, soup):
        try:
            reviewers_link = soup.find('a', {'data-hook': 'see-all-reviews-link-foot'})
            return f"https://www.amazon.fr{reviewers_link['href']}"
        except:
            return None

    def getProductReviewersDate(self, soup):
        try:
            dates = soup.find_all('span', {'data-hook': 'review-date'})
            return [date.get_text().strip() for date in dates]
        except:
            return None

    def getProductReviewersBody(self, soup):
        try:
            contents = soup.find_all('span', {'data-hook': 'review-body'})
            return [content.find('span').get_text().strip() for content in contents]
        except:
            return None

    def getImageUrl(self, soup):
        try:
            image_url = soup.find('img', {'data-a-image-name': "landingImage"})
            return image_url['src']
        except:
            return None

    def getProductReviewers(self, review_url):
        url = review_url
        reviews_list = []
        while True:
            try:
                # Aller à la page de commentaire suivante si elle existe
                self.driver.get(url)
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            except:
                return None
            else:
                review_dates = self.getProductReviewersDate(soup)
                region = [review_date.split()[2] for review_date in review_dates]
                date = [' '.join(date.split()[4:]) for date in review_dates]
                body = self.getProductReviewersBody(soup)

                review = {
                    "date": date,
                    "region": region,
                    "body": body
                }
                reviews_list.append(review)

                try:
                    if (
                        # Récupérer le lien de la page des commentaires suivant
                        next_page_comment := soup.find(
                            'div', {'id': 'cm_cr-pagination_bar'}
                        )
                        .find('li', {'class': 'a-last'})
                        .find('a')
                    ):
                        url = f"https://www.amazon.fr{next_page_comment['href']}"
                    else:
                        return reviews_list
                except:
                    return reviews_list



    def getProductData(self, product_url):
        self.driver.get(product_url)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        title = self.getProductTitle(soup)
        rating = self.getProductRating(soup)
        nb_reviewers = self.getProductNbReviewers(soup)
        price = self.getProductPrice(soup)
        reviewers_url = self.getProductLinkReviewers(soup)
        product_reviews = self.getProductReviewers(reviewers_url)
        image_url = self.getImageUrl(soup)

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "nb_reviewers": nb_reviewers,
            "url": product_url,
            "image_url": image_url,
            "remark": product_reviews
        }

    def scrapeCategoryUrls(self):
        """
        Cette fonction nous permet de scraper les urls des produits present dans la catégorie et de les sauvegardés
        dans MongoDB
        """

        category_urls = self.mongodb_client["commind"]["category_urls"].find({})
        for category_url in category_urls:
            print("Url à scraper (cat):", category_url["url"], "\n")

            product_urls = self.getProductUrls(category_url["url"])

            # Upsert
            for product_url in product_urls:
                print("product", product_url)
                self.mongodb_client["commind"]["product_urls"].update({"url": product_url},
                                                                     {"$set": {"url": product_url}},
                                                                     upsert=True)

            # Update
            self.mongodb_client["commind"]["category_urls"].update({"url": category_url["url"]}, {"$set": {
                'scrape': False
            }})
            time.sleep(2)

    def scrapeProductData(self):
        """
        Cette fonction nous permet de récupérer les informations liées au produit et les stoke dans une base de donnée
        MongoDB
        """

        # Query MongoDB pour récupérer les liens à scraper
        product_urls = self.mongodb_client["commind"]["product_urls"].find({})

        for product_url in product_urls:
            print("Url à scraper:", product_url["url"], "\n")
            data = self.getProductData(product_url["url"])

            # Upsert
            self.mongodb_client["commind"]["product_data"].update({"url": product_url['url']}, {"$set": data},
                                                                 upsert=True)

            # if reviews is not None:
            #     # Upsert
            #     self.mongodb_client["commind"]["product_reviews"].update({"product_url": reviews['product_url']},
            #                                                             {"$set": reviews},
            #                                                             upsert=True)

        # pause de 2 secondes
        time.sleep(2)

    def scrapePrototypeData(self, prototype_urls):
        """
        Cette fonction nous permet de récupérer les informations liées au produit et les stoke dans une base de donnée
        MongoDB
        """

        # Query MongoDB pour récupérer les liens à scraper
        print(type(prototype_urls))

        for product_url in prototype_urls:
            print("Url à scraper:", product_url, "\n")
            data = self.getProductData(product_url)

            # Upsert
            self.mongodb_client["commind"]["prototype_data"].update({"url": product_url}, {"$set": data},
                                                                 upsert=True)
        # pause de 2 secondes
        time.sleep(2)


if __name__ == '__main__':
    pass
    # product_title = "Iphone"
    # review_url = "https://www.amazon.fr/Apple-iPhone-13-Pro-Max/product-reviews/B09G94C81G/ref=cm_cr_getr_d_paging_btm_next_5?ie=UTF8&reviewerType=all_reviews&pageNumber=5"
    # product_url = "https://www.amazon.fr/Apple-iPhone-13-Pro-Max/dp/B09G94C81G/ref=cm_cr_arp_d_product_top?ie=UTF8"
    # test = AmazonBot('rien')
    # test.getProductData(product_url)
    # test.getProductReviewers(review_url, product_title, product_url)
