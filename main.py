import os

from dotenv import load_dotenv
from pymongo import MongoClient

from site_bot import AmazonBot

# Chargement des variables d'environnement se trouvant dans le fichier .env
load_dotenv()

# Connexion à la base de donnée MongoDB
try:
    client = MongoClient(
        "mongodb+srv://" + os.getenv("MONGODB_USERNAME") +
        ":" + os.getenv("MONGODB_PASSWORD") + "@" + os.getenv("MONGODB_DOMAIN") +
        "/" + os.getenv("MONGODB_DBNAME") + "?retryWrites=true&w=majority"
    )
    client.server_info()
except Exception as e:
    raise e from e

prototype_urls = [
    "https://www.amazon.fr/HP-Cartouches-Couleurs-Authentiques-Officejet/dp/B019EIFWLK/ref=zg-bs_computers_1/257"
    "-6313485-9093037?pd_rd_w=oFs7Z&pf_rd_p=f492caf8-8007-48d2-883a-38800a772222&pf_rd_r=K7S2T2XYHGSYF9PZZR3Q&pd_rd_r=6b3a3481-0a0d-407f-b873-8f3c7fbfbf73&pd_rd_wg=aqXNP&pd_rd_i=B019EIFWLK&th=1",
    "https://www.amazon.fr/HP-cartouches-couleurs-authentiques-N9J72AE/dp/B01AGGJ44K/ref=zg-bs_computers_2/257"
    "-6313485-9093037?pd_rd_w=oFs7Z&pf_rd_p=f492caf8-8007-48d2-883a-38800a772222&pf_rd_r=K7S2T2XYHGSYF9PZZR3Q&pd_rd_r=6b3a3481-0a0d-407f-b873-8f3c7fbfbf73&pd_rd_wg=aqXNP&pd_rd_i=B01AGGJ44K&th=1",
    "https://www.amazon.fr/Crucial-CT480BX500SSD1-Interne-BX500-Pouces/dp/B07G3KGYZQ/ref=zg-bs_computers_9/257"
    "-6313485-9093037?pd_rd_w=oFs7Z&pf_rd_p=f492caf8-8007-48d2-883a-38800a772222&pf_rd_r=K7S2T2XYHGSYF9PZZR3Q&pd_rd_r=6b3a3481-0a0d-407f-b873-8f3c7fbfbf73&pd_rd_wg=aqXNP&pd_rd_i=B07G3KGYZQ&th=1",
    "https://www.amazon.fr/TP-Link-Archer-T3U-adaptateur-compatible/dp/B07M69276N/ref=zg-bs_computers_10/257-6313485"
    "-9093037?pd_rd_w=oFs7Z&pf_rd_p=f492caf8-8007-48d2-883a-38800a772222&pf_rd_r=K7S2T2XYHGSYF9PZZR3Q&pd_rd_r=6b3a3481-0a0d-407f-b873-8f3c7fbfbf73&pd_rd_wg=aqXNP&pd_rd_i=B07M69276N&th=1",
    "https://www.amazon.fr/SanDisk-Ultra-allant-jusqu%C3%A0-150-Mo/dp/B015CH1NAQ/ref=zg-bs_computers_12/257-6313485"
    "-9093037?pd_rd_w=oFs7Z&pf_rd_p=f492caf8-8007-48d2-883a-38800a772222&pf_rd_r=K7S2T2XYHGSYF9PZZR3Q&pd_rd_r=6b3a3481-0a0d-407f-b873-8f3c7fbfbf73&pd_rd_wg=aqXNP&pd_rd_i=B015CH1NAQ&th=1",
    "https://www.amazon.fr/TP-Link-Compatibilit%C3%A9-Universelle-Installation-TL-WA850RE/dp/B00A0VCJPI/ref=zg"
    "-bs_computers_16/257-6313485-9093037?pd_rd_w=oFs7Z&pf_rd_p=f492caf8-8007-48d2-883a-38800a772222&pf_rd_r=K7S2T2XYHGSYF9PZZR3Q&pd_rd_r=6b3a3481-0a0d-407f-b873-8f3c7fbfbf73&pd_rd_wg=aqXNP&pd_rd_i=B00A0VCJPI&th=1",
    "https://www.amazon.fr/Crucial-CT1000P2SSD8-Interne-Vitesses-atteignant/dp/B089DNM8LR/ref=zg-bs_computers_17/257"
    "-6313485-9093037?pd_rd_w=oFs7Z&pf_rd_p=f492caf8-8007-48d2-883a-38800a772222&pf_rd_r=K7S2T2XYHGSYF9PZZR3Q&pd_rd_r=6b3a3481-0a0d-407f-b873-8f3c7fbfbf73&pd_rd_wg=aqXNP&pd_rd_i=B089DNM8LR&th=1",
    "https://www.amazon.fr/TP-Link-TL-SG105-Switch-Gigabit-Bo%C3%AEtier/dp/B00A128S24/ref=zg-bs_computers_18/257"
    "-6313485-9093037?pd_rd_w=oFs7Z&pf_rd_p=f492caf8-8007-48d2-883a-38800a772222&pf_rd_r=K7S2T2XYHGSYF9PZZR3Q&pd_rd_r=6b3a3481-0a0d-407f-b873-8f3c7fbfbf73&pd_rd_wg=aqXNP&pd_rd_i=B00A128S24&th=1",
]

# Initialisation de la classe AmazonBot
bot = AmazonBot(mongodb_client=client)

# Lancement du Scraping
bot.scrapePrototypeData(prototype_urls)
# bot.scrapeCategoryUrls()
# bot.scrapeProductData()
