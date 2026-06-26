from pathlib import Path
from typing import Dict, Any

import torch

from apps.const.image_const import ImageConst
from apps.model.interface.base_detection_model import BaseDetectionModel
from apps.model.impl.torch_detection_model import TorchDetectionModel
from apps.model.impl.yolo_detection_model import YoloDetectionModel


class DetectionModelFactory:
    """全域模型工廠（單例模式），確保每種模型在記憶體中只會被加載一次"""
    _instances: Dict[str, BaseDetectionModel] = {}

    @classmethod
    def _get_linux_device(cls) -> Any:
        """
        針對 Linux 環境優化的四大平台硬體偵測
        優先序: NVIDIA/AMD (cuda) -> Intel Arc (xpu) -> Mac (mps) -> CPU
        """
        # 檢查 NVIDIA GPU 或 AMD GPU (Linux 下 ROCm 也是對應 cuda)
        if torch.cuda.is_available():
            # 可以透過裝置名稱進一步區分是英偉達還是超微（純日誌紀錄用）
            device_name = torch.cuda.get_device_name(0).lower()
            if "amd" in device_name or "radeon" in device_name:
                print(f"Detected AMD GPU (ROCm) -> [{torch.cuda.get_device_name(0)}] -> Using 'cuda'")
            else:
                print(f"Detected NVIDIA GPU (CUDA) -> [{torch.cuda.get_device_name(0)}] -> Using 'cuda'")
            return "cuda"

        # 檢查 Intel Arc / Intel 顯示卡
        if hasattr(torch, "xpu") and torch.xpu.is_available():
            print("Detected Intel GPU (Arc/Flex) -> Using 'xpu'")
            return torch.device("xpu")

        # 檢查 Mac / Apple Silicon 後端 (保留彈性)
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            print("Detected Apple Silicon 後端 -> Using 'mps'")
            return "mps"

        # Fallback 回 CPU
        print("No GPU acceleration detected -> Falling back to 'cpu'")
        return "cpu"

    @classmethod
    def init_models(cls, root_path: str):
        """在 Flask App 啟動時，由全域呼叫此函式進行『冷啟動』加載"""
        print("=== 初始化全域模型常駐記憶體 ===")

        # 自動辨識 Linux 最佳硬體
        gpu_device = cls._get_linux_device()

        # 預先載入 Torch 模型
        torch_path = Path(root_path) / "model" / "maskrcnn_model.pt"
        torch_model = TorchDetectionModel(
            model_path=torch_path,
            score_threshold=ImageConst.SCORE_THRESHOLD,
            device=gpu_device
        )
        torch_model.load()  # 確保這裡執行了真正的 .load()
        cls._instances[ImageConst.MODEL_TORCH] = torch_model

        # 預先載入 YOLO 模型
        yolo_path = Path(root_path) / "model" / "yolo11n.pt"
        yolo_model = YoloDetectionModel(
            model_path=yolo_path,
            score_threshold=ImageConst.SCORE_THRESHOLD,
            device=gpu_device
        )
        yolo_model.load()  # 確保這裡執行了真正的 .load()
        cls._instances[ImageConst.MODEL_YOLO] = yolo_model

        print("=== 所有 AI 模型載入完畢，準備就緒 ===")

    @classmethod
    def get_model(cls, model_type: str) -> BaseDetectionModel:
        """API 路由呼叫這個方法，直接從記憶體拿，不讀寫硬碟"""
        model = cls._instances.get(model_type)
        if model is None:
            raise ValueError(f"Unknown model type or model not initialized: {model_type}")
        return model