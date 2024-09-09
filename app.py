from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
import time

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review', methods=['GET'])
@cross_origin()
def index():
    # Use GET for the form submission
    if request.method == 'GET':
        try:
            searchString = request.args.get('content').replace(" ", "+")  # Get the query parameter from GET request
            reviews = []  # Initialize an empty list for reviews

            for page in range(1,2):  # Loop through multiple pages
                url = f'https://bikroy.com/data/serp?top_ads=2&spotlights=5&sort=relevance&buy_now=0&urgent=0&categorySlug=mobiles&locationSlug=bangladesh&category=101&query={searchString}&page={page}&filter_json=[]'
                
                req = requests.get(url)
                time.sleep(3)  # Add delay to avoid overloading the server
                response = req.json()

                print(f"Page {page} done")

                for product in range(0, 25):
                    try:
                        price = response['ads'][product]['price']
                    except KeyError:
                        price = "Not Available"

                    data_json = {
                        'Product': response['ads'][product]['title'],
                        'Name': response['ads'][product]['title'],
                        'Rating':3,
                        'CommentHead': response['ads'][product]['description'],
                        'Comment': price
                    }
                    reviews.append(data_json)  # Append the data to the reviews list

            return render_template('results.html', reviews=reviews)
        except Exception as e:
            print('The Exception message is:', e)
            return f'Something is wrong: {str(e)}'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
