from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
CORS(app)

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")  # Boleh sama dengan sender

@app.route("/kirim-pesan", methods=["POST"])
def kirim_pesan():
    data = request.get_json()
    nama = data.get("nama", "")
    email = data.get("email", "")
    pekerjaan = data.get("pekerjaan", "")
    pesan = data.get("pesan", "")

    if not nama or not email or not pesan:
        return jsonify({"error": "Nama, email, dan pesan wajib diisi"}), 400

    isi_email = f"""
    Pesan dari halaman About Us:

    Nama: {nama}
    Email: {email}
    Pekerjaan: {pekerjaan}
    
    Pesan:
    {pesan}
    """

    try:
        msg = MIMEText(isi_email)
        msg["Subject"] = f"Pesan Baru dari {nama}"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"message": "Pesan berhasil dikirim!"})
    except Exception as e:
        return jsonify({"error": f"Gagal mengirim pesan: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

CORS(app, resources={r"/*": {"origins": "https://solusiai.free.nf"}})
