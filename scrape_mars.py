##### Import and Setup #####

#Imports and dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


# Define init_browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "../chromedriver_win32/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

##### NASA Mars News #####

def mars_news(): 
    # Initiate browser
    browser = init_browser()

    # Visit the Mars New Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Add time sleep to prevent erroring out
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
        
    # Get the headline and paragraph text
    headline_list = soup.find("div", class_="list_text")
    news_headline = headline_list.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    
    return news_headline, news_paragraph


##### Store all data #####

# Create dictionary to store data
def scrape_all():
    browser = init_browser()
    news_headline, news_paragraph = mars_news()


    data = {
        "news_headline": news_headline,
        "news_paragraph": news_paragraph,
    }

    # Close the browser after scraping
    browser.quit()

    return data 