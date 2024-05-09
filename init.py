from fastapi import FastAPI, HTTPException
import uvicorn
import scrap, helpers

app = FastAPI()

@app.post("/product-information")
def product_information(product_url: str):
    try:
        product_data = scrap.scrape_amazon_product(product_url)
        product_name = product_data['product_name']
        product_rating = product_data['product_rating']
        product_reviews = product_data['product_reviews']
        product_reviews = helpers.extract_reviews(product_reviews)
        print(product_name)
        labels = []
        for review in product_reviews:
            review_title = review['review_title']
            review_text = review['review_text']
            label = helpers.predict_label(review_title, review_text)
            label_dict = {'review_text' : review_text, 'label' : label}
            labels.append(label_dict)
    except:
        raise HTTPException(status_code=404, detail="Product doesn't have enough or valid reviews")
    return labels



if __name__ == "__main__":
    
    uvicorn.run("init:app", host = "127.0.0.1", port = 8000, reload = True)