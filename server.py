import requests
from flask import Flask, render_template, jsonify
from yelp_scraper import yelp_info


app = Flask(__name__)


@app.route("/<city><state>", methods=['GET'])
def get_info(city, state):
    return jsonify(yelp_info(city, state))


if __name__ == '__main__':
    # change to your own port
    app.run(host='0.0.0.0', port=3000, debug=True)