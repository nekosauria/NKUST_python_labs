## add requirements.txt
./python -m pip freeze > ../../requirements.txt

## 本次部署以 ubuntu 26.04, Python 3.14.4 為例
cat /etc/os-release
python3 --version

## scp project
mkdir -p /opt/NKUST_python_labs/independent_study/logs
# ......
sudo chown -R teddylai:teddylai /opt/NKUST_python_labs/independent_study

# add python venv & venv install package
cd /opt/NKUST_python_labs/independent_study
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r build/requirements.txt

# add systemd service
sudo vi /etc/systemd/system/independent_study.service

```
[Unit]
Description=NKUST Independent Study
After=network.target

[Service]
Type=simple
User=teddylai

# 專案的根目錄路徑
WorkingDirectory=/opt/NKUST_python_labs/independent_study
# 環境變數設定 (如果有使用 .env 檔案也可以指過去)
Environment="PATH=/opt/NKUST_python_labs/independent_study/.venv/bin:$PATH"

# 啟動指令：直接呼叫虛擬環境內的 gunicorn 或 python 執行檔
ExecStart=/opt/NKUST_python_labs/independent_study/.venv/bin/python3 /opt/NKUST_python_labs/independent_study/app.py

# 異常崩潰時自動重啟
Restart=always
RestartSec=5

# 標準輸出與錯誤日誌導向系統日誌
StandardOutput=file:/opt/NKUST_python_labs/independent_study/logs/app.log
StandardError=file:/opt/NKUST_python_labs/independent_study/logs/error.log

[Install]
WantedBy=multi-user.target
```

# enable systemd
sudo systemctl daemon-reload
sudo systemctl start independent_study
sudo systemctl enable independent_study
sudo systemctl status independent_study