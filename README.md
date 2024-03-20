Repositori ini berisikan implementasi penggunaan API yang diintegrasikan dengan bot telegram menggunakan library <a href="https://github.com/eternnoir/pyTelegramBotAPI">pyTelegramBotAPI</a>, diharapkan dengan adanya pembuatan bot ini dapat membantu sebagian orang.

## File description

- requirements.txt berisikan nama dari library yang telah diinstal pada laptop penulis source-code.
- waktusholat.py berfungsi sebagai module yang dipanggil guna memproses data dari lokasi yang dikirim oleh user.

## Installation

- Pastikan terlebih dahulu bahwa PC/Laptop Anda terhubung dengan internet dan telah terinstall python.
- Unduh file zip atau gunakanlah git clone.
  ```<language>
  git clone https://github.com/Ray123fa/bot-telegram-python.git
  ```
- Buka file config.example.py lalu rename menjadi config.py. Kemudian:
  - Ganti <b><<BOT_APIKEY>></b> dengan APIKEY yang diberikan botfather saat pembuatan bot.
  - Ganti <b><<BINDERBYTE_APIKEY>></b> dengan APIKEY yang diberikan binderbyte setelah pembuatan akun.
- Buka terminal dan arahkan ke penyimpanan folder.
- Ketik pip install -r requirements.txt untuk menginstall library yang digunakan penulis source-code.
  ```<language>
  pip install -r requirements.txt
  ```
- Ketik python bot.py untuk memulai program.
  ```<language>
  python bot.py
  ```
- Start bot telegram.
- Untuk menonaktifkan program, cukup tekan Ctrl+C.

## Big thanks to

- https://github.com/eternnoir/pyTelegramBotAPI
- https://pypi.org
- https://stackoverflow.com
- https://aladhan.com/
- https://binderbyte.co

Bila terdapat kesalahan maupun error, silakan ajukan melalui issues.