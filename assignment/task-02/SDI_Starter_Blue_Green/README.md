# SDI Starter — Blue-green dan Rollback

1. Ekstrak ZIP. Buka dua terminal di folder yang memuat lab.py.
2. Python 3.10+; tidak membutuhkan pip/Docker/internet.
3. Terminal B: python lab.py prepare
4. Terminal A: python lab.py run (biarkan terbuka).
5. Terminal B: python lab.py check --target public
6. Ikuti panduan PRAKTIKUM.md, bagian langkah 2–6.

Windows: gunakan py -3; macOS/Linux: gunakan python3 jika python tidak tersedia.
Endpoint: http://127.0.0.1:8100/health
Stop: Ctrl+C di terminal A.

Satu proses dengan dua slot logis dan router. Ini simulasi pembelajaran, bukan server production.
Artifacts memuat kode biaya yang sama dengan kontrak pertemuan sebelumnya, ditambah currency pada 1.1.0.
Jangan menjalankan kode/ZIP asing melalui loader.
