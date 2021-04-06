# importing dependencies 
from splinter import Browser
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request as urllib
from webdriver_manager.chrome import ChromeDriverManager
import requests
import time  


# scrape function that will execute all of the code from mission_to_mars
def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA MARS NEWS 
    # scrape the mars news site to collect the most recent article title and paragraph
    mars_url = "https://redplanetscience.com/"
    browser.visit(mars_url)

    # getting the html from site and scraping page into Soup
    mars_html = browser.html
    mars_soup = BeautifulSoup(mars_html, "html.parser")

    # collect news title and paragraph and save into variables
    # saving the news articles section of page into a variable
    news_articles = mars_soup.find('div', id='news')

    # scraping the fist articles title and putting it in a variable
    first_title = news_articles.find_all('div', 'content_title')[0].text
    
    # scraping first articles paragraph and putting it in a variable
    first_paragraph = news_articles.find_all('div', 'article_teaser_body')[0].text
    

    # JPL MARS SPACE IMAGES - FEATURED IMAGE
    # Finding current Featured Mars Image from website
    space_images_url = "https://spaceimages-mars.com/"
    browser.visit(space_images_url)

    # getting the html from mars images site and scraping page into BeautifulSoup
    space_images_html = browser.html
    space_images_soup = BeautifulSoup(space_images_html, 'html.parser')       

    # find the image url and store it in a variable
    image_url = space_images_soup.find(class_='headerimage fade-in')['src']
    print(image_url)

    # bring the two variables together to create the url 
    featured_image_url = space_images_url + image_url
    print(featured_image_url)


    # MARS FACTS
    # scrape webpage for the tables with pandas and turn into dataframes
    mars_facts_url = "https://galaxyfacts-mars.com/"

    fact_tables = pd.read_html(mars_facts_url)
    fact_tables

    # Get only the table containing information on mars
    mars_table = fact_tables[0]
    mars_df = pd.DataFrame(mars_table)
    mars_df

    # update column names
    mars_df.columns = mars_df.iloc[0]
    mars_df = mars_df.drop(mars_df.index[0])
    mars_df

    # convert to html table string
    html_table = mars_df.to_html()
    html_table  

    # strip unwanted new lines to clean up table
    html_table = html_table.replace('\n', '')
    html_table



    # MARS HEMISPHERES
    # url of site to get pictures from
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)

    # Getting the html from website and scraping it into soup 
    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')   

    image_items = hemisphere_soup.find_all('div',class_='item')
    print(image_items)

    # initializing empty dictionary to store image titles and url's (lists to temporarily hold them)
    title_list = []
    url_list = []
    image_title_url_dict = []

    # loop through html text and find the h3's and img sources for each hemisphere
    for hemisphere in image_items:
        if hemisphere.h3:
            title = hemisphere.h3.text
            title_list.append(title)
        if hemisphere.img:
            image_src = hemisphere.find('img')['src']
            url_list.append(image_src)

    # for loop adding contents of lists into dictionary
    for title, img_url in zip(title_list, url_list):
        title_url = {"title": title, "image_url": hemisphere_url+img_url}
        image_title_url_dict.append(title_url)

    image_title_url_dict


    # adding all of the scraped data into a single dictionary which will then go into a MongoDB
    mars_data = {
        "news_title": first_title,
        "news_paragraph": first_paragraph,
        "featured_image": featured_image_url,
        "mars_fact_table": html_table,
        "hemisphere_title_1": image_title_url_dict[0]["title"],
        "hemisphere_image_1": image_title_url_dict[0]["image_url"],
        "hemisphere_title_2": image_title_url_dict[1]["title"],
        "hemisphere_image_2": image_title_url_dict[1]["image_url"],
        "hemisphere_title_3": image_title_url_dict[2]["title"],
        "hemisphere_image_3": image_title_url_dict[2]["image_url"],
        "hemisphere_title_4": image_title_url_dict[3]["title"],
        "hemisphere_image_4": image_title_url_dict[3]["image_url"]
    }


    browser.quit()

    return mars_data

