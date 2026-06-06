# Booking Studio Musik

## Deskripsi Singkat Aplikasi

Booking Studio Musik merupakan aplikasi berbasis web yang digunakan untuk melakukan reservasi studio musik secara online. Melalui aplikasi ini, pengguna dapat memilih studio yang tersedia, menentukan jadwal penggunaan, memilih metode pembayaran, serta melihat daftar booking yang tersimpan pada sistem.

Selain itu, aplikasi dapat menghitung total biaya sewa secara otomatis berdasarkan durasi penggunaan dan harga studio yang dipilih. Data booking yang telah dibuat akan disimpan ke dalam database sehingga dapat ditampilkan kembali pada halaman aplikasi.

---

## Arsitektur Sistem Berbasis 3 VM

Sistem dijalankan menggunakan tiga Virtual Machine (VM) yang saling terhubung melalui jaringan private.

```text
                    HOST MACHINE
                         |
        -----------------+-----------------
        |                |                |
   VM Database      VM Backend       VM Frontend
 192.168.56.11    192.168.56.10    192.168.56.12
     MySQL             Flask            Nginx
    Port 3306        Port 5000         Port 80
```

Alur kerja sistem:

1. Pengguna mengakses aplikasi melalui browser pada VM Frontend.
2. Frontend mengirim request ke Backend API.
3. Backend memproses data dan berkomunikasi dengan Database.
4. Database menyimpan atau mengirimkan data sesuai permintaan.
5. Hasil dikembalikan ke Frontend untuk ditampilkan kepada pengguna.

---

## Pembagian Fungsi Virtual Machine

### 1. VM Database (192.168.56.11)

VM Database digunakan untuk menyimpan seluruh data booking studio musik menggunakan MySQL.

Fungsi utama:

* Menyimpan data reservasi studio.
* Menyimpan informasi pelanggan.
* Menyimpan data pembayaran dan status booking.
* Menyediakan data yang dibutuhkan oleh backend.

---

### 2. VM Backend (192.168.56.10)

VM Backend menjalankan aplikasi berbasis Python Flask yang berfungsi sebagai REST API.

Fungsi utama:

* Menerima request dari frontend.
* Memproses data booking.
* Menghubungkan frontend dengan database.
* Menyediakan endpoint API untuk operasi data booking.

Endpoint yang digunakan:

| Method | Endpoint          | Fungsi                         |
| ------ | ----------------- | ------------------------------ |
| GET    | /api/booking      | Mengambil seluruh data booking |
| POST   | /api/booking      | Menambahkan booking baru       |
| DELETE | /api/booking/{id} | Menghapus booking              |

---

### 3. VM Frontend (192.168.56.12)

VM Frontend digunakan untuk menampilkan antarmuka aplikasi kepada pengguna.

Fungsi utama:

* Menampilkan daftar studio dan harga.
* Menyediakan form booking studio.
* Menampilkan total pendapatan studio.
* Menampilkan daftar booking yang tersimpan.
* Mengirim dan menerima data melalui API Backend.

Frontend dibangun menggunakan HTML, CSS, JavaScript, dan Bootstrap serta dijalankan menggunakan Nginx.

---

## Tools dan Teknologi yang Digunakan

| Komponen       | Teknologi             |
| -------------- | --------------------- |
| Virtualisasi   | VirtualBox            |
| Manajemen VM   | Vagrant               |
| Provisioning   | Ansible               |
| Database       | MySQL                 |
| Backend        | Python Flask          |
| Frontend       | HTML, CSS, JavaScript |
| Framework CSS  | Bootstrap 5           |
| Web Server     | Nginx                 |
| Sistem Operasi | Ubuntu 22.04          |

---

## Cara Instalasi dan Menjalankan Aplikasi

### Prasyarat

Sebelum menjalankan aplikasi, pastikan perangkat telah terpasang:

* VirtualBox
* Vagrant
* Git

### Clone Repository

```bash
git clone <url-repository>
cd booking-studio-musik
```

### Menjalankan Virtual Machine

```bash
vagrant up
```

Perintah tersebut akan:

* Membuat seluruh Virtual Machine.
* Menjalankan proses provisioning menggunakan Ansible.
* Menginstal dan mengonfigurasi layanan pada setiap VM.

### Mengakses Aplikasi

Setelah seluruh VM berhasil dijalankan, aplikasi dapat diakses melalui browser:

```text
http://192.168.56.12
```

### Perintah Vagrant yang Sering Digunakan

Menjalankan VM:

```bash
vagrant up
```

Menghentikan VM:

```bash
vagrant halt
```

Menghapus VM:

```bash
vagrant destroy -f
```

Menjalankan ulang provisioning:

```bash
vagrant provision
```

Masuk ke VM Frontend:

```bash
vagrant ssh vm-frontend
```

Masuk ke VM Backend:

```bash
vagrant ssh vm-backend
```

Masuk ke VM Database:

```bash
vagrant ssh vm-database
```