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
    
    # Return result
    return news_headline, news_paragraph

##### Mars Featured Image #####

def mars_feature(): 
    # Initiate browser
    browser = init_browser()

    # Visit the Mars images url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Add time sleep to prevent erroring out
    time.sleep(1)

    #Click on image button and then click for more info
    browser.find_by_id('full_image').click()
    browser.links.find_by_partial_text('more info').click()

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find the relative image path
    relative_image_path = soup.select_one("figure", class_="lede").a["href"]

    # Set the main url for all the JPL images
    jpl_url = "https://www.jpl.nasa.gov/"

    # Create the link to the large image
    featured_url = jpl_url + relative_image_path

    # Return result
    return featured_url

##### Mars Facts #####

def mars_facts(): 
    facts_url = "https://space-facts.com/mars/"

    # Scrape table with pandas
    facts_df = pd.read_html(facts_url)[0]

    # Change column names
    facts_df.columns = ['Category', 'Value']

    # Save table as html
    mars_table = facts_df.to_html(index = False)

    # Return result
    return mars_table

##### Mars Hemisphere #####

def mars_hemisphere(): 

    # Initiate browser
    browser = init_browser()

    # Visit 
    main_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(main_url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # URL for images
    hemisphere_url = "https://astrogeology.usgs.gov"

    # Find all the links
    image_links = soup.find_all('div', class_='item')

    # Create 
    hemisphere_links = []

    # Loop through the links and store the information

    for link in image_links:
        # Get Title
        title = link.find("h3").text
        
        # Remove "Enhanced" from the title
        title = title.split(' Enhanced')[0]
        
        # Get link for hemisphere page
        hemi_link = link.find("a")["href"]
        hemi_url = hemisphere_url + hemi_link
        
        # Click on image button and then click for more info
        browser.visit(hemi_url)
    
        # Add time sleep to prevent erroring out        
        time.sleep(2)
    
        # Scrape page into Soup
        html = browser.html
        soup = bs(html, "html.parser")
    
        # Find the full image url
        full_image_url = soup.find("li").a['href']
    
        # Append both title and full image url to hemisphere links.
        hemisphere_links.append({'title': title, 'image': full_image_url}) 

    return hemisphere_links

##### Store all data #####

# Create dictionary to store data
def scrape_all():
    browser = init_browser()
    news_headline, news_paragraph = mars_news()
    featured_url = mars_feature()
    mars_table = mars_facts()
    hemisphere_links = mars_hemisphere()

    data = {
        "news_headline": news_headline,
        "news_paragraph": news_paragraph,
        "featured_url": featured_url,
        "mars_table": mars_table,
        "hemisphere_links": hemisphere_links
    }

    # Close the browser after scraping
    browser.quit()

    return data 