from clasesAuxiliares.httpFetcher import HttpFetcher
from clasesAuxiliares.csvExporter import CsvExporter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

def extract_product_data(product_search: str, web_driver: webdriver.Chrome, http_fetcher: HttpFetcher, url: str = None):
    if url: 
        product_list_url = url
    else: #caso inicial
        product_list_url = get_product_search_url(product_search)

    random_delay(1, 2)

    page = http_fetcher.GET(product_list_url)
    html_tree = BeautifulSoup(page.content, "html.parser")
    html_tree_prettified = BeautifulSoup(html_tree.prettify(), "html.parser")

    #extraigo la data de los productos y la guardo
    data.append(extract_product_list_data(html_tree_prettified))

    random_delay(3, 2)

    #le asigno una url al webdriver
    web_driver.get(product_list_url)


    #obtengo y clickeo el boton que lleva a la siguiente pagina
    next_page_button = get_next_page_button(web_driver)
    click_tag(web_driver, next_page_button, 2)

    #clausula de escape
    if next_page_button:
        new_url = web_driver.current_url
        extract_product_data(product_search, web_driver, http_fetcher, new_url)
    else:
        web_driver.quit()
        print("Extraction finished.")


def extract_product_list_data(html_tree: BeautifulSoup):
    product_containers = html_tree.find_all("div", class_="ui-search-result__wrapper")
    products_data = []

    for product_container in product_containers:
        anchor = product_container.find("a", class_="ui-search-item__group__element ui-search-link__title-card ui-search-link")
        title_raw_text = anchor['title']
        title = title_raw_text.strip()
        
        try:
            score_container = product_container.find("div", class_="ui-search-reviews ui-search-item__group__element")
            score_raw_text = score_container.find("span").text
            score = score_raw_text.strip()
        except AttributeError:
            score = "?"
            print("error encontrando el score de: ", title[:25])

        try:
            price_container = product_container.find("div", class_="ui-search-item__group ui-search-item__group--price ui-search-item__group--price-grid-container")
            price_raw_text = price_container.find("span", class_="andes-money-amount__fraction").text
            price = price_raw_text.strip()
        except AttributeError:
            price = "?"
            print("error encontrando el precio de: ", title[:20])
        products_data.append([title, score, price])

    fully_fetched_products = [product for product in products_data if "?" not in product]
    no_score_products = [product for product in products_data if "?" in product[1]]
    no_price_products = [product for product in products_data if "?" in product[2]]
    print("product count:", len(product_containers))
    print("full data product count:", len(fully_fetched_products))
    print("no score product count", len(no_score_products))
    print("no price product count:", len(no_price_products))
    return products_data


def get_next_page_button(webdriver):
    next_page_button = webdriver.find_element(By.CSS_SELECTOR, "div > div.ui-search-main.ui-search-main--only-products.ui-search-main--with-topkeywords > section > nav > ul > li.andes-pagination__button.andes-pagination__button--next > a")
    next_page_li = next_page_button.find_element(By.XPATH, '..')
    li_classes = next_page_li.get_attribute("class")
    button_disabled = "disabled" in li_classes

    if not button_disabled:
        return next_page_button


def click_tag(webdriver, tag, delay_range):
    if tag:
        random_delay(2, delay_range)
        webdriver.execute_script("arguments[0].click();", tag)
        random_delay(2, delay_range)
    else:
        print("Trying to click unexisting or not loaded tag.")


def random_delay(minimum: int, range: int):
    time.sleep(random.uniform(minimum, minimum + range))


def slugify_product_name(product_name: str, space_character_replacement: str):
    slug = ''
    for character in product_name:
        if character == " ":
            slug += space_character_replacement
        else:
            slug += character
    return slug


def get_product_search_url(product_search: str):
    search_slug_dash = slugify_product_name(product_search, "-")
    search_slug_url_encoded = slugify_product_name(product_search, "%20")
    return f"https://listado.mercadolibre.com.ar/{search_slug_dash}#D[A:{search_slug_url_encoded}]"


#contemplate cases of searches wtih spaces: "cama dos plazas" -> /cama-dos-plazas#D[A:cama%20dos%20plazas]
product_search = ''
product_list_url = get_product_search_url(product_search)
data = []
web_driver = webdriver.Chrome() #instanciate driver for chrome
http_fetcher = HttpFetcher() #instanciate the object to make requests


#Test for a product search
extract_product_data(product_search, web_driver, http_fetcher, product_list_url)
csv_exporter = CsvExporter()
header = ['Title', 'Price', 'Score']
csv_exporter.createCsvFile(f'product_{product_search}.csv', header)
for product_list_data in data:
    for product_data in product_list_data:
        csv_exporter.append(product_data)