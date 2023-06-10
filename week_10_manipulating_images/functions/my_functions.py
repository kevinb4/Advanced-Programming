import os
import shutil
import zipfile
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from bs4 import BeautifulSoup

def get_data(url):
    """Download images from url and save them to a folder
    Arguments:
        url [string] -- url to download images from
    Returns:
        people [array] -- array of dicts with info about each person"""
    if os.path.exists('images'): # clear images when starting over
        shutil.rmtree('images')
        os.mkdir('images')

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div', class_='card')

    # split the paths to remove the last one so the images can work
    routes = url.split('/')[:-1]
    path = ""

    # rebuild the path without the last part
    for route in routes:
        path += route + '/'

    # save logo
    with open('images/logo.jpg', 'wb') as file:
        img = requests.get(path + soup.find('img')['src'])
        file.write(img.content)

    # save info about each person in an array of dicts
    people = []

    for div in divs:
        person = {}
        person['image'] = 'images/' + div.img["src"].split("/")[1]
        info = div.h5.text.split(',')
        person['name'] = info[0].strip()
        person['title'] = info[1].strip()

        people.append(person)

        # save image
        with open(f'images/{div.img["src"].split("/")[1]}', 'wb') as file:
            img = requests.get(path + div.img['src'])
            file.write(img.content)

    return people

def process_images(people):
    """Process images
    Arguments:
        people [array] -- array of dicts with info about each person"""
    for person in people:
        image = Image.open(person['image'])
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("fonts/Syne-Regular.otf", 20)

        if not os.path.exists('images/output_images'):
            os.mkdir('images/output_images')

        # add logo
        logo = Image.open('images/logo.jpg')
        logo = logo.resize((100, 50), Image.Resampling.LANCZOS) # resize so it fits
        image.paste(logo, (10, image.size[1] - 100), logo)

        # draw the text at the bottom left of the image
        draw.text((10, image.size[1] - 50), f"Name: {person['name']}\nTitle: {person['title']}", (0, 0, 0), font)
        
        image.save("images/output_images/" + person['image'].split('/')[1])

def zip_images(path):
    """Zip up the modified images
    Arguments:
        path [string] -- path to the folder with the images"""
    with zipfile.ZipFile('images/output_images.zip', 'w') as file:
        os.chdir(path) # change the dir so the zip file doesn't have extra folders
        for image in os.listdir():
            file.write(image)
