# Studi Kasus: Monday Morning Go-Live

## 1. Apa tiga risiko terbesar?

Menurut kelompok kami, ada tiga risiko utama yang perlu diperhatikan sebelum sistem benar-benar *go-live*.

**Pertama, kesiapan server.** Server belum pernah dites, sementara sistem berpotensi digunakan hingga 5.000 pengguna. Ada kemungkinan sistem mengalami error, lambat, atau bahkan down ketika banyak pengguna mengaksesnya secara bersamaan.

**Kedua, risiko pada proses migrasi data.** Data lama yang akan dipindahkan ke sistem baru bisa saja mengalami masalah, seperti data hilang, tidak sesuai, atau tidak lengkap. Hal ini cukup berisiko karena berkaitan langsung dengan data yang akan digunakan pada sistem baru.

**Ketiga, kesiapan admin dalam menggunakan sistem.** Waktu training yang hanya tersedia selama dua jam membuat kemungkinan admin belum sepenuhnya memahami sistem. Jika terjadi masalah saat sistem sudah berjalan, admin mungkin belum siap untuk menangani atau merespons kendala tersebut.

---

## 2. Apa persyaratan minimum sebelum Go-Live?

Sebelum sistem *go-live*, menurut kelompok kami beberapa hal minimum harus dipastikan terlebih dahulu:

* Server sudah diuji dan berjalan dengan stabil.
* Data hasil migrasi sudah diperiksa dan sesuai dengan data sebelumnya.
* Fitur-fitur utama sistem sudah berhasil melalui proses testing.
* Admin sudah mendapatkan training dan memahami cara menggunakan sistem.
* Tersedia backup data.
* Terdapat rollback atau fallback plan jika sewaktu-waktu terjadi masalah setelah sistem di-*deploy*.

Selain itu, kondisi sistem setelah *go-live* juga perlu dapat dipantau agar masalah dapat diketahui lebih awal.

---

## 3. Bukti apa yang harus tersedia sebelum peluncuran?

Menurut kelompok kami, sebelum mengambil keputusan untuk *go-live*, harus ada beberapa bukti yang menunjukkan bahwa sistem memang sudah cukup siap.

Bukti tersebut antara lain:

* Hasil testing fitur utama sistem.
* Bukti bahwa data yang sudah dimigrasikan sesuai dan tidak ada data penting yang hilang.
* Hasil pengujian server untuk memastikan sistem mampu menangani jumlah pengguna yang diperkirakan.
* Bukti bahwa admin sudah mendapatkan training terkait penggunaan sistem.
* Backup data yang sudah disiapkan.
* Dokumentasi rollback plan jika deployment mengalami masalah.

Dengan adanya bukti tersebut, keputusan untuk melakukan *go-live* tidak hanya berdasarkan asumsi bahwa sistem sudah berjalan, tetapi berdasarkan hasil pengujian dan kesiapan yang sudah dapat dibuktikan.

---

## 4. Kapan kita memutuskan NO-GO?

Menurut kelompok kami, keputusan **NO-GO** sebaiknya diambil jika masih terdapat masalah yang sifatnya kritis dan dapat memberikan risiko besar ketika sistem digunakan.

Contohnya seperti server yang belum stabil, data hasil migrasi belum benar atau belum tervalidasi, fitur utama masih mengalami error, atau belum tersedia backup dan rollback plan.

Menurut kami, lebih baik menunda *go-live* daripada memaksakan sistem untuk berjalan sesuai jadwal tetapi ternyata belum siap dan justru menimbulkan masalah yang lebih besar. Karena pada akhirnya, *go-live* bukan hanya soal merilis sistem tepat waktu, tetapi memastikan bahwa risiko yang ada sudah cukup dapat diterima.
