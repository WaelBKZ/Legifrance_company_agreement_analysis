#initialization cell

!pip install selenium
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

import sys
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import datetime
import time
import pandas as pd
from google.colab import drive
try:
    from simplejson.errors import JSONDecodeError
except ImportError:
    from json.decoder import JSONDecodeError


sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

#drive.mount('/content/drive')

class ScrapAgreement:
    # scrap_agreement objects will serve as tools to scrap french company agreements on Legifrance, weither they be
    # Telecommuting agreements or F/M Equality agreements.

    def __init__(self, agree_subject='tele', agree_type='title', token_legifrance=None, token_sirene=None):
        # agree_subject must be 'tele' or 'equa', agree_type must be 'title' or 'theme'
        # token_legifrance must be recovered on Legifrance API
        # token_sirene must be recovered on Sirene API

        self.agree_subject = agree_subject
        self.agree_type = agree_type

        if agree_subject == 'tele':
            if agree_type == 'title':
                self.url_scrap = 'https://www.legifrance.gouv.fr/search/acco?tab_selection=acco&searchField=TITLE' \
                                 '&query=t%C3%A9l%C3%A9travail&searchType=ALL&typePagination=DEFAULT&sortValue' \
                                 '=DATE_ASC&pageSize=100&page={page_number}&tab_selection=acco#acco '
            elif agree_type == 'theme':
                self.url_scrap = 'https://www.legifrance.gouv.fr/search/acco?tab_selection=acco&searchField=ALL' \
                                 '&searchType=ALL&theme=yDGL3w%3D%3D&typePagination=DEFAULT&sortValue=DATE_ASC' \
                                 '&pageSize=100&page={page_number}&tab_selection=acco#acco '
            else:
                raise ValueError('agree_type must be set as "tele" or "title".')
        elif agree_subject == 'equa':
            if agree_type == 'title':
                self.url_scrap = 'https://www.legifrance.gouv.fr/search/acco?tab_selection=acco&searchField=TITLE' \
                                 '&query=%C3%A9galit%C3%A9+professionnelle&searchType=ALL&typePagination=DEFAULT' \
                                 '&sortValue=DATE_ASC&pageSize=100&page={page_number}&tab_selection=acco#acco '
            elif agree_type == 'theme':
                self.url_scrap = 'https://www.legifrance.gouv.fr/search/acco?tab_selection=acco&searchField=ALL' \
                                 '&searchType=ALL&theme=iOR56g%3D%3D&typePagination=DEFAULT&sortValue=DATE_ASC' \
                                 '&pageSize=100&page={page_number}&tab_selection=acco#acco '
            else:
                raise ValueError('agree_type must be set as "tele" or "title".')
        else:
            raise ValueError('agree_subject must be set as "tele" or "equa".')

        # if token_legifrance is None or token_sirene is None:
        #     raise ValueError('Please go on Legifrance API and Sirene API and fetch a token for each of them.')

        self.token_legifrance = token_legifrance

        # self.token_sirene = token_sirene
        # self.number_fails_sirene_api = 0
        # self.count_api_siren = 0

    def get_max_page_number(self):
        first_page_url = self.url_scrap.format(page_number=1)
        wd = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        wd.get(first_page_url)
        source = wd.page_source
        soup = BeautifulSoup(source)
        self.max_page_number = int(soup.select('#main_acco > div > div > div > nav > ul > li > a')[2][
                                       'data-num'])  # Total number of pages on legifrance for the given search results.

    @staticmethod
    def get_a_page(soup):
        # get a list of dictionaries with agreements ids and links on a given legifrance page.
        list_agreement_page = []

        for text in soup.findAll("h2"):
            agreement_id = text['data-id']
            link = 'https://www.legifrance.gouv.fr' + text.findChild("a")['href']
            agreement = {'link': link, 'id': agreement_id}
            list_agreement_page.append(agreement)
        return list_agreement_page

    def get_all_pages_ids(self, n=1_000_000):
        # n corresponds to the maximum number of pages there.
        # get all agreements on legifrance by title research on the "Télétravail" (telecommuting) topic.
        if n == 1_000_000:
            # In case the user did not specify a number of page he is willing to scrap, we will automatically fetch
            # the maximum number of pages.
            self.get_max_page_number()
            n = self.max_page_number
        list_agreement = []
        for i in range(1, n + 1):
            url = self.url_scrap.format(page_number=i)
            wd.get(url)
            source = wd.page_source
            soup = BeautifulSoup(source)
            try:
                list_agreement_page_i = self.get_a_page(soup)
                list_agreement.extend(list_agreement_page_i)
            except:
                print(i)
                print(f"Error getting agreement {i} id.")
        self.list_agreement = list_agreement

    @staticmethod
    def get_company_size(siret):
        url_siret = f'https://www.sirene.fr/sirene/public/recherche?recherche.sirenSiret={siret}&recherche.commune=&recherche.captcha=&__checkbox_recherche.excludeClosed=true&recherche.adresse=&recherche.raisonSociale=&recherche.excludeClosed=true&sirene_locale=fr'
        wd.get(url_siret)
        source = wd.page_source
        soup = BeautifulSoup(source)
        size = soup.select_one('#collapse-0 > div > div.result-right > p:nth-of-type(8) > label').next_sibling.strip()
        try:
            size_category = \
            soup.select_one('#collapse-0 > div > div.result-right > p:nth-of-type(10) > label').next_sibling.split()[0]
        except IndexError:
            size_category = None
            print(f"Couldn't fetch size_category for company with siret {siret}.")
        return size, size_category

    # def get_company_size(self, siret):
    #     # Get the company size with Siret, only after you've scrapped all Sirets. API link :
    #     # https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3
    #     # &provider=insee#!/Etablissement/findBySiret

    #     url_siret = f"https://api.insee.fr/entreprises/sirene/V3/siret/{siret}"
    #     headers = {'Authorization': f'Bearer {self.token_sirene}'}
    #     response = requests.get(url_siret, headers=headers)
    #     count = 0
    #     if self.count_api_siren < 8 :
    #       self.count_api_siren += 1
    #     else :
    #       time.sleep(1)
    #       self.count_api_siren = 0
    #     while True :
    #       try :
    #         response_json = response.json()
    #         size = response_json['etablissement']['uniteLegale']['categorieEntreprise']  # size of the company
    #         return size
    #       except JSONDecodeError :
    #         if count < 4 :
    #           print(f'Had to sleep {count+1}s.')
    #           time.sleep(count+1)
    #           count += 1
    #         else :
    #           print("Size scrapping via Sirene API failed for agreement with siret:", siret)
    #           print("response value:", response)
    #           n = self.max_page_number
    #           self.number_fails_sirene_api += 1
    #           size = None
    #           return size

    @staticmethod
    def date_raw_to_dmy(date_raw):
        your_dt = datetime.datetime.fromtimestamp(int(date_raw) / 1000)  # using the local timezone
        return your_dt.strftime("%d-%m-%Y")

    def get_agreements_infos(self, user_feedback=True):
        # user_feedback : indicates if user wants feeback or not.
        # Run this after running get_all_pages_ids.
        n = len(self.list_agreement)
        if user_feedback == True:
            count_1 = 0
            count_2 = 0
        for i in range(n):
            agree = self.list_agreement[i]
            agreement_id = agree['id']

            headers = {'Authorization': f'Bearer {self.token_legifrance}'}
            data = {"id": agreement_id}
            count_requests_fail = 0
            bool_break = 1
            while bool_break:
                response = requests.post(
                    'https://sandbox-api.piste.gouv.fr/dila/legifrance-beta/lf-engine-app/consult/acco',
                    headers=headers,
                    json=data)
                try:
                    response_json = response.json()
                    bool_break = 0
                except JSONDecodeError:
                    if count_requests_fail < 11:
                        count_requests_fail += 1
                    else:
                        user_request = input(
                            '  Please refresh your Legifrance token. Enter the new token there : \n(if you do not wish to refresh your token and wish to exit the scrapping, do not type anything there and press Enter) \n')
                        if user_request != '':
                            self.token_legifrance = user_request
                            headers = {'Authorization': f'Bearer {self.token_legifrance}'}
                        else:
                            print("Scrapping via Legifrance API failed for agreement with id:", agreement_id)
                            print("response value:", response)
                            raise JSONDecodeError
            try:
                dateDepot_raw = response_json['acco']['dateDepot']  # deposit date on legifrance
                dateDepot = self.date_raw_to_dmy(dateDepot_raw)
                self.list_agreement[i]['dateDepot'] = dateDepot

                dateDiffusion_raw = response_json['acco']['dateDiffusion']  # date it was published on legifrance
                dateDiffusion = self.date_raw_to_dmy(dateDiffusion_raw)
                self.list_agreement[i]['dateDiffusion'] = dateDiffusion

                dateEffet_raw = response_json['acco']['dateEffet']  # date from which the agreement takes effect
                dateEffet = self.date_raw_to_dmy(dateEffet_raw)
                self.list_agreement[i]['dateEffet'] = dateEffet

                dateFin_raw = response_json['acco']['dateFin']  # date until which the agreement has effect
                dateFin = self.date_raw_to_dmy(dateFin_raw)
                self.list_agreement[i]['dateFin'] = dateFin

                dateMaj_raw = response_json['acco'][
                    'dateMaj']  # unsure what this date corresponds to. will let it as is in the dataframe
                dateMaj = self.date_raw_to_dmy(dateMaj_raw)
                self.list_agreement[i]['dateMaj'] = dateMaj

                dateTexte_raw = response_json['acco']['dateTexte']  # date the agreement was signed
                dateTexte = self.date_raw_to_dmy(dateTexte_raw)
                self.list_agreement[i]['dateTexte'] = dateTexte

                entreprise = response_json['acco']['raisonSociale']
                self.list_agreement[i]['entreprise'] = entreprise

                siret = response_json['acco']['siret']
                self.list_agreement[i]['siret'] = siret

                size, size_category = self.get_company_size(siret)
                self.list_agreement[i]['size'] = size
                self.list_agreement[i]['size_category'] = size_category

                syndicats = []
                for syndic in response_json['acco']['syndicats']:
                    syndicats.append(syndic['libelle'])
                self.list_agreement[i]['syndicats'] = syndicats

                secteur = response_json['acco']['secteur']
                self.list_agreement[i]['secteur'] = secteur

                nature = response_json['acco']['nature']
                self.list_agreement[i]['nature'] = nature

                themes = []
                for theme in response_json['acco']['themes']:
                    themes.append(theme['libelle'])
                self.list_agreement[i]['themes'] = themes

                codeNAF = response_json['acco']['codeApe']
                self.list_agreement[i]['codeNAF'] = codeNAF

                contenu = response_json['acco']['attachment']['content']
                self.list_agreement[i]['contenu'] = contenu

            except KeyError:  # Si un accord ne peut pas être récupéré à cause d'une erreur "Le nombre de résultat retourné par le moteur de recherche n'est pas égal à 1."
                dateDepot = None
                self.list_agreement[i]['dateDepot'] = dateDepot

                dateDiffusion = None
                self.list_agreement[i]['dateDiffusion'] = dateDiffusion

                dateEffet = None
                self.list_agreement[i]['dateEffet'] = dateEffet

                dateFin = None
                self.list_agreement[i]['dateFin'] = dateFin

                dateMaj = None
                self.list_agreement[i]['dateMaj'] = dateMaj

                dateTexte = None
                self.list_agreement[i]['dateTexte'] = dateTexte

                entreprise = None
                self.list_agreement[i]['entreprise'] = entreprise

                siret = None
                self.list_agreement[i]['siret'] = siret

                size, size_category = (None, None)
                self.list_agreement[i]['size'] = size
                self.list_agreement[i]['size_category'] = size_category

                syndicats = None
                self.list_agreement[i]['syndicats'] = syndicats

                secteur = None
                self.list_agreement[i]['secteur'] = secteur

                nature = None
                self.list_agreement[i]['nature'] = nature

                themes = None
                self.list_agreement[i]['themes'] = themes

                codeNAF = None
                self.list_agreement[i]['codeNAF'] = codeNAF

                contenu = None
                self.list_agreement[i]['contenu'] = contenu

            if user_feedback == True:
                count_1 += 1
                count_2 += 1
                if count_2 == 500:
                    print(f"We're at {count_1 / n * 100}%.")
                    count_2 = 0

    def auto_scrap(self, save_path=None):
        # Does all the scrapping
        time1 = time.time()
        self.get_all_pages_ids()
        print("All pages IDs fetched.")
        self.get_agreements_infos()
        self.df = pd.DataFrame(self.list_agreement)
        self.df.to_csv(save_path + f'/database_{self.agree_subject}_{self.agree_type}.csv')
        print(f"Scrapping done. It took {time.time() - time1} seconds.")