from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser ("chrome", **executable_path, headless=False)

def scrape():
    mars_data = {}
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_data["news_title"] = soup.find("div", class_ ="list_text").text

    
    mars_data["news_paragraph"] = soup.find("div", class_="article_teaser_body").text
    
    #mars image
    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url)

    html_image = browser.html

    soup = bs(html_image, "html.parser")

    featured_image_url = soup.find("article")["style"].replace('background-image: url(','').replace(');', '')[1:-1]

    main_url = "https://www.jpl.nasa.gov"

    featured_image_url = main_url + featured_image_url

    mars_data["featured_image_url"] = featured_image_url

    #Mars Weather
    import time
    twitter_weather_url= "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_weather_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")
    results = soup.find_all("div", class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    mars_data["latest_results"] = results[1]

    #Mars Fact
    mars_facts_url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_facts_url)
    mars_facts[0]
    mars_facts_df = mars_facts[0]
    mars_facts_df.columns = ["Perameter', 'Facts"]
    mars_facts_df.to_html("mars_facts_df.html")
    mars_facts = mars_facts_df.html()
    mars_data["mars_facts"] = mars_facts

    return mars_data



