import requests
from bs4 import BeautifulSoup
import emoji

def scrape_amazon_product(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract product name
    product_name = soup.select_one('#productTitle').get_text(strip=True)
    
    # Extract product rating
    rating_element = soup.select_one("#acrPopover")
    product_rating = rating_element.attrs.get('title')
    
    # Extract product reviews
    product_reviews = []
    review_elements = soup.select('[data-hook="review"]')
    for review_element in review_elements:
        author_name = review_element.select_one('.a-profile-name').get_text(strip=True)
        author_name = str(emoji.demojize(author_name))
        review_rating = review_element.select_one('.a-icon-alt').get_text(strip=True)
        review_title = review_element.select_one('.review-title').get_text(strip=True)
        review_title = str(emoji.demojize(review_title))
        review_text = review_element.select_one('.review-text').get_text(strip=True)
        review_text = str(emoji.demojize(review_text))
        review_date = review_element.select_one('.review-date').get_text(strip=True)
        verified_purchase = review_element.select_one('.a-row.a-spacing-mini.review-data.review-format-strip span.a-size-mini').get_text(strip=True)
        product_reviews.append({
            'author_name': author_name,
            'review_rating': review_rating,
            'review_title': review_title,
            'review_text': review_text,
            'review_date': review_date,
            'verified_purchase': verified_purchase
        })
    
    # Return the extracted data
    return {
        'product_name': product_name,
        'product_rating': float(product_rating.split(" ")[0]),
        'product_reviews': product_reviews
    }

