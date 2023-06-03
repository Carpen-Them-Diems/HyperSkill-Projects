import requests
from bs4 import BeautifulSoup
import string
import os


# Get the number of pages and article type from the user
num_pages = int(input("Enter the number of pages to collect articles from:\n> "))
article_type = str(input("Enter the type of article you\'d like to collect:\n> "))

# Iterate over the number of pages
for i in range(1, num_pages + 1):
    # Create a directory for the current page
    os.makedirs(f'Page_{i}', exist_ok=True)

    # Make a request to the website
    r = requests.get(f"https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i}")

    # Parse the website's content with BeautifulSoup a.k.a BS4
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find all articles on the page
    articles = soup.find_all('article')

    # For each news article, follow the link and save the content
    for article in articles:
        # Check if the article type is the user's input
        if article.find('span', {'data-test': 'article.type'}).text == article_type:
            # Find the link to the article
            article_link = article.find('a', {'data-track-action': 'view article'}).get('href')
            # Create the full URL (Nature uses relative URLs)
            article_url = 'https://www.nature.com' + article_link
            # Make a request to the article page
            article_page = requests.get(article_url)
            # Parse the article page
            article_soup = BeautifulSoup(article_page.content, 'html.parser')
            # Find the article content
            article_content = article_soup.find('p', {'class': 'article__teaser'}).text.strip()
            # Find the article title and process it to create a valid filename
            article_title = article.find('a', {'data-track-action': 'view article'}).text
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            filename = ''.join(c for c in article_title if c in valid_chars)
            filename = filename.replace(' ', '_')
            # Write the article content to a file in the current page's directory
            with open(f'Page_{i}/{filename}.txt', 'wb') as f:
                f.write(article_content.encode('utf-8'))

print("Saved all articles.")

### Stage 4, keeping, so I can go back to look over it in the future... and yes it is somehow actually easier to -
# - just redo the code each step sometimes, lol. ###

# # Create a directory for the articles
# if not os.path.exists('NatureNews'):
#     os.makedirs('NatureNews')
#
# # Make a request to the website
# r = requests.get("https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3")
#
# # Parse the website's content with BeautifulSoup
# soup = BeautifulSoup(r.content, 'html.parser')
#
# # Find all articles on the page
# articles = soup.find_all('article')
#
# # For each news article, follow the link and save the content
# for article in articles:
#     # Check if the article type is 'News'
#     if article.find('span', {'data-test': 'article.type'}).text == 'News':
#         # Find the link to the article
#         article_link = article.find('a', {'data-track-action': 'view article'}).get('href')
#         # Create the full URL (Nature uses relative URLs)
#         article_url = 'https://www.nature.com' + article_link
#         # Make a request to the article page
#         article_page = requests.get(article_url)
#         # Parse the article page
#         article_soup = BeautifulSoup(article_page.content, 'html.parser')
#         # Find the article content
#         article_content = article_soup.find('p', {'class': 'article__teaser'}).text.strip()
#         # Find the article title and process it to create a valid filename
#         article_title = article.find('a', {'data-track-action': 'view article'}).text
#         valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
#         filename = ''.join(c for c in article_title if c in valid_chars)
#         filename = filename.replace(' ', '_') + '.txt'
#         # Write the article content to a file
#         with open(filename, 'wb') as f:
#             f.write(article_content.encode('utf-8'))


### Stage 1-3, keeping, so I can go back to look over it in the future ###

# import requests
# import json
# import bs4 as bs
# import re
#
# # Read the URL from the user
# url = input('Input the HTTPS://www.nature.com/articles/... URL:\n> ')
#
# # Try block to check the URL\'s validity
# # try:
# #     if 'https://www.nature.com/articles/' not in url:
# #         raise ValueError
#
#     # Headers/Parameters for GET request
# headers = {'Accept-Language': 'en-US,en;q=0.5'}
#
#     # Send a GET request to the URL
# response = requests.get(url, headers)
#
#     # Check if the request was successful and if there's a 'content' in the response
# if response.status_code == 200:
#
#     #     # Parse the HTML content of the response with BeautifulSoup a.k.a BS4
#     # soup = bs.BeautifulSoup(response.content, 'html.parser')
#     #
#     #     # Find the title and description
#     # title = soup.find('title').text
#     # description = soup.find('meta', attrs={'name': 'description'})['content']
#     #
#     #     # Print the title and description as a dictionary
#     # print({"title": title, "description": description})
#
#         # Open file in binary-write mode and save the response content to it
#     with open('source.html', 'wb') as file:
#         file.write(response.content)
#     print('Content saved.')
# else:
#         # Print an error message
#     print(f'The URL returned {response.status_code}!')
#
#     # else:
#     #     raise ValueError
# #
# # except ValueError as e:
# #     print(f'{e} Invalid page!')
