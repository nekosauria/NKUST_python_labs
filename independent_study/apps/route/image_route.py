import json

from flask import Blueprint, request, jsonify, send_file
import hashlib
from apps.service.image_detect import make_detect_image
from apps.const.image_const import ImageConst, allowed_file

image_bp = Blueprint("image", __name__)
@image_bp.route('/upload', methods=["GET", "POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "no image field in form-data"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "file type not allowed"}), 400

    try:
        tags, tag_scores, ora_img, detect_img = make_detect_image(file)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    data = {
        "tags": tags,
        "scores": tag_scores,
        "ora_img": ora_img,
        "detect_img": detect_img
    }

    # 建立 jsonify Response（給前端使用）
    result = jsonify(data)

    # === 印出漂亮的 JSON 字串（方便 debug）===
    print("=== API Response JSON ===")
    print(json.dumps(data, ensure_ascii=False, indent=4))

    return result, 200

