from flask import Flask, jsonify
from flask import render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_weather_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        xpath_element = soup.select_one(
            'html body app-root app-today one-column-layout wu-header sidenav mat-sidenav-container mat-sidenav-content div section div:nth-of-type(3) div:nth-of-type(1) div div:nth-of-type(1) div:nth-of-type(1) lib-city-current-conditions div div:nth-of-type(2) div div div:nth-of-type(3) span'
        )

        if xpath_element:
            return {"weather_data": xpath_element.text.strip()}
        else:
            return {"weather_data": "Data not found."}
    else:
        print("Error accessing the website.")
        return None

@app.route('/')
def index():
    url = "https://www.wunderground.com/weather/us/az/tucson/KAZTUCSO658"
    try:
        data = scrape_weather_data(url)
        return jsonify(data)
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while fetching the weather data."})


if __name__ == "__main__":
    app.run(debug=True)
