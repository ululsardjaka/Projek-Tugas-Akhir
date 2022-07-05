import time
import telegram
import requests
# import schedule
import urllib.request
from bs4 import BeautifulSoup
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


bot = "1641206173:AAFgbHPeIFkC_CO4Fu2oacAzfcwyekahUVc"
url = 'https://data.bmkg.go.id/DataMKG/TEWS/autogempa.xml'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

rt = bot.reply_to
sm = bot.send_message
sp = bot.send_photo
sca = bot.send_chat_action
erm = bot.edit_message_reply_markup

jam = soup.infogempa.jam.text
tanggal = soup.infogempa.tanggal.text
wilayah = soup.infogempa.wilayah.text
coordinates = soup.infogempa.coordinates.text
lintang = soup.infogempa.lintang.text
bujur = soup.infogempa.bujur.text
magnitude = soup.infogempa.magnitude.text
kedalaman = soup.infogempa.kedalaman.text
potensi = soup.infogempa.potensi.text
dirasakan = soup.infogempa.dirasakan.text
shakemap = soup.infogempa.shakemap.text

@bot.message_handler(commands=['gempa'])
def gempa(message):
        cid = message.chat.id
        ggempa = 'https://data.bmkg.go.id/DataMKG/TEWS/{}'.format(shakemap)
        urllib.request.urlretrieve(ggempa , 'img.png')
        sca(cid, 'typing')
        sm(cid , '=========I N F O G E M P A=========')
        # Gambar Pusat Gempa
        sca(cid, 'upload_photo')
        sp(cid , open('img.png','rb'))
        # Info Pusat Gempa
        sca(cid, 'typing')
        sm(cid,
        '⌚️ Waktu		:	{} , {}\n'.format(tanggal,jam)+
        '📍 Lokasi		:	{}\n'.format(wilayah)+
        '					{} , {} - {}\n'.format(coordinates,lintang,bujur)+
        '🌏 Magnitude	:	{}\n'.format(magnitude)+
        '⬇️ Kedalaman	:	{}\n'.format(kedalaman)+
        '📳 Dirasakan	:	{}\n'.format(dirasakan)+
        '🌊 Potensi		:	{}\n'.format(potensi))

bot.polling()