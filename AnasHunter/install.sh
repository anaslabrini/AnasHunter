#!/bin/bash

echo "[+] Installing required packages..."
sudo apt update
sudo apt install -y python3 python3-pip

# تثبيت المكتبات المطلوبة
pip install -r requirements.txt

# نسخ السكريبت إلى المسار المناسب
echo "[+] Installing AnasHunter..."
sudo cp anashunter /usr/local/bin/anashunter
sudo chmod +x /usr/local/bin/anashunter

echo "[✓] Installation complete!"
