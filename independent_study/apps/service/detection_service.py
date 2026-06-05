import hashlib

import cv2
import numpy as np
from PIL import Image

from apps.const.image_const import ImageConst
from apps.model.interface.base_detection_model import BaseDetectionModel
from apps.util.image_draw import get_color_by_label, make_line, draw_lines, draw_texts


class DetectionService:

    def __init__(self, model: BaseDetectionModel):
        self._model = model
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if not self._loaded:
            self._model.load(self._model.model_path)
            self._loaded = True

    def make_detect_image(self, file) -> tuple[dict, str, str]:
        """
        接收前端上傳的檔案物件，儲存原始圖片後執行物件偵測，
        並將偵測結果（框線 + 標籤）繪製後存檔。

        Args:
            file: 前端上傳的檔案物件（需支援 .read() 與 .filename）

        Returns:
                - tag_scores (dict): 各標籤對應的信心分數
                - ora_img (str): 原圖片的網址
                - detect_img (str): 偵測結果圖片的網址
        """

        # add md5 key
        data = file.read()
        md5 = hashlib.md5(data).hexdigest()
        input_path  = ImageConst.UPLOAD_FOLDER / f"{md5}_{file.filename}"
        output_path = ImageConst.RESULT_FOLDER / f"{md5}_{file.filename}"

        # 寫入原圖
        input_path.write_bytes(data)
        ora_img = f"{ImageConst.WEB_BASE_URL}/{ImageConst.UPLOAD_FOLDER}/{input_path.name}"

        # init var
        labels = self._model.labels
        print(f"labels: {labels}")

        image = Image.open(input_path)
        tags = []
        tag_scores = {}  # 紀錄每個標籤對應的信心分數
        result_image = np.array(image.copy())  # 複製原圖作為繪圖畫布（RGB numpy array）

        # -----------------------------------------------------------
        # 執行推論，取第一張圖片的結果（回傳格式：list of dict）
        self._ensure_loaded()
        output = self._model.predict(image)  # ← 統一介面，與模型實作無關
        # -----------------------------------------------------------

        # 開始畫框線
        # 【條件】信心分數需超過預測值就標記，且同一標籤不重複標記
        for box, label_idx, score in zip(output.boxes, output.labels, output.scores):
            if score > ImageConst.SCORE_THRESHOLD and labels[label_idx] not in tags:
                print(f"score: {score:.4f}, label: {labels[label_idx]}")

                # 產生框線顏色（BGR or RGB tuple）
                color = get_color_by_label(label_idx)

                # 計算適合圖片尺寸的框線粗細
                line = make_line(result_image)

                # 將 box tensor 轉為左上角 (c1) 與右下角 (c2) 的像素座標
                c1 = (int(box[0]), int(box[1]))  # (x_min, y_min)
                c2 = (int(box[2]), int(box[3]))  # (x_max, y_max)

                # 在 result_image 上繪製偵測框
                result_image = draw_lines(c1, c2, result_image, line, color)

                # 在偵測框旁繪製文字標籤
                result_image = draw_texts(result_image, line, c1, color, labels, label_idx)

                # 記錄已處理的標籤與對應信心分數
                tags.append(label_idx)
                tag_scores[labels[label_idx]] = round(float(score), 4)

        # ✅ imwrite 前確認 result_image 是合法的 numpy array
        if result_image is None or not isinstance(result_image, np.ndarray) or result_image.size == 0:
            raise ValueError("result_image 不合法，無法寫入檔案")

        # 直接對 result_image 原地修改，最後用 cv2 模組存檔
        # 將 RGB 轉回 BGR（OpenCV 預設色彩空間），再寫入輸出路徑
        cv2.imwrite(str(output_path), cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))

        # return data
        detect_img = f"{ImageConst.WEB_BASE_URL}/{ImageConst.RESULT_FOLDER}/{output_path.name}"
        print(tag_scores, ora_img, detect_img)

        return tag_scores, ora_img, detect_img