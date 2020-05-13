import requests

from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from requests.compat import quote_plus

from .models import Search

BASE_SEARCH_URL = "https://losangeles.craigslist.org/search/sss?query={}"
BASE_IMG_URL = "https://images.craigslist.org/{}_300x300.jpg"

# Create your views here.
def index(request):
    return render(request, 'radzlist/base.html')


def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        Search.objects.create(search=search)
        final_url = BASE_SEARCH_URL.format(quote_plus(search))
        
        response = requests.get(final_url)
        data = response.text
        soup = BeautifulSoup(data, features='html.parser')
        
        posts = soup.find_all('li', class_='result-row')

        final_posts = []

        for post in posts:
            post_title = post.find('a', class_='result-title').text
            post_link = post.find('a', class_='result-title').get('href')
            
            if post.find('span', class_='result-price'):
                post_price = post.find('span', class_='result-price').text
            else:
                post_price = 'N/A'

            if post.find('a', class_='result-image gallery'):
                image_ids = post.find('a', class_='result-image gallery').get('data-ids')
                image_id = image_ids.split(',')[0].split(':')[1]
                post_image = BASE_IMG_URL.format(image_id)
            else:
                post_image = "https://www.craigslist.org/images/peace.jpg"

            final_posts.append((post_title, post_link, post_price, post_image))

        frontend = {
            'search': search,
            'final_posts': final_posts,
        }

        return render(request, 'radzlist/search.html', frontend)
    else:
        return redirect('/')