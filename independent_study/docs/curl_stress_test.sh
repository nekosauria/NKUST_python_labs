# 壓力測試

PIC_DIR="/Users/teddylai/Downloads/tmp/picture"

for i in {1..10}; do
  RANDOM_PIC=$(ls "$PIC_DIR"/*.[jJ][pP][gG] "$PIC_DIR"/*.[jJ][pP][eE][gG] "$PIC_DIR"/*.[pP][nN][gG] 2>/dev/null | sort -R | head -n 1)

  if [ -z "$RANDOM_PIC" ]; then break; fi

  # 用小括號包起來丟進背景跑
  (
    # 先撈出 JSON 內容
    JSON_OUT=$(curl -s -X POST https://nkust.nekosaur.com/upload \
      -F "image=@${RANDOM_PIC}" \
      -F "model=torch" | python3 -m json.tool)

    # 集中一次印出來，確保多執行緒併發時，日誌不會交錯碎掉
    echo "==================== Count: $i ===================="
    echo "Testing image: $(basename "$RANDOM_PIC")"
    echo "$JSON_OUT"
    echo -e "==================================================\n"
  ) &
done

wait
echo "=== 併發壓力測試全部結束 ==="