import requests

from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render, redirect
from requests.compat import quote_plus

from .forms import SearchForm
from .models import Search

BASE_SEARCH_URL = "https://losangeles.craigslist.org/search/?query={}"
BASE_IMG_URL = "https://images.craigslist.org/{}_300x300.jpg"

# Create your views here.
def index(request):
    form = SearchForm()
    frontend = {'form': form}
    return render(request, 'radzlist/base.html', frontend)


def searches(request):
    searches = Search.objects.all()
    list_searches = [s.as_dict() for s in searches]
    return JsonResponse(list_searches, safe=False)


def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search']
            
            if not Search.objects.filter(search=search):
                new_search = form.save(commit=False)
                new_search.save()

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

        form = SearchForm()

        frontend = {
            'form':form,
            'search': search,
            'final_posts': final_posts,
        }

        return render(request, 'radzlist/search.html', frontend)
    else:
        return redirect('index')