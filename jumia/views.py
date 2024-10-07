
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def jumia_data(request):
    category = request.GET.get('category')
    max_price = request.GET.get('max')
    url = 'https://www.jumia.com.tn/smartphones/'
    if category is not None:
        url += category + '/'
    if max_price is not None:
        url += f'?price=0-{max_price}'
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('article', {'class': 'prd _fb col c-prd'})
    except:
        print("error")
        products = []
        
    smartphones = []
    for product in products:
        name = product.find('h3', {'class': 'name'}).text
        price = product.find('div', {'class': 'prc'}).text
        link = product.find('a', {'class': 'core'}).get('href')
        image = product.find('img', {'class': 'img'}).get('data-src')
        smartphone = {
            'name': name,
            'price': price,
            'link': link,
            'image': image
        }
        smartphones.append(smartphone)
    
    urlCategorie = 'https://www.jumia.com.tn/smartphones/'
    try:
        responseForCat = requests.get(urlCategorie)
        soupForCat = BeautifulSoup(responseForCat.content, 'html.parser')
        categories= soupForCat.find('div', {'class': '-phs -pvxs -df -d-co -h-168 -oya -sc'})
        Categories = [c.text.replace(" ", "-") for c in categories]
    except:



        Categories = []
    
    template = loader.get_template('jumiaData.html')
    context = {
        'smartphones': smartphones,
        'category': category,
        'max_price': max_price,
        'Categories': Categories,
    }
    return HttpResponse(template.render(context, request))



def detailsPhone(request, name):
    url = 'https://www.jumia.com.tn/' + name
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get product name, image, and price
    product = soup.find('section', {'class': 'col12 -df -d-co'})
    
    #get the name of the product
    
    name = product.find('h1', {'class': '-fs20 -pts -pbxs'}).text
    
    image  = product.find('img', {'class': '-fw -fh'}).get('data-src')
    
    price = product.find('span', {'class': '-b -ltr -tal -fs24'}).text
   

    # Get characteristics
    characteristics = []

    char_section = soup.find('div', {'class': 'markup -pam'})
    if char_section:
        char_items = char_section.find_all('li')
        for char_item in char_items:
            characteristics.append(char_item.text)


    # Get technical description
    technical_description = []
    tech_section = soup.find('ul', {'class': '-pvs -mvxs -phm -lsn'})
    if tech_section:
        tech_items = tech_section.find_all('li')
        for tech_item in tech_items:
            technical_description.append(tech_item.text.strip())

    # Get description
    description = []
    desc_section = soup.find('div', {'class': 'markup -mhm -pvl -oxa -sc'})
    if desc_section:
        desc_items = desc_section.find_all('p')
        for desc_item in desc_items:
            description.append(desc_item.text.strip())

    context = {
        'name': name,
        'image': image,
        'price': price,
        'characteristics': characteristics,
        'technical_description': technical_description,
        'description': description
    }

    return render(request, 'detailsSmartPhone.html', context)
