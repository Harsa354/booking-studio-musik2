CREATE DATABASE IF NOT EXISTS db_studio;

USE db_studio;

CREATE TABLE IF NOT EXISTS booking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_studio VARCHAR(100),
    tanggal DATE,
    jam_mulai TIME,
    jam_selesai TIME,
    nama_pemesan VARCHAR(100),
    no_hp VARCHAR(20),
    metode_bayar ENUM('tunai','transfer','qris') DEFAULT 'tunai',
    harga DECIMAL(15,2),
    status ENUM('pending','konfirmasi','batal') DEFAULT 'pending'
);