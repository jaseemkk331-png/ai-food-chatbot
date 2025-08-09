from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import textstat

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    if not url:
        return "Please enter a URL", 400

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return "Failed to fetch the URL.", 400

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)

    readability = textstat.flesch_reading_ease(text)

    return render_template('result.html', url=url, readability=readability)

if __name__ == "__main__":
    app.run()