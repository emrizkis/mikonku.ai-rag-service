# Gunakan image dasar Debian-based Python yang stabil dan ringan
FROM python:3.11-slim

# Atur environment untuk Python agar log langsung tercetak ke terminal
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set direktori kerja di dalam container
WORKDIR /app

# (Opsional) Install library sistem dasar jika `pypdf` atau `sentence-transformers` membutuhkannya
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Salin hanya requirements.txt terlebih dahulu (demi caching layer Docker yang lebih baik)
COPY requirements.txt .

# Install dependencies Python (versi CPU-only secara otomatis ditarik dari index-url yang kita set)
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode sumber ke dalam direktori kerja container
COPY . .

# Secara default, container akan menampilkan panduan argumen main.py
CMD ["python", "main.py", "--help"]
