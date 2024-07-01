from flask import Flask, jsonify

app = Flask(__name__)

products = [
    # Define sample product data with desired attributes
    {
        "id": 1,
        "name": "Product 1",
        "company": "Company A",
        "category": "Electronics",
        "price": 100,
        "rating": 4.5,
        "discount": 10,
        "availability": "In Stock",
    },
    # ... Add more sample products
]

@app.route('/api/products')
def get_products():
  return jsonify(products[:5])  # Return top 5 products

if __name__ == '__main__':
  app.run(debug=True, port=9876)
