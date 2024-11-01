# 5_TugasSocketProgramming

## Kegeprek - Aplikasi Chat Sederhana Berbasis UDP

**Kegeprek Chat App** adalah sebuah aplikasi chat sederhana berbasis protokol UDP (User Datagram Protocol). Program ini membantu antar client berkomunikasi melalui room chat secara real-time.

**Disusun oleh**: Catherine Alicia N (18223069) dan Velicia Christina Gabriel (18223085)

## 📝 Deskripsi
Kegeprek Chat App adalah aplikasi room chat berbasis protokol UDP (User Datagram Protocol) yang dirancang untuk klien berkomunikasi dengan klien lain secara real-time dalam satu _chat room_ di jaringan yang sama. Karena menggunakan protokol UDP, aplikasi ini lebih berfokus pada kecepatan pengiriman pesan.

### Tujuan Utama:
1. Menyediakan platform room chat untuk client saling mengirim pesan secara _real-time_.
2. Mendalami konsep Transport Protocol, terutama UDP (User Datagram Protocol).
3. Mengaplikasikan materi perkuliahan secara langsung.

## 🔑 Fitur Aplikasi

- **Autentifikasi Pengguna**:  
  Semua pengguna yang ingin mengakses room chat harus masuk menggunakan password yang sudah tersedia. Setiap pengguna yang berhasil masuk harus menggunakan username yang unik (tidak boleh sama dengan client lain).

- **Pesan Real-Time**:  
  Pengiriman pesan dilakukan secara langsung dan diterima secara tepat (dengan catatan jaringan dalam keadaan stabil).

- **Broadcast Pesan**:  
  Semua pesan yang dikirim akan diterima oleh semua pengguna yang terhubung.

## 🗃️ Struktur Proyek 

- `server.py`: File utama untuk menjalankan server UDP.
- `client.py`: File untuk menjalankan client yang terhubung ke server, dengan antarmuka GUI menggunakan `tkinter`.

## ⚒️ Cara Kerja

### Server
1. Server berjalan di IP dan Port default, yaitu `0.0.0.0:8083`.
2. Server memverifikasi keunikan nama; jika unik, pengguna dapat mengakses server.
3. Jika login berhasil, server akan mengirimkan pesan: `"Nama diterima. Anda sudah bisa mengirim pesan."`
4. Server menyimpan alamat klien dan memungkinkan klien untuk mengirim dan menerima pesan dari klien lain.
5. Setiap pesan dari klien akan diteruskan ke semua klien lainnya yang terhubung ke server.

### Client
1. Pengguna memasukkan alamat lokal host, lokal port, remote IP, dan remote port melalui antarmuka grafis `(tkinter)`.
2. Pengguna memasukkan password yang sudah ditentukan `(kegeprek)`.
3. Pengguna memasukkan username yang unik (tidak boleh sama dengan klien lain). Klien akan mengirimkan permintaan ke server untuk mengecek keunikan username.
4. Jika username unik, maka server akan menerima permintaan login, dan klien dapat mulai mengirim pesan.
5. Jika username tidak unik, maka server akan meminta klien untuk mengirimkan username lain.

## 👩‍💻 Cara Menjalankan

### Syarat
- Python 3.x harus sudah terpasang pada komputer.
- Komputer klien dan komputer server berada di dalam satu jaringan yang sama.

### Menjalankan Server
1. Clone repositori ini dan buka direktori proyek.
2. Buka folder yang berisi file `server.py` dan `client.py`, lalu buka di terminal.
3. Jalankan `server.py` dengan perintah:
   ```bash
   python server.py
4. Server akan jalan di port dan IP yang sudah ditentukan

### Menjalankan Client
1. Clone repositori ini dan buka direktori proyek.
2. Buka folder yang berisi file `server.py` dan `client.py`, lalu buka di terminal.
3. Jalankan `client.py` dengan perintah:
   ```bash
   python client.py
4. Masukkan lokal IP, lokal port, remote IP, dan remote port
5. Masukkan password dan username
6. Jika login berhasil, akan muncul tampilan roomchat dan anda bisa mengirim dan menerima pesan dari pengguna lain.

