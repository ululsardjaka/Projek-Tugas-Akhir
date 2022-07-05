import time
import telegram
import requests
# import schedule
import urllib.request
from bs4 import BeautifulSoup
from telegram.ext import InlineKeyboardMarkup, InlineKeyboardButton


# Telegram Bot
infogempamassbot = "1641206173:AAFgbHPeIFkC_CO4Fu2oacAzfcwyekahUVc"
bot = infogempamassbot
# testbot = "1785945956:AAH3LHKCWZFofX-wuFnIOSrO4ebzmggmPRw"
# bot = telebot.TeleBot(testbot)

# InfoGempa BMKG
url = 'https://data.bmkg.go.id/DataMKG/TEWS/autogempa.xml'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')

# Shortcut Telebot
rt = bot.reply_to
sm = bot.send_message
sp = bot.send_photo
sca = bot.send_chat_action
erm = bot.edit_message_reply_markup

# ID Telegram 
admin_mass = "1668406442"
admin = "1820157143"
mass = "936017049"
bubu = "1309048511"

# Soup
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

# Bot InfoGempa BMKG X Mass
@bot.message_handler(commands=['start'])
def startcom(message):
	fn = message.chat.first_name
	ln = message.chat.last_name
	cid = message.chat.id
	username = message.chat.username
	text = message.text

	sca(cid,'typing')
	sm(cid, 'Hallo {}\n'.format(fn)+
		'Selamat datang di InfoGempa BMKG X Mass\n'+
		'Untuk mengetahui infogempa terkini /gempa\n'+
		'Terima kasih , {} telah menggunakan layanan kami'.format(fn))

	sm(admin_mass , 'First_name : {}\n'.format(fn)+
				'Last_name 	: {}\n'.format(ln)+
				'Username 	: @{}\n'.format(username)+
				'ID 		: {}\n'.format(cid)+
				'Text 		: {}\n'.format(text))

@bot.message_handler(commands=['gempa'])
def gempa(message):
	fn = message.chat.first_name
	ln = message.chat.last_name
	cid = message.chat.id
	username = message.chat.username
	text = message.text
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

	sm(admin_mass , 'First_name : {}\n'.format(fn)+
				'Last_name 	: {}\n'.format(ln)+
				'Username 	: @{}\n'.format(username)+
				'ID 		: {}\n'.format(cid)+
				'Text 		: {}\n'.format(text))

@bot.message_handler(commands=['sbubu'])
def start_bubu(message):
	cid = message.chat.id
	fn = message.chat.first_name
	ln = message.chat.last_name
	username = message.chat.username
	text = message.text
	sca(bubu, 'typing')
	sm(bubu , 'Bot ini memberitahukan informasi gempa bumi terkini')
	sca(bubu, 'typing')
	sm(bubu , 'Kalau mau info lebih lanjut silakan hubungi')
	sca(bubu, 'typing')
	sm(bubu , 'Sekian terimakasih ☺️')
	sm(admin_mass , 'First_name : {}\n'.format(fn)+
		'Last_name 	: {}\n'.format(ln)+
		'Username 	: @{}\n'.format(username)+
		'ID 		: {}\n'.format(cid)+
		'Text 		: {}\n'.format(text))

@bot.message_handler(commands=['gbubu'])
def gempabubu(message):
	fn = message.chat.first_name
	ln = message.chat.last_name
	cid = message.chat.id
	username = message.chat.username
	text = message.text
	ggempa = 'https://data.bmkg.go.id/DataMKG/TEWS/{}'.format(shakemap)
	urllib.request.urlretrieve(ggempa , 'img.png')
	sca(bubu, 'typing')
	sm(bubu , '=========I N F O G E M P A=========')
	# Gambar Pusat Gempa
	sca(bubu, 'upload_photo')
	sp(bubu , open('img.png','rb'))
	# Info Pusat Gempa
	sca(bubu, 'typing')
	sm(bubu,
	'⌚️ Waktu		:	{} , {}\n'.format(tanggal,jam)+
	'📍 Lokasi		:	{}\n'.format(wilayah)+
	'					{} , {} - {}\n'.format(coordinates,lintang,bujur)+
	'🌏 Magnitude	:	{}\n'.format(magnitude)+
	'⬇️ Kedalaman	:	{}\n'.format(kedalaman)+
	'📳 Dirasakan	:	{}\n'.format(dirasakan)+
	'🌊 Potensi		:	{}\n'.format(potensi))

	sm(admin_mass , 'First_name : {}\n'.format(fn)+
				'Last_name 	: {}\n'.format(ln)+
				'Username 	: @{}\n'.format(username)+
				'ID 		: {}\n'.format(cid)+
				'Text 		: {}\n'.format(text))

@bot.message_handler(func=lambda m: True)
def ec(message):
	cid = message.chat.id
	fn = message.chat.first_name
	ln = message.chat.last_name
	username = message.chat.username
	text = message.text
	sca(cid, 'typing')
	sm(cid , 'Maaf perintah yang {} masukan salah'.format(fn))

	sm(admin_mass , 'First_name : {}\n'.format(fn)+
			'Last_name 	: {}\n'.format(ln)+
			'Username 	: @{}\n'.format(username)+
			'ID 		: {}\n'.format(cid)+
			'Text 		: {}\n'.format(text))


# schedule.every(1).hours.do()

print("Bot is Online")

bot.polling()