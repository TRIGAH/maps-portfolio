from flask import Flask, render_template,request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def get_website_logo(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the logo using common HTML tags and attributes
    possible_logo_tags = soup.find_all(['img', 'link'], {'rel': 'icon'})

    if possible_logo_tags:
        # Get the first logo tag
        logo_tag = possible_logo_tags[0]

        # Extract the logo URL
        if logo_tag.name == 'img':
            logo_url = logo_tag.get('src')
        elif logo_tag.name == 'link':
            logo_url = logo_tag.get('href')

        # Make the logo URL absolute if it's a relative URL
        logo_url = urljoin(url, logo_url)

        return logo_url

    return None

def extract_link_preview(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})

    return {
        'title': title.text.strip() if title else None,
        'description': description['content'].strip() if description else None,
        'image_url': get_website_logo(url),
        'web_url':url,
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        project_links = ['https://www.quarrter.com/','https://piggyvest.com/','https://www.vibes.com/','https://www.youtube.com/']
        link_preview_data = [extract_link_preview(link) for link in project_links]
        return render_template('index.html', link_preview=link_preview_data)


@app.route('/about')
def about():
    return render_template('generic.html')

@app.route('/more')
def more():
    return render_template('elements.html')

if __name__ == '__main__':
    app.run(debug=True)
