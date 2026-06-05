import hashlib
from pathlib import Path

import torch
import torchvision
from PIL import Image
from flask import current_app
from apps.const.image_const import ImageConst
import numpy as np

from apps.util.image_draw import make_color, make_line, draw_lines, draw_texts


def make_detect_image(file):
    """
    接收前端上傳的檔案物件，儲存原始圖片後執行物件偵測，
    並將偵測結果（框線 + 標籤）繪製後存檔。

    Args:
        file: 前端上傳的檔案物件（需支援 .read() 與 .filename）

    Returns:
        tuple: (tags, tag_scores, detect_img)
            - tags (list[str]): 本次偵測到的物件標籤清單（去重複）
            - tag_scores (dict): 各標籤對應的信心分數
            - ora_img (str): 原圖片的網址
            - detect_img (str): 偵測結果圖片的網址
    """

    data = file.read()
    md5 = hashlib.md5(data).hexdigest()

    input_path  = ImageConst.UPLOAD_FOLDER / f"{md5}_{file.filename}"
    output_path = ImageConst.RESULT_FOLDER / f"{md5}_{file.filename}"

    # 寫入原圖
    input_path.write_bytes(data)
    ora_img = f"{ImageConst.WEB_BASE_URL}/{ImageConst.UPLOAD_FOLDER}/{input_path.name}"

    labels = ImageConst.LABELS
    image = Image.open(input_path)

    image_tensor = torchvision.transforms.functional.to_tensor(image)
    """
    將 PIL Image 轉成 PyTorch 張量
    PyTorch Tensor (以此例來說)
    shape = [C,H,W]
    dtype = float32

    value = 0~1
    R = 255 / 255 = 1.0
    G = 128 / 255 ≈ 0.502
    B = 64 / 255 ≈ 0.251

    """

    """
    以 4 pixel 圖為例

    [R, G, B]
    紅色 = [255, 0, 0]
    綠色 = [0, 255, 0]
    藍色 = [0, 0, 255]
    白色 = [255, 255, 255]


    像素值（HWC 格式）： [
        [[255, 0, 0], [0, 255, 0]],
        [[0, 0, 255], [255, 255, 255]]
    ]
    等同於 tensor（CHW 格式) ： ([
        [
            [1.0, 0.0],
            [0.0, 1.0]
        ],

        [
            [0.0, 1.0],
            [0.0, 1.0]
        ],

        [
            [0.0, 0.0],
            [1.0, 1.0]
        ]
    ])
    
    CHW = Channel × Height × Width
    C = Channel（顏色通道，RGB 就是 3）
    H = Height（圖片高度，幾個像素）
    W = Width（圖片寬度，幾個像素）
    """

    model_path = Path(current_app.root_path) / "model" / "model.pt"
    model = torch.load(model_path, weights_only=False)
    model = model.eval()

    # 執行推論，取第一張圖片的結果（回傳格式：list of dict）
    output = model([image_tensor])[0]

    tags = []  # 紀錄已標記過的標籤，避免重複
    tag_scores = {}  # 紀錄每個標籤對應的信心分數
    result_image = np.array(image.copy())  # 複製原圖作為繪圖畫布（RGB numpy array）

    # 【條件】信心分數需超過 0.5，且同一標籤不重複標記
    for box, label, score in zip(output["boxes"], output["labels"], output["scores"]):
        if score > 0.5 and labels[label] not in tags:
            print(f"score: {score:.4f}, label: {labels[label]}")

            # 產生框線顏色（BGR or RGB tuple）
            color = make_color(labels)

            # 計算適合圖片尺寸的框線粗細
            line = make_line(result_image)

            # 將 box tensor 轉為左上角 (c1) 與右下角 (c2) 的像素座標
            c1 = (int(box[0]), int(box[1]))  # (x_min, y_min)
            c2 = (int(box[2]), int(box[3]))  # (x_max, y_max)

            # 在 result_image 上繪製偵測框
            cv2 = draw_lines(c1, c2, result_image, line, color)

            # 在偵測框旁繪製文字標籤
            cv2 = draw_texts(result_image, line, c1, cv2, color, labels, label)

            # 記錄已處理的標籤與對應信心分數
            tags.append(labels[label])
            tag_scores[labels[label]] = round(float(score), 4)

    # 直接對 result_image 原地修改，最後用 cv2 模組存檔
    # 將 RGB 轉回 BGR（OpenCV 預設色彩空間），再寫入輸出路徑
    cv2.imwrite(str(output_path), cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR))
    detect_img = f"{ImageConst.WEB_BASE_URL}/{ImageConst.RESULT_FOLDER}/{output_path.name}"

    print(tags, tag_scores, ora_img, detect_img)

    return tags, tag_scores, ora_img, detect_img