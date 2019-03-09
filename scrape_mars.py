#import dependencies
import pandas as pd
import requests
import pymongo
from bs4 import BeautifulSoup as bs
from splinter import Browser
#!which chromedriver
from IPython.display import display, HTML

#scrape function
def scrape():

	#Create empty mars dictiomary
	mars = {}
	executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
	browser = Browser('chrome', headless=False)

	##################
	#NASA Mars News
	##################
	url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
	browser.visit(url)

	#Add condition telling browser to wait before retrieving html to give it time to load
	if browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5):
		html = browser.html

	# Retrieve page with the requests module
	response = requests.get(url)
	# Create BeautifulSoup object; parse with 'lxml'
	soup = bs(html, 'lxml')

	# Collect the latest News Title and Paragraph Text. Assign text to variables
	# Limit results to the first 40 elements of relevant class, because we are interested in the slides with this element.
	# Other parts of the page use the same class, which is why we impose the limit
	titles = soup.find_all('div',  class_='content_title', limit=40)
	titles

	slides = soup.find_all('li',  class_='slide', limit=40)

	# Loop through returned results
	for slide in slides:
	    # Error handling
	    try:
	        # Identify and return title of listing
	        clean_title = slide.find('div', class_='content_title').text
	        #add .text to the end to specify that we exclude the descendant 'href' link anchored within..
	        #..'content_title' 
	        #Note, the 'a' anchor begins before the href link and ends at the end of the title text
	        
	        # Identify and return paragraph
	        par_text = slide.find('div', class_= 'article_teaser_body').text
	            #we add .text to exclude the div class from being included in results
	        # Identify and return link to listing
	        link = slide.a['href']

	        # Run only if title, price, and link are available
	        if (clean_title and par_text and link):
	            # Print results
	            print('-------------')
	            print(clean_title)
	            print(par_text)
	            print("https://mars.nasa.gov/" + link)

	            mars['title'] = clean_title
	            mars['article teaser'] = par_text


	    except Exception as e:
	        print(e)



	#######################
	#JPL Mars Space Images
	#######################

	jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

	browser.visit(jpl_url)


	html = browser.html
	soup2 = bs(html, 'lxml')

	buttons = soup2.find('a',  class_='button fancybox')
	#buttons

	link2 = soup2.find_all('a', class_='button fancybox')[0].get('data-fancybox-href')

	featured_image_url = "https://www.jpl.nasa.gov/" + link2
	featured_image_url


	link2 = soup2.find_all('a', class_='button fancybox')[0].get('data-fancybox-href')

	featured_image_url = "https://www.jpl.nasa.gov/" + link2
	mars['featured_image_url'] = featured_image_url


	###############
	#Mars Weather
	###############

	weather_url = "https://twitter.com/marswxreport?lang=en"

	browser.visit(weather_url)

	html = browser.html

	soup3 = bs(html, "html.parser")
	##############################

	#scrape the latest Mars weather tweet
	mars_weather = soup3.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text
	mars['mars_weather'] = mars_weather


	###################
	#Mars Facts
	###################
	wait_time=1
	facts_url = "https://space-facts.com/mars/"
	browser.visit(facts_url)

	html = browser.html
	soup4 = bs(html, "lxml")

	#Scrape the table. Use Pandas to convert the data to a HTML table string
	table = pd.read_html(facts_url)
	#table
	# convert table list to DF
	facts_df = table[0]
	facts_df
	#convert DF to html
	#mars_facts = facts_df.to_html('facts.html')
	mars_facts = facts_df.to_html()	
	mars['mars_facts'] = mars_facts

	##################
	#Mars Hemispheres
	##################

	hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(hemi_url)
	html = browser.html
	soup5 = bs(html, "lxml")

	# Empty list 
	hemisphere = []

	links = browser.find_by_css('a.product-item h3')
	#Empty dictionary
	dict = {}
	for l in range(len(links)):

		browser.find_by_css('a.product-item h3')[l].click()
		#wait_time=0.5
		sample = browser.find_link_by_text('Sample').first
		#wait_time=0.5
		img_url = sample['href']
		dict['img_url'] = img_url
		title = browser.find_by_css('h2.title').text
		dict['title'] = title
		#Append the dictionary to the list 'hemisphere'
		hemisphere.append(dict)
		browser.back()
	

	mars['hemisphere'] = hemisphere

##########################################################
	return mars 



