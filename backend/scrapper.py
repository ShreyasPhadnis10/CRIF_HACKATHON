from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import asyncio
from bs4 import BeautifulSoup

from utils.executor import executor
from ner import title_sentiment_analyzer
from summerizer import generate_summary

@executor()
def get_company_articles(company_name: str) -> tuple:
    """Provide any company name to scrape article links from Google News."""
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get("https://www.news.google.com/search?q=" + company_name + " company")
    articles = driver.find_elements(By.XPATH, "//div[@class='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc']")
    links = []
    articles_list = []
    for article in articles:
        title = article.find_element(By.XPATH, ".//h3").text
        link = article.find_element(By.XPATH, ".//a").get_attribute("href")
        links.append(link)
        articles_list.append(title)
    driver.close()
    return (articles_list, links)


    #TODO: remove unnecessary text from the article

async def check_bad_articles(company_name: str):
    articles = await get_company_articles(company_name)
    bad_articles_list = []
    for article in zip(*articles):
        link = article[1]
        if await title_sentiment_analyzer(article[0]) < 0:
            text = await read_bad_articles(article[1])
            bad_articles_list.append((link, text))
    return bad_articles_list

async def main():
    a= await read_bad_articles("https://yourstory.com/2023/01/twitter-considering-selling-usernames-elon-musk")
    generate_summary(a)

if __name__ == "__main__":
    asyncio.run(main())
