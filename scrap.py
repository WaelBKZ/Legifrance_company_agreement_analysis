import sys
import requests
import datetime
import time
import pandas as pd

from selenium import webdriver
from bs4 import BeautifulSoup
try:
    from simplejson.errors import JSONDecodeError
except ImportError:
    from json.decoder import JSONDecodeError


class ScrapAgreement:
    """A class for creating scrappers on Legifrance API.
    """

    def __init__(self, agree_subject='tele', agree_type='title', token_legifrance=None):
        """ScrapAgreement class constructor.

        Args:
            agree_subject (str): Must be 'tele' for scrapping Telecommuting agreements or 'equa' for Professional
            Equality agreements.
            agree_type (str): Must be 'title' for scrapping agreements according to their title or 'theme' for scrapping
            them according to their theme.
            token_legifrance: Token obtained on Legifrance API. More details on how to get it in the Readme file.

        Raises:
            ValueError: If the agree_subject or agree_type are not in str format such as described above. If the user
            has not entered a valid token_legifrance.
        """
        self.agree_subject = agree_subject
        self.agree_type = agree_type

        # Next, we choose the template of the url that will be used for scrapping, according to the subject and type of
        # agreement wished by the user.
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

        if token_legifrance is None:
            raise ValueError('Please go on Legifrance API and fetch a token there. Go on the Readme file for further '
                             'details on how to do it.')
        self.token_legifrance = token_legifrance

    def get_max_page_number(self):
        """Creates a max_page_number attribute, which corresponds to the number of pages for the search results on Legifrance.
        """
        first_page_url = self.url_scrap.format(page_number=1)
        wd = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
        wd.get(first_page_url)
        source = wd.page_source
        soup = BeautifulSoup(source)
        self.max_page_number = int(soup.select('#main_acco > div > div > div > nav > ul > li > a')[2][
                                       'data-num'])  # Total number of pages on legifrance for the given search results.

    @staticmethod
    def get_a_page(soup):
        """Gets a list of dictionaries of agreements IDs and links on a given Legifrance page.

        Args:
            soup (BeautifulSoup object): The soup object of a given page of agreements from Legifrance.

        Returns:
            list: A list of dictionaries each containing an unique ID and link for each agreement on a chosen page.
        """
        list_agreement_page = []
        for text in soup.findAll("h2"):
            agreement_id = text['data-id']
            link = 'https://www.legifrance.gouv.fr' + text.findChild("a")['href']
            agreement = {'link': link, 'id': agreement_id}
            list_agreement_page.append(agreement)

        return list_agreement_page

    def get_all_pages_ids(self, n=1_000_000):
        """Generalizes ScrapAgreement.get_a_page() method to all pages on Legifrance according to the scrapping criteria
        chosen by the user (subject and type).

        Creates a list_agreement attribute (for your ScrapAgreement object) which consists in a list of dictionaries of
        IDs and links for each agreement.

        They are fetched on chronological order.

        Args:
            n: Maximum number of pages that will be scrapped. Is set to 1 Million by default, i.e. it fetches every page
            by default.
        """
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
        """Gets the size and the size category of a French company using its Siret, and by scrapping the Sirene website.
        Used website : https://www.sirene.fr/sirene/public/accueil

        Args:
            siret (int_or_str): Siret of the company you wish to get the size.

        Returns:
            str: Range of people in the company (e.g. '150 à 999 personnes').
            str: Size category of the company, according to INSEE taxonomy ('PME', 'ETI' or 'GE'). For more, see :
            https://www.insee.fr/fr/metadonnees/definition/c1057
        """
        url_siret = f'https://www.sirene.fr/sirene/public/recherche?recherche.sirenSiret=54565020200025&amp;recherche.commune=&amp;recherche.captcha=&amp;__checkbox_recherche.excludeClosed=true&amp;recherche.adresse=&amp;recherche.raisonSociale=&amp;sirene_locale=fr'
        wd.get(url_siret)
        source = wd.page_source
        soup = BeautifulSoup(source)
        size = soup.select_one('#collapse-0 > div > div.result-right > p:nth-of-type(8) > label').next_sibling.strip()
        try:
            size_category = \
                soup.select_one(
                    '#collapse-0 > div > div.result-right > p:nth-of-type(10) > label').next_sibling.split()[0]
        except IndexError:
            size_category = None
            print(f"Couldn't fetch size_category for company with siret {siret}.")
        return size, size_category

    @staticmethod
    def date_raw_to_dmy(date_raw):
        """Converts a timestamp to a day-month-Year date.

        Args:
            date_raw (int): timestamp (e.g. 1624028410).

        Returns:
            str: date with d-m-Y format.
        """
        your_dt = datetime.datetime.fromtimestamp(int(date_raw) / 1000)  # using the local timezone
        return your_dt.strftime("%d-%m-%Y")

    def get_agreements_infos(self, user_feedback=True, start_at=0):
        """Gets a complete set of information for each agreement on the chosen scope of agreements.

        Information that are gathered for each agreement are : dateDepot, dateDiffusion, dateEffet, dateFin, dateMaj,
        dateTexte, company name, siret, size, size category, union, sector, nature, themes, NAF code and its content.

        It enriches the list_agreement attribute with additional information using the Legifrance API:
        https://developer.aife.economie.gouv.fr/.

        Should only be ran after ScrapAgreement.get_all_pages_ids.

        Args:
            user_feedback (:obj:`bool`, optional): Set to True if the user wishes to have feedback on the advancement
            of the scrapping. Defaults to True.
            start_at (:obj:`int`, optional): Number of the agreement you wish to start with for the scrapping. Useful
            when your session crashed and you don't want to start again from the beginning. Defaults to 0.

        Raises:
            JSONDecodeError: An error occurs while you are trying to access the Legifrance API. The json decoding
            is not actually the issue, it is rather that the API communication failed and that you most likely need
            to get a fresh token on the API. This error can only be raised if the user decides to exit the program (by
            entering 'Enter' when they are asked to).
        """
        n = len(self.list_agreement)
        if user_feedback == True:
            self.count_1 = 0
            count_2 = 0
        for i in range(start_at, n):
            self.position = i  # Useful for recovering the position at which you stopped, in case your session crashed or
            # raised an error.
            agree = self.list_agreement[i]
            agreement_id = agree['id']

            headers = {'Authorization': f'Bearer {self.token_legifrance}'}
            data = {"id": agreement_id}
            count_requests_fail = 0
            bool_break = 1 #When set to 1, the while loop below won't break unless we get a positive result or the user
            # decides to stop the algorithm.
            while bool_break :
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
                            '  Please refresh your Legifrance token. Enter the new token there : \n'
                            '(if you do not wish to refresh your token and wish to exit the scrapping, do not type '
                            'anything there and press Enter) \n')
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

            except KeyError:  # If an agreement cannot be fetched due to an "Le nombre de résultat retourné par le
                # moteur de recherche n'est pas égal à 1." error

                print(f"Agreement {agreement_id}'s information couldn't be fetched at all.")

            if user_feedback == True:
                self.count_1 += 1
                count_2 += 1
                if count_2 == 500:
                    print(f"We're at {self.count_1 / n * 100}%.")
                    count_2 = 0

    def auto_scrap(self, save_path=None, saving_format='xlsx', start_at = 0, skip_to_saving = False):
        """Compiles all the scrapping methods in one. Does all the scrapping at once.

        Args:
            save_path (str): Path you wish the .csv database be saved to. Please remove any '\' or '/' at the end. For
            example, it can be under the form of 'C:\User\documents\folder'.
            saving_format (:obj:`str`, optional): 'xlsx' or 'csv'. Defaults as 'xlsx'.
            start_at (:obj:`int`, optional): Number of the agreement you wish to start with for the scrapping. Useful
            when your session crashed and you don't want to start again from the beginning. Defaults to 0. If set as
            higher than 0, will automatically skip the get_all_pages_ids method as we assume you've already finished it.
            skip_to_saving (:obj:`bool`, optional): If, as a user, you only failed when entering the saving path and do
            not wish to relaunch the whole thing. If set as True, will directly skip to the saving part. Defaults to
            False.

        Raises:
            JSONDecodeError: An error occurs while you are trying to access the Legifrance API. The json decoding
            is not actually the issue, it is rather that the API communication failed and that you most likely need
            to get a fresh token on the API. This error can only be raised if the user decides to exit the program (by
            entering 'Enter' when they are asked to).
            FileNotFoundError: You entered a wrong save_path.
        """
        time1 = time.time()
        if skip_to_saving == False:
            if start_at != 0:
                self.get_all_pages_ids()
                print("All pages IDs fetched.")
            self.get_agreements_infos(start_at=start_at)
        self.df = pd.DataFrame(self.list_agreement)
        try:
            if saving_format == 'xlsx':
                self.df.to_excel(save_path + f'/legifrance_database_{self.agree_subject}_{self.agree_type}.{saving_format}')
            elif saving_format == 'csv':
                self.df.to_csv(save_path + f'/legifrance_database_{self.agree_subject}_{self.agree_type}.{saving_format}')
            else:
                raise ValueError("Please choose 'xlsx' or 'csv' as the saving_format for your scrapped database.")

        except FileNotFoundError:
            raise FileNotFoundError('Please enter a valid save_path for your file. You do not need to relaunch the '
                                    'whole process, please set skip_to_saving to True in the attributes to directly skip'
                                    ' to saving the dataframe.')

        print(f"100%.\nScrapping done. It took {time.time() - time1} seconds.")