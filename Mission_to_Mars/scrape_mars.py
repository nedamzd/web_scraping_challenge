from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser=Browser('chrome', **executable_path, headless=False)



# NASA Mars News
def marsnews():
    mars_url = 'https://www.redplanetscience.com'
    browser.visit(mars_url)
    news_html = browser.html
    news_soup = bs(news_html, 'html.parser')
    news_title = news_soup.find('div', class_='content_title').text
    news_p = news_soup.find('div', class_="article_teaser_body").text
    news = [news_title, news_p]

    return news

 #JPL Mars Space Images - Featured Image
def mars_fimg():
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    jpl_html = browser.html
    fimg_soup = bs(jpl_html, 'html.parser')
    featured_image_url_rel=fimg_soup.find('img', class_="headerimage")['src']
    fimg_url=jpl_url+featured_image_url_rel
    fimg_name = fimg_soup.find('h1', class_='media_feature_title').text
    fimg=[fimg_name,fimg_url]
    return fimg

#Mars Facts
def mars_facts():
    url_3 = 'https://galaxyfacts-mars.com/'
    browser.visit(url_3)
    tables = pd.read_html(url_3)
    mars_table=tables[1]
    mars_table.columns=['Dimension', 'Value']
    mars_table.set_index("Dimension", inplace=True)
    mars_table_html=mars_table.to_html()
    return mars_table_html

# Mars Hemisphere
def mars_hemi():
    url_4 = 'https://marshemispheres.com/'
    browser.visit(url_4)
    html = browser.html
    mars_hemi_soup = bs(html, 'html.parser')
    links = []
    names = []
    results = mars_hemi_soup.find_all('div', class_='item')
    for result in results:
        name=result.find('h3').text
        names.append(name)
        link_rel = result.find('a')['href']
        link=url_4 + link_rel
        links.append(link)
    img_links = []
    
    for link in links:
        url_5 = link
        browser.visit(url_5)
        html = browser.html
        soup = bs(html, 'html.parser')
        img = soup.find('img', class_="wide-image")['src']
        img_link = url_4+img
        img_links.append(img_link)

    df=pd.DataFrame({'title':names,'img_url':img_links})
    hemisphere_image_urls = df.to_dict('records')
    return hemisphere_image_urls
##################################################

##############################
# Set up scrape and dictionary
def scrape():

    mars_dict= {}
    news=marsnews()
    fimg=mars_fimg()
    mars_dict["news_title"]=news[0]
    mars_dict["news_paragraph"]=news[1]
    mars_dict["featured_image_name"]=fimg[0]
    mars_dict["featured_image_url"]=fimg[1]
    mars_dict["mars_facts"]= mars_facts()
    mars_dict["hemisphere_images"]=mars_hemi()
    
    browser.quit()
    return mars_dict

# results=scrape()
# print(results)


