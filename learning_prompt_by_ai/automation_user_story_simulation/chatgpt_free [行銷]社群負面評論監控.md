<question>
行銷人員需要隨時緊盯公司粉專.
只要有人留言不滿意、憤怒、退款相關內容.
系統必須立刻在公司的 LINE 發通知給相關人員
</question>

<content>

## # 自動化五問

1. 起點: Facebook 粉專新增留言事件（使用者留言觸發）

2. 終點: 符合條件留言即時透過 LINE 發送通知至指定人員或群組完成

3. 判斷:
   - Trigger condition（觸發條件）:
     - Facebook Graph API comment_created event（Webhook / polling）
   - business rule（關鍵規則 / keyword / threshold）:
     - 關鍵字：不滿意、憤怒、退款、投訴、抱怨、refund
     - 或 NLP 情緒分類：negative / anger / complaint / refund intent

4. 失敗處理:
   - API / 系統失敗:
     - Facebook API / LINE API 呼叫失敗需記錄 log
   - retry 機制:
     - LINE 通知失敗 retry 3 次（exponential backoff）
     - webhook 遺失 → polling 補償機制
   - fallback（人工處理）:
     - 進入 dead-letter queue（DLQ）
     - 提供後台手動補發通知功能

5. 值得做嗎:
   - ROI summary（時間 / 人力 / 風險）:
     - 時間：減少人工監看粉專成本（約 1–3 人時/日）
     - 人力：降低輪班監控需求
     - 風險：降低負面留言延遲處理導致公關危機
     - 自動化：高（事件驅動即時通知系統）
     - 可追蹤性：留言→判斷→通知全鏈路可追蹤

---

## # 需求點（Functional Requirements）

- 接收 Facebook 粉專留言事件（Webhook / polling）
- 解析留言內容並進行情緒與關鍵字分析
- 判斷留言是否屬於負面或退款相關內容
- 即時推送符合條件事件至 LINE Notify / Messaging API
- 記錄所有事件與通知結果（audit log）
- 建立 retry 機制與 dead-letter queue（DLQ）
- 提供管理介面查詢與補發通知功能

---

## # 缺少資訊（Missing Requirements）

### 1. 業務規則缺失
- 情緒判斷使用 keyword 或 NLP model
- 退款類事件是否具有更高優先級

### 2. 系統整合缺失
- Facebook API 使用 webhook 或 polling
- LINE 使用 Notify、Messaging API 或 Bot API

### 3. 流程 / 權限缺失
- 通知對象（個人 / 群組 / 多部門）
- 是否需要 escalation 機制

### 4. 資料格式缺失
- 留言 schema（id / user / content / timestamp）
- log 格式與保存期限（retention policy）

---

## # 判斷價值（Business Value）

1. 時間節省
- 減少人工監看社群與篩選留言時間

2. 風險降低
- 即時處理負面留言，降低品牌危機擴散

3. 自動化程度提升
- 從人工監控轉為 event-driven 自動化

4. 可追蹤性
- 全流程（留言→判斷→通知）可完整追蹤與稽核

</content>