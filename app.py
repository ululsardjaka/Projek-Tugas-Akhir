import requests, re, logging
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

BOT_TOKEN   = "1347046475:AAEiu5OtiWp5AiF3UI4YB44K5aUjoDF7Qkw"
BASE_URL    = "https://www.accuweather.com/id"
HEADERS     = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.41'}

PILIHAN, CARI_LOKASI, SIMPAN_LOKASI, CUACA_SEKARANG, CUACA_HARIAN = range(5)
KEYBOARD_PILIHAN = [['Cuaca Sekarang', 'Cuaca Harian'], ['Tentang', 'Keluar']]
WELCOME_MESSAGE = """Halo, Saya adalah bot untuk forecast cuaca
Berikut hal yang bisa saya lakukan:
-> Lihat Cuaca Sekarang
-> Lihat Cuaca Harian"""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
import os
PORT = int(os.environ.get('PORT', 5000))

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=ReplyKeyboardMarkup(KEYBOARD_PILIHAN),
    )

    return PILIHAN


def pilihan(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.lower()
    lokasi = context.user_data.get('lokasi', 'Not set')
    if user_input == 'cuaca sekarang':
        context.user_data['pilihan_cuaca'] = 'sekarang'
        if lokasi == 'Not set':
            update.message.reply_text('Lokasi belum diatur, Silahkan masukkan lokasi anda', reply_markup=ReplyKeyboardRemove())
            return CARI_LOKASI
        else:
            cuaca_sekarang(update, context)
    elif user_input == 'cuaca harian':
        context.user_data['pilihan_cuaca'] = 'harian'
        if lokasi == 'Not set':
            update.message.reply_text('Lokasi belum diatur, Silahkan masukkan lokasi anda', reply_markup=ReplyKeyboardRemove())
            return CARI_LOKASI
        else:
            cuaca_harian(update, context)
    elif user_input == 'tentang':
        reply = WELCOME_MESSAGE
    else:
        reply = 'Maaf bot tidak mengetahui maksud anda'

    update.message.reply_text(reply)
    return PILIHAN

def query_search(update: Update, context: CallbackContext) -> int:
    url = "{}/search-locations?query={}".format(BASE_URL, update.message.text)
    html = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(html.text, 'lxml')
    try:
        result = soup.findAll('div', {'class': 'search-results'})[1].findAll('a', href=True)
        reply = ''
        lokasi = []
        for i, item in enumerate(result, start=1):
            data = {}
            label = item.getText(strip=True)
            data['key'] = re.findall('/web-api/three-day-redirect\?key=(.*)&target=', item['href'])[0]
            kota_negara = item.getText(strip=True).split(', ')
            data['kota'] = kota_negara[0].lower().replace(' ', '-')
            data['negara'] = kota_negara[-1].lower()
            lokasi.append(data)
            reply += '{}. {}\n'.format(i, label)
        context.user_data['pilihan_lokasi'] = lokasi
        update.message.reply_text(reply)
        update.message.reply_text('Lokasi ditemukan, pilih lokasi anda')
        return SIMPAN_LOKASI
    except IndexError as e:
        print(e)
        update.message.reply_text('Lokasi tidak ditemukan, coba lagi')
        return CARI_LOKASI

def simpan_lokasi(update: Update, context: CallbackContext) -> int:
    data = context.user_data.get('pilihan_lokasi')
    pilihan_cuaca = context.user_data.get('pilihan_cuaca')
    try:
        text = int(update.message.text)
        if (text <= len(data) and text > 0):
            update.message.reply_text('Lokasi berhasil diatur')
            context.user_data['lokasi'] = data[text - 1]
            del context.user_data['pilihan_lokasi']

            if pilihan_cuaca == 'sekarang':
                cuaca_sekarang(update, context)
            else:
                cuaca_harian(update, context)
            return PILIHAN
        else:
            update.message.reply_text('Pilihan anda salah, coba lagi')
            return SIMPAN_LOKASI
    except ValueError as e:
        print(e)
        update.message.reply_text('Masukkan hanya angka')
        return SIMPAN_LOKASI

def query_cuaca(negara, kota, key, tab):
    url = "{}/{}/{}/{}/{}/{}".format(BASE_URL, negara, kota, key, tab, key)
    html = requests.get(url, headers=HEADERS)
    return html

def cuaca_sekarang(update: Update, context: CallbackContext) -> int:
    try:
        data = context.user_data.get('lokasi')
        key = data['key']
        negara = data['negara']
        kota = data['kota']
        result = query_cuaca(negara, kota, key, 'weather-forecast')
        soup = BeautifulSoup(result.text, 'lxml')
        dataCuaca = soup.find('a', {'class': 'cur-con-weather-card'})
        jam = dataCuaca.find('p').getText(strip=True)
        cuaca = dataCuaca.find('span', {'class': 'phrase'}).getText(strip=True)
        suhu = dataCuaca.find('div', {'class': 'temp'}).getText(strip=True)
        reply = 'Kondisi Cuaca sekarang di {} pukul {} :\n'.format(kota.replace('-', ' ').capitalize(), jam)
        reply += '-> Cuaca : {}\n' .format(cuaca)
        reply += '-> Suhu : {}\n' .format(suhu)
        for detail in dataCuaca.find('div', {'class': 'details-container'}).findAll('div', {'spaced-content'}):
            label = detail.find('span', {'class': 'label'}).getText(strip=True).lower().replace(' ', '-')
            value = detail.find('span', {'class': 'value'}).getText(strip=True)
            reply += '-> {} : {}\n' .format(label, value)
        update.message.reply_text(
            reply,
            reply_markup=ReplyKeyboardMarkup(KEYBOARD_PILIHAN),
        )
        return PILIHAN
    except Exception as e:
        print(e)
        update.message.reply_text(
            'Terjadi kesalahan, silahkan coba kembali atau hubungi admin',
            reply_markup=ReplyKeyboardMarkup(KEYBOARD_PILIHAN),
        )
        return PILIHAN

def cuaca_harian(update: Update, context: CallbackContext) -> int:
    try:
        data = context.user_data.get('lokasi')
        key = data['key']
        negara = data['negara']
        kota = data['kota']
        result = query_cuaca(negara, kota, key, 'daily-weather-forecast')
        soup = BeautifulSoup(result.text, 'lxml')
        dataCuaca = soup.findAll('div', {'class': 'content-module'})[1]
        tanggal = dataCuaca.p.text.replace('-', '\-')
        reply = 'Kondisi Cuaca harian *{}* pada {} :' .format(kota.replace('-', ' ').capitalize(), tanggal)
        for harian in dataCuaca.findAll('div', {'class': 'daily-wrapper'}):
            tanggal = harian.findAll('span', {'class': 'date'})
            suhu_tinggi = harian.find('span', {'class':'high'}).text
            suhu_rendah = harian.find('span', {'class':'low'}).text
            cuaca = harian.find('div', {'class': 'phrase'}).getText(strip=True)
            curah_hujan = harian.find('div', {'class': 'precip'}).getText(strip=True)
            reply += '\n\n*Cuaca pada {} {} : *'.format(tanggal[0].text, tanggal[1].text)
            reply += '\n  \-\> Cuaca : {}'.format(cuaca)
            reply += '\n  \-\> Suhu\(Tinggi/Rendah\) : {}{}'.format(suhu_tinggi, suhu_rendah)
            reply += '\n  \-\> Curah Hujan : {}'.format(curah_hujan)
        update.message.reply_text(
            reply,
            parse_mode='MarkdownV2',
            reply_markup=ReplyKeyboardMarkup(KEYBOARD_PILIHAN),
        )
        return PILIHAN
    except Exception as e:
        print(e)
        update.message.reply_text(
            'Terjadi kesalahan, silahkan coba kembali atau hubungi admin',
            reply_markup=ReplyKeyboardMarkup(KEYBOARD_PILIHAN),
        )
        return PILIHAN

def other(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text.lower()
    if user_input == 'keluar':
        end(update, context)
    else:
        update.message.reply_text("Maaf bot tidak mengerti maksud anda")
        return PILIHAN

def end(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        'Terima kasih telah menggunakan bot kami, sampai jumpa kembali.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            PILIHAN: [MessageHandler(Filters.regex(re.compile(r'^(cuaca sekarang|cuaca harian|tentang)$', re.IGNORECASE)), pilihan)],
            CARI_LOKASI: [MessageHandler(Filters.text, query_search)],
            SIMPAN_LOKASI: [MessageHandler(Filters.text, simpan_lokasi)],
            CUACA_SEKARANG: [MessageHandler(Filters.text, cuaca_sekarang)],
            CUACA_HARIAN: [MessageHandler(Filters.text, cuaca_harian)],
        },
        fallbacks=[MessageHandler(Filters.text, other)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=BOT_TOKEN)
    updater.bot.setWebhook('https://forcast-cuaca-bot.herokuapp.com/' + BOT_TOKEN)  


if __name__ == '__main__':
    main()