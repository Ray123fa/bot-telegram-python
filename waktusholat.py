from translate import Translator
import requests as req, time, re

# Inisiasi request ke Web API
def init(lat, long):
	today = time.strftime("%d-%b-%Y", time.localtime())
	api = req.get(f"https://api.aladhan.com/v1/timings/{today}?latitude={lat}&longitude={long}&method=20")

	return api.json()

# Ganti format penanggalan hijriah
# Contoh 27-03-1445 menjadi 27 Rabiul Awal 1445
def hijrDate(date):
	num_months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
	name_months = ['Muharram', 'Safar', 'Rabiul Awal', 'Rabiul Akhir', 'Jumadil Awal', 'Jumadil Akhir', 'Rajab', "Sya'ban", 'Ramadhan', 'Syawal', 'Dzulkaidah', 'Dzulhijjah']

	tgl = date[:2]
	bln = date[3:5] # urutan bulan ke-
	thn = date[-4:]

	bln = bln.replace(num_months[int(bln)-1], name_months[int(bln)-1]) # nama bulan
	return f"{tgl} {bln} {thn}"

# Ganti format zona waktu
# Asia/Jakarta menjadi GMT+07.00 , dst.
def timezoneFormat(tz):
	arr_tz = ['Asia/Jakarta', 'Asia/Makassar', 'Asia/Jayapura']
	tz_replace = ['GMT+07.00 (WIB)', 'GMT+08.00 (WITA)', 'GMT+09.00 (WIT)']

	for i in range(3):
		if re.findall(arr_tz[i], tz):
			tz = tz.replace(arr_tz[i], tz_replace[i])
	return tz

def toDisplay(lat, long):
	apiRes = init(lat, long)

	# Penanggalan Masehi
	_dt = time.strftime("%A, %d %B %Y", time.localtime())
	grego_date = Translator(to_lang="id").translate(_dt)

	# Penanggalan Hijriah
	dt2 = apiRes['data']['date']['hijri']['date']
	hijr_date = hijrDate(dt2)

	# Waktu Sholat
	praytimes = [
		"Imsak: " + apiRes['data']['timings']['Imsak'],
		"Subuh: " + apiRes['data']['timings']['Fajr'],
		"Dzuhur: " + apiRes['data']['timings']['Dhuhr'],
		"Ashar: " + apiRes['data']['timings']['Asr'],
		"Maghrib: " + apiRes['data']['timings']['Maghrib'],
		"Isya: " + apiRes['data']['timings']['Isha']
	]

	# Zona Waktu
	tz = apiRes['data']['meta']['timezone']
	zonawaktu = timezoneFormat(tz)

	# Detail request API
	detail = {
		"date": grego_date + " | " + hijr_date,
		"latitude": lat,
		"longitude": long,
		"timezone": zonawaktu,
		"calculation": apiRes['data']['meta']['method']['name'],
		"juristic": "Syafi'i",
	}
	return praytimes, detail

def waktusholat(lat, long):
  praytimes, detail = toDisplay(lat, long)
  header = f"{detail['date']}\n{detail['timezone']}"
  footer = f"Koordinat: {str(detail['latitude'])}, {str(detail['longitude'])}\nMetode Kalkulasi: {detail['calculation']}\nMetode Juristik: Standar({detail['juristic']})"
  
  return header, praytimes, footer