"""
GBN — Gunpla Battle Nexus Online
=================================
Backend xác thực mã bí mật cho hệ thống Gundam.

Cách thêm Gundam mới:
    1. Thêm một entry vào GUNDAM_DATABASE bên dưới.
    2. Key của dict là MÃ BÍ MẬT người dùng sẽ nhập (viết hoa, không dấu cách).
    3. Không cần sửa gì trong route — mọi thứ đọc thẳng từ database.
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# ============================================================
# DATABASE — Danh sách Gundam / Gunpla trong hệ thống GBN
# ============================================================
# Mỗi entry:
#   id           -> mã hiển thị (VD: "001")
#   name         -> tên Gundam
#   video_url    -> link video trận chiến (YouTube)
#   description  -> mô tả ngắn hiển thị trên terminal
GUNDAM_DATABASE = {
    "0001": {
        "id": "001",
        "name": "RX-78-2 Gundam",
        "video_url": "https://www.youtube.com/watch?v=T0x5YcPIdO8",
        "description": "Biểu tượng huyền thoại của kỷ nguyên vũ trụ, sở hữu độ cơ động cao và khả năng chiến đấu toàn diện.",
    },
    "0298": {
        "id": "002",
        "name": "Sazabi",
        "video_url": "https://www.youtube.com/watch?v=Gc5BBt5wShc",
        "description": "Cỗ máy chỉ huy của Char Aznable, mang sức mạnh áp đảo và khí chất của một huyền thoại phản diện.",
    },
    "1983": {
        "id": "003",
        "name": "ZAKU II",
        "video_url": "https://www.youtube.com/watch?v=d4ZeAa3a_Rw",
        "description": "Zaku II — những người lính bị cuốn vào chiến tranh ngoài ý muốn, biểu tượng của lực lượng Zeon.",
    },
}


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def index():
    """Trang chủ — terminal đăng nhập GBN."""
    return render_template("index.html")


@app.route("/api/verify-code", methods=["POST"])
def verify_code():
    """Xác thực mã bí mật và trả về dữ liệu Gundam tương ứng."""
    data = request.get_json(silent=True) or {}
    code = data.get("code", "").strip().upper()

    if not code:
        return jsonify({
            "status": "error",
            "message": "Vui lòng nhập mã truy cập.",
        }), 400

    gundam = GUNDAM_DATABASE.get(code)

    if gundam is None:
        return jsonify({
            "status": "error",
            "message": "Mã truy cập không tồn tại hoặc sai mã bảo mật!",
        }), 404

    return jsonify({
        "status": "success",
        "message": f"Xác thực thành công {gundam['name']}!",
        "data": gundam,
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
