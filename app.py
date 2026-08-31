from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Cơ sở dữ liệu Gunpla / Gundam hệ thống GBN
GUNDAM_DATABASE = {
    "0001": {
        "id": "001",
        "name": "RX-78-2 Gundam",
        "video_url": "https://www.youtube.com/watch?v=T0x5YcPIdO8",
        "description": "Biểu tượng huyền thoại của kỷ nguyên vũ trụ, sở hữu độ cơ động cao và khả năng chiến đấu toàn diện."
    },
    "0002": {
        "id": "002",
        "name": "Freedom Gundam",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", # Có thể thay bằng link chiến đấu khác
        "description": "Mobile Suit cao cấp trang bị hệ thống lò phản ứng hạt nhân và dàn vũ khí Full Burst."
    },
    "0003": {
        "id": "003",
        "name": "Gundam Exia",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "description": "Chuyên gia cận chiến với hệ thống 7 thanh kiếm độc quyền của Celestial Being."
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/verify-code', methods=['POST'])
def verify_code():
    data = request.get_json()
    code = data.get('code', '').strip()

    if code in GUNDAM_DATABASE:
        gundam_info = GUNDAM_DATABASE[code]
        return jsonify({
            "status": "success",
            "message": f"Xác thực thành công {gundam_info['name']}!",
            "data": gundam_info
        }), 200
    else:
        return jsonify({
            "status": "error",
            "message": "Mã truy cập không tồn tại hoặc sai mã bảo mật!"
        }), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
