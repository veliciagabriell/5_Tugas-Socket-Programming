<h1>5_TugasSocketProgramming</h1>

<h2>Kegeprek - Aplikasi CHat Sederhana Berbasis UDP</h2>

**Kegeprek Chat App** adalah sebuah aplikasi chat sederhada berbasis protokol UDP (User Datagram Protocol). Program Chat App ini untuk membantu antar client berkomunikasi lewat roomchat dengan real-time.
**Disusun oleh** : Catherine Alicia N (18223069) dan Velicia Christina Gabriel (18223085)
---
<h2>📝Deskripsi</h2>
Kegeprek Chat App adalah aplikasi room chat berbasisi protokol UDP (User Datagram Protocol) yang dirancang untuk ***client*** berkomunikasi dengan ***client*** lain secara real-time dalam satu ***chat room*** di jaringan yang sama. Karena menggunakan protokol UDP, aplikasi ini lebih berfokus pada kecepatan pengiriman pesan 

<h4>Tujuan Utama:</h4>
1. Menyediakan platform roomchat untuk client saling mengirim pesan secara ***real-time***
2. Mendalami konsep Transport Protocol, terutama UDP (User Datagram Protocol)
3. Mengaplikasikan materi perkuliahan secara langsung 
---
<h2>🔑Fitur Aplikasi</h2>
- **Autentifikasi Pengguna**:
  - Semua pengguna yang ingin mengakses roomchat harus masuk menggunakan password yang sudah tersedia
  - Semua pengguna yang sudah berhasil masuk menggunakan password, akan memasukkan username yang unik (Tidak boleh sama dengan client lain).
- **Pesan Real-Time**:
  - Pengiriman pesan secara langsung dan diterima secara tepat (tetapi jaringan harus dalam keadaan stabil)
- **Broadcast Pesan**:
  - Semua pesan yang dikirim akan diterima oleh semua pengguna yang terhubung
---
<h2>🗃️ Sturktur Proyek</h2> 
- `server.py` : File utama untuk menjalankan server UDP
- `client.py` : File untuk menjalankan client yang terhubung ke server. File untuk menampilkan GUI
---
<h2>⚒️Cara Kerja</h2> 
<h4>Server</h4>
1. Server berjalan di IP:Port default, yaitu `0.0.0.0:8083`
2. Jika pengguna sudah berhasil mengakses server, server akan mengirimkan pesan `"Nama diterima. Anda sudah bisa mengirim pesan."`
4. 
<h4>Client</h4>
1. Pengguna memasukkan alamat local host, local port, remote IP, remote port melalui antarmuka grafis `(tkinter)`.
2. Pengguna memasukkan password yang sudah ditentukan `(kegeprek)`.
3. Pengguna memasukkan username yang unik (Tidak boleh sama dengan klien lain). Klien akan mengirimkan permintaan ke server untuk mengecek keunikan username.
4. Jika username unik, maka server akan menerima permintaan login dan klien dapat mulai mengirim pesan.
5. Jika username tidak unik, maka server akan meminta client untuk mengirimkan username lain.
