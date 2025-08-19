from flask import Flask, jsonify, render_template, send_from_directory
import json, os, time, shutil

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("home.html")  # templates/home.html aranır

@app.get("/health")
def health():
    return jsonify({"status": "ok"})  # JSON key'leri küçük harf yaygın

@app.get("/lastest/info")  
def info():
    path = os.path.join(os.path.dirname(__file__), "lastest_info.json")
    if not os.path.exists(path):
        return jsonify({"error": "no data"}), 404
    with open(path, "r", encoding="utf-8") as f:
        context = json.load(f)
    return jsonify(context), 200

@app.get("/lastest/30/photos")
def photos():
    source_dir = "Images/frames"  # Kaynak klasör
    snapshot_name = time.strftime("%Y%m%d_%H%M%S")  # Zaman damgası
    dest_dir = os.path.join("snapshots", snapshot_name)  # Hedef klasör

    # Hedef klasörü oluştur
    os.makedirs(dest_dir, exist_ok=True)

    # Kaynak klasördeki .jpg dosyalarını al
    files = sorted(f for f in os.listdir(source_dir) if f.endswith(".jpg"))

    # Dosyaları kopyala
    for f in files:
        shutil.copy(os.path.join(source_dir, f), dest_dir)

    urls = [f"/snapshots/{snapshot_name}/{f}" for f in files]


    return render_template("photos.html", urls=urls)
    
@app.get('/snapshots/<path:filename>')
def serve_snapshot(filename):
    return send_from_directory('snapshots', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
