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
    news_headline = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text

    # Return headline and paragraph text
    return news_headline, news_paragraph

    # Exit Browser
    browser.quit()

##### Store all data #####

# Create dictionary to store data
mars_data =  {
    "news_headline" = news_headline,
    "news_paragraph" = news_paragraph,
    

}