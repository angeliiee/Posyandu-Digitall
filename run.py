"""
Entry point launcher untuk aplikasi Posyandu Digital.
Perintah utama untuk menjalankan aplikasi:
    streamlit run app.py
atau:
    python run.py
"""
import sys
import subprocess

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
