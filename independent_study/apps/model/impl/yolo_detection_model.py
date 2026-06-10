from pathlib import Path
from typing import Any, List

from PIL.Image import Image
from ultralytics import YOLO

from apps.const.image_const import ImageConst
from apps.dto.detection_result import DetectionResult
from apps.model.interface.base_detection_model import BaseDetectionModel


class YoloDetectionModel(BaseDetectionModel):
    """YOLO 系列模型（ultralytics）"""

    def __init__(self, model_path: Path, score_threshold: float = 0.5):
        self._model_path = model_path
        self._model = None
        self._score_threshold = score_threshold
        self._labels = ImageConst.YOLO_LABELS

    @property
    def model_path(self) -> Path:
        return self._model_path

    @property
    def name(self) -> str:
        return "ultralytics.YOLO"

    @property
    def labels(self) -> List[str]:
        return self._labels

    def load(self, model_path: Path) -> None:
        print(f"loading model from {model_path}")
        self._model = YOLO(str(model_path))


    def predict(self, image: Image) -> DetectionResult:
        if self._model is None:
            raise RuntimeError("模型尚未載入，請先呼叫 load()")

        output = self._model(image, verbose=False)[0]
        boxes, labels, scores = [], [], []
        # 每個 label 若有重複取分數最高
        best = {}  # label_str -> (box, label_idx, score)

        for box in output.boxes:
            label_str = output.names[int(box.cls[0])]
            label_idx = self._labels.index(label_str) if label_str in self._labels else -1

            if label_idx == -1:
                continue

            score = round(float(box.conf[0]), 4)
            if label_str not in best or score > best[label_str][2]:
                best[label_str] = (box, label_idx, score)

        for box, label_idx, score in best.values():
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            boxes.append((int(x1), int(y1), int(x2), int(y2)))
            labels.append(label_idx)
            scores.append(score)

        return DetectionResult(boxes=boxes, labels=labels, scores=scores)