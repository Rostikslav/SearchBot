import discord
from discord.ext import commands
import requests
import urllib.request
from bs4 import BeautifulSoup
from PIL import Image
import random
import time
import os

class MyClient(discord.Client):

    @client.event
    async def on_message(self, message):
        msg = message.content
        help_list = {'.help', '.hlp', '.hel[', '.info', '.инфо', 'юинфо', '.хелп', 'юхелп', 'юхэлп', '.хэлп', ',инфо', ',хелп', ',хэлп', '-инфо', '-хелп', '-хэлп', '.infp', '.unfo', '.unfp', ',help', ',hlp', ',hel[', ',info', ',infp', ',unfo', ',unfp', '/help', '/hlp', '/hel[', '/info', '/infp', '/unfo', '/unfp'}
        bad_list = ('sex', 'seks', 'pidor', 'penis', 'pisun', 'pisiun', 'gej', 'gei', 'tits', 'butt', 'siski', 'zhopa', 'zopa', 'jopa', 'jhopa', 'секс', 'писюн', 'пидор', 'жопа', 'сиськи', 'писька', 'письки', 'гей', 'сиська', 'гандон', 'очко', 'залупа', 'пизда')

        if msg.startswith('.search ') or msg.startswith('.искать ') or msg.startswith('-искать ') or msg.startswith('.bcrfnm ') or msg.startswith('.ыуфкср ') or msg.startswith('юыуфкср '):
            search_name = msg[8:]
            start_url = 'https://www.shutterstock.com/ru/search/'
            url = start_url + search_name
            HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36' }

            def get_html(url, params = None):
                r = requests.get( url, headers = HEADERS, params = params )
                return r

            def download_img(url):
                full_path = 'images/image.png'
                urllib.request.urlretrieve(url, full_path)

            def crop_img():
                img = Image.open('images/image.png')
                width = img.size[0]
                height = img.size[1]
                area = (0, 0, width, height-20)
                cropped_img = img.crop(area)
                cropped_img.save('images/image.png')

            def get_content(html):
                soup = BeautifulSoup( html, 'html.parser' )
                items = soup.find_all('img', class_='z_h_e')
                images_urls = []
                for item in items:
                    images_urls.append( item.get('src') )

                if len(images_urls) != 0:
                    try:
                        download_img( random.choice(images_urls) )
                        crop_img()
                        return True
                    except:
                        return False
                else:
                    return False

            def parse():
                html = get_html(url)
                if html.status_code == 200:
                    get_content(html.text)
                else:
                    pass
            parse()

            channel = message.channel
            try:
                if search_name in bad_list:
                    emb = discord.Embed(title = 'Ну ты и извращенец xD', colour = 0xAD2049)
                    await channel.send(embed = emb)
                await channel.send(file=discord.File('images/image.png'))
                os.remove('images/image.png')
            except:
                emb = discord.Embed(title = 'Что-то пошло не так :( \n Попробуй другое слово', colour = 0xAD2049)
                await channel.send(embed = emb)
        elif msg in help_list:
            emb = discord.Embed(title = 'Возможные команды', colour = 0xAD2049)
            emb.add_field( name = '.help / .info / .инфо / .хелп', value = 'Показать возможные команды')
            emb.add_field( name = '.search / .искать / -искать <слово>', value = 'Поиск картинки по названию')
            channel = message.channel
            await channel.send(embed = emb)

client = MyClient()
token = os.environ.get('BOT_TOKEN')