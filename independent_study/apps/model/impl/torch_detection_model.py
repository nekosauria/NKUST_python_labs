from pathlib import Path
from typing import List

import torch
import torchvision
from PIL.Image import Image

from apps.const.image_const import ImageConst
from apps.dto.detection_result import DetectionResult
from apps.model.interface.base_detection_model import BaseDetectionModel


class TorchDetectionModel(BaseDetectionModel):
    def __init__(self, model_path: Path, score_threshold: float = 0.5):
        self._model_path = model_path
        self._model = None
        self._score_threshold = score_threshold
        self._labels = ImageConst.TORCH_LABELS

    @property
    def model_path(self) -> Path:
        return self._model_path

    @property
    def name(self) -> str:
        return "torchvision.models.detection.maskrcnn_resnet50_fpn"

    @property
    def labels(self) -> List[str]:
        return self._labels

    def load(self, model_path: Path) -> None:
        print(f"loading model from {model_path}")
        raw = torch.load(model_path, weights_only=False)
        print(type(raw))  # 看這裡
        self._model = raw
        self._model.eval()

    def predict(self, image: Image) -> DetectionResult:
        if self._model is None:
            raise RuntimeError("模型尚未載入，請先呼叫 load()")

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

        output = self._model([image_tensor])[0]
        boxes, labels, scores = [], [], []
        seen = set()

        for box, label, score in zip(output["boxes"], output["labels"], output["scores"]):
            label_str = self._labels[int(label)]
            if label_str not in seen:
                seen.add(label_str)
                boxes.append((int(box[0]), int(box[1]), int(box[2]), int(box[3])))
                labels.append(int(label))
                scores.append(round(float(score), 4))

        return DetectionResult(boxes=boxes, labels=labels, scores=scores)