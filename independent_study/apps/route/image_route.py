import json
import time
from pathlib import Path
from flask import current_app
from flask import Blueprint, request, jsonify, app

from apps.const.image_const import allowed_file, ImageConst
from apps.model.impl.torch_detection_model import TorchDetectionModel
from apps.model.impl.yolo_detection_model import YoloDetectionModel
from apps.service.detection_service import DetectionService

image_bp = Blueprint("image", __name__)
@image_bp.route('/upload', methods=["GET", "POST"])
def upload():
    if "image" not in request.files:
        return jsonify({"error": "no image field in form-data"}), 400

    # get parameter
    file = request.files["image"]
    model_type = request.form.get("model", "yolo")  # 預設 yolo

    if file.filename == "":
        return jsonify({"error": "empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "file type not allowed"}), 400

    try:
        print(f"current_app.root_path:{current_app.root_path}")

        match model_type:
            case "torch":
                model = TorchDetectionModel(
                    model_path=Path(current_app.root_path) / "model" / "maskrcnn_model.pt",
                    score_threshold=ImageConst.SCORE_THRESHOLD
                )
            case "yolo":
                model = YoloDetectionModel(
                    model_path=Path(current_app.root_path) / "model" / "yolo11n.pt",
                    score_threshold=ImageConst.SCORE_THRESHOLD
                )
            case _:
                return jsonify({"error": f"unknown model type: {model_type}"}), 400

        svc = DetectionService(model=model)

        t0 = time.time()
        tags, tag_scores, ora_img, detect_img = svc.make_detect_image(file)
        cost = round(time.time() - t0, 3)
        print(f"\n[{model.__class__.__name__}] make_detect_image cost: {cost}s")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    data = {
        "model": model_type,
        "cost_sec": cost,
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

