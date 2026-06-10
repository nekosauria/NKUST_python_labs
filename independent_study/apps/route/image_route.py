import json
import time
from flask import Blueprint, request, jsonify, app

from apps.const.image_const import allowed_file, ImageConst
from apps.service.detection_service import DetectionService
from apps.model.factory.detection_model_factory import DetectionModelFactory

image_bp = Blueprint("image", __name__)
@image_bp.route('/upload', methods=["GET", "POST"])
def upload():
    # 紀錄 Cost time
    t0 = time.time()

    if "image" not in request.files:
        return jsonify({"error": "no image field in form-data"}), 400

    # get parameter
    file = request.files["image"]
    model_type = request.form.get("model", ImageConst.MODEL_YOLO)  # 預設 yolo

    if file.filename == "":
        return jsonify({"error": "empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "file type not allowed"}), 400

    try:
        # === 直接從全域單例工廠取得常駐記憶體的模型 ===
        try:
            model = DetectionModelFactory.get_model(model_type)
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400

        # === 開始跑預測 ===
        svc = DetectionService(model=model)
        tag_results, predict_list, ora_img, detect_img = svc.make_detect_image(file, model_type)

        cost = round(time.time() - t0, 3)
        print(f"\n[{model.__class__.__name__}] make_detect_image cost: {cost}s")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    data = {
        "model": model_type,
        "cost_sec": cost,
        "tag_results": tag_results,
        "predict_list": predict_list,
        "ora_img": ora_img,
        "detect_img": detect_img
    }

    # 建立 jsonify Response（給前端使用）
    result = jsonify(data)

    # === 加上 No-Cache Headers，防止 Nginx、瀏覽器或 Cloudflare 快取 AI 辨識後的圖片結果 ===
    result.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
    result.headers['Pragma'] = 'no-cache'
    result.headers['Expires'] = '0'

    # === 印出漂亮的 JSON 字串（方便 debug）===
    print("=== API Response JSON ===")
    print(json.dumps(data, ensure_ascii=False, indent=4))

    return result, 200
