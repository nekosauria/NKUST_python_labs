from flask import Flask, render_template
from apps.const.image_const import ImageConst
from flask_cors import CORS
from apps.route.image_route import image_bp
from apps.model.factory.detection_model_factory import DetectionModelFactory

app = Flask(__name__)
CORS(app)

# 註冊 blueprint (routes)
app.register_blueprint(image_bp)

@app.route("/")
def index():
    return render_template("index.html")

def init_stage():
    ImageConst.UPLOAD_FOLDER.mkdir(exist_ok=True)
    ImageConst.RESULT_FOLDER.mkdir(exist_ok=True)

    #在 App 啟動時就把模型餵進記憶體
    print(f"app.root_path: {app.root_path}")
    DetectionModelFactory.init_models(app.root_path)


if __name__ == "__main__":
    init_stage()
    app.run(debug=True, host=ImageConst.WEB_BASE_HOST, port=ImageConst.WEB_BASE_PORT)