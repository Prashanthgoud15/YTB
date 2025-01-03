from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os


app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('videoUrl')
    format_choice = data.get('format')

    if not video_url:
        return jsonify({"error": "Please provide a valid YouTube link."}), 400

    try:
        command = f'yt-dlp -f {format_choice} -o "downloads/%(title)s.%(ext)s" "{video_url}"'
        subprocess.run(command, shell=True, check=True)
        return jsonify({"message": "Download successful!"})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

