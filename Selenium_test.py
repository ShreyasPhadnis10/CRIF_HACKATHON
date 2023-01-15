from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from textblob import TextBlob


path = "C:\Program Files (x86)\chromedriver.exe"


from backend.ner import risk_entities

# driver.get("https://news.google.com")
# print(driver.title)

# search = driver.find_element("name", "q")
# search.send_keys("Mit wpu")
# search.send_keys(Keys.RETURN)

# print(driver.page_source)

# time.sleep(5)

# driver.quit()

titles = []
links = []

negative_articles = {}
detail = []

negative_articles["detail"] = detail
score = 0


def sentiment_analysis(title, link):
    blob = TextBlob(title)
    
    sentiment = blob.sentiment.polarity 
    if (sentiment < 0):
        
        detail.append(
            {"title": title,
             "link": link,
             "score": sentiment
            }
        )


    





def get_company_articles(company_name: str) -> list:
    driver = webdriver.Chrome(path)
    """Provide any company name to scrape article links from Google News."""
    
   
    driver.get("https://www.news.google.com/search?q=" + company_name + " company");
    articles = driver.find_elements(By.XPATH, "//div[@class='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc']");
  
 

    for num, article in enumerate(articles):
        # titles = []
        title = article.find_element(By.XPATH, ".//h3").text
        link = article.find_element(By.XPATH, ".//a").get_attribute("href")
        titles.append(title)
        links.append(link)

    for i in range(0, len(titles)):
    
        sentiment_analysis(titles[i], links[i])

    
    risk_entities(titles, company_name)

    driver.close();
    

    return negative_articles 

    
    


