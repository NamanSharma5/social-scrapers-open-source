from dataclasses import dataclass

from flask import Flask, render_template
import instagram_scraper
from post import Post

app = Flask(__name__)


@app.route("/")
def landing_page():
    return render_template("landing.html")

@app.route("/instagram/account/", methods=['GET'])
def test():
    return "Please specifc account type: public or private [not supported yet]"

@app.route("/instagram/account/public/<username>", methods=['GET'])
def return_information_for_public_account(username):
    scraped_details = instagram_scraper.overall_description_and_picture_scraper(username)
    return render_template("main.html", scraped_details=scraped_details)

@app.route("/api/<username>", methods=['GET'])
def return_information_for_public_account_api(username):
    scraped_details = instagram_scraper.overall_description_and_picture_scraper(username)
    classes = [Post(details[0], details[1], details[2]) for details in scraped_details]
    return classes

if __name__ == '__main__':
    app.run()