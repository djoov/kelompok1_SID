# Evidence: Praktikum Blue-Green Deployment & Rollback

Screenshot terminal dari percobaan Kelompok 1 (Windows 11, Python 3.14, perintah `py -3`). Terminal A menjalankan server; Terminal B menjalankan perintah kontrol dan validasi secara berurutan pada sesi server yang sama. Gambar yang sama juga dilampirkan pada [laporan praktikum](../Laporan_Praktikum_Blue_Green_Kelompok1.pdf).

| No | Langkah | Yang dibuktikan | Screenshot |
| :---: | :--- | :--- | :--- |
| 1 | Server berjalan | Blue `:8101`, green `:8102`, dan router public `:8100` aktif | [01-server-berjalan.png](./01-server-berjalan.png) |
| 2 | Langkah 0–2 | Versi Python, kendala `prepare` (zlib-ng), baseline, dan validasi kandidat green | [02-langkah-0-2-baseline-dan-kandidat.png](./02-langkah-0-2-baseline-dan-kandidat.png) |
| 3 | Langkah 3 | Fault pada kandidat: gate green FAIL, `switch green --approve` tetap ditolak, public tetap di blue | [03-langkah-3-kandidat-gagal-switch-ditolak.png](./03-langkah-3-kandidat-gagal-switch-ditolak.png) |
| 4 | Langkah 4 | Switch tanpa approval ditolak; promosi ke green berhasil dengan checksum artifact yang sama; 0/10 kegagalan | [04-langkah-4-promosi-ke-green.png](./04-langkah-4-promosi-ke-green.png) |
| 5 | Langkah 5 | Gangguan pasca-promosi: `/health` tetap 200, tetapi 3/10 biaya salah dan gate public FAIL | [05-langkah-5-gangguan-pasca-promosi.png](./05-langkah-5-gangguan-pasca-promosi.png) |
| 6 | Langkah 6 | Rollback ke blue: 0/10 kegagalan; green tetap FAIL sampai `fault off`, lalu PASS | [06-langkah-6-rollback-ke-blue.png](./06-langkah-6-rollback-ke-blue.png) |
