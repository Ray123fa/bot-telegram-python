from telebot import TeleBot as bot, types
from waktusholat import waktusholat
from config import bot_key, binderbyte_key
import requests as req

apikey = bot_key
tb = bot(apikey)

@tb.message_handler(commands=["start"])
def send_welcome(message):
	respon = "Haloo, selamat datang\n\nUntuk mengetahui layanan apa saja yang disediakan pada bot ini, Anda dapat mengklik /help"
	tb.reply_to(message, respon)

@tb.message_handler(commands=["help"])
def send_help(message):
	respon = "Berikut adalah beberapa layanan yang dapat anda gunakan pada bot ini:\n\n/cekresi\n/waktusholat"
	tb.reply_to(message, respon)

@tb.message_handler(commands=["cekresi"])
def send_msg(message):
	pihak = ["jne", "pos", "jnt", "sicepat", "tiki", "anteraja", "spx"]
	text = message.text
	if text == "/cekresi":
		respon = "<b>Pada layanan ini anda dapat melacak paket yang diproses atau diantar menggunakan pihak berikut:</b>\njne - JNE Express\npos - POS Indonesia\njnt - J&T Express Indonesia\nsicepat - SiCepat\ntiki - TIKI\nanteraja - AnterAja\nspx - Shopee Express\n\nContoh:\n/cekresi anteraja [nomer resi]\n/cekresi anteraja 10006134347351\n\n<b>Disclaimer: Layanan ini hanya menampilkan progress paket terakhir</b>"
		tb.reply_to(message, respon, parse_mode="HTML")

	txt = text.split(" ")
	if len(txt) == 3 and txt[0] == "/cekresi" and txt[1] in pihak:
		pihak = txt[1]
		awb = txt[2]

		binderbyte_apikey = binderbyte_key
		result = req.get(
			f"https://api.binderbyte.com/v1/track?api_key={binderbyte_apikey}&courier={pihak}&awb={awb}").json()
  
		if result["status"] == 200:
			pengirim = result["data"]["detail"]["shipper"]
			penerima = result["data"]["detail"]["receiver"]
			tgl = result["data"]["history"][0]["date"]
			desc = result["data"]["history"][0]["desc"]

			respon = f"<b>Pengirim: {pengirim}\nPenerima: {penerima}</b>\n\nTanggal: {tgl}\nDeskripsi: {desc}"
			tb.reply_to(message, respon, parse_mode="HTML")
		else:
			respon = f"Kode resi {awb} tidak ditemukan pada pihak {pihak}"
			tb.reply_to(message, respon)
	elif txt[1] not in pihak:
		respon = f"Pihak {txt[1]} tidak terdaftar dalam layanan ini"
		tb.reply_to(message, respon)

@tb.message_handler(commands=["waktusholat"])
def send_msg(message):
	markup = types.ForceReply(selective=False)
	respon = "Silakan kirim lokasi anda dengan mereply pesan ini untuk mengetahui waktu sholat."
	tb.reply_to(message, respon, reply_markup=markup)

@tb.message_handler(content_types=["location"])
def send_msg(message):
	msg_id = message.message_id
	replymsg_id = message.reply_to_message.message_id
	
	# Inisiasi agar bot hanya merespon terhadap lokasi yang dikirimkan setelah bot mengirimkan perintah
	if msg_id == replymsg_id+1:
		lat = message.location.latitude
		long = message.location.longitude
		data = waktusholat(lat, long)

		# data[0] is a header of the text will be send to telegram
		# data[1] is an array of pray times
		# data[2] is a footer of the text will be send to telegram
		# See waktusholat.py for more details

		respon = f'{data[0]}\n\n{data[1][0]}\n{data[1][1]}\n{data[1][2]}\n{data[1][3]}\n{data[1][4]}\n{data[1][5]}\n\n{data[2]}'
		tb.reply_to(message, respon)
	else:
		respon = "<b>Maaf, waktu respon anda terlalu lama. Silahkan coba sekali lagi!</b>"
		tb.reply_to(message, respon, parse_mode="HTML")

print("Bot sedang berjalan")
tb.infinity_polling()