<question>
新進員工完成線上測驗(google表單). 
人資必需確認分數是否及格(80分),及格者要製作一張 pdf 證書並 email 給員工 , 不及格者要發信提醒重測
</question>

<content>

## # 自動化五問

1. 起點: Google Forms 測驗提交完成（員工填寫並送出答案與分數）

2. 終點: 根據分數自動完成兩種流程之一：
   - 及格（≥80）：生成 PDF 證書並寄送 email
   - 不及格（<80）：寄送重測通知 email

3. 判斷:
   - Trigger condition（觸發條件）:
     - Google Forms response submitted（透過 Google Sheets / Apps Script trigger）
   - business rule（關鍵規則 / keyword / threshold）:
     - score ≥ 80 → pass
     - score < 80 → fail
     - 每筆 response 必須綁定唯一員工 email
     - 重複提交需決定是否覆蓋或忽略

4. 失敗處理:
   - API / 系統失敗:
     - Google Sheets / Apps Script / Gmail / PDF 生成服務失敗需記錄 log
   - retry 機制:
     - email 發送失敗 retry 3 次（exponential backoff）
     - PDF 生成失敗需重試生成流程
     - trigger missed → 定期 batch reconciliation 補償處理
   - fallback（人工處理）:
     - 進入 dead-letter queue（DLQ）
     - 人資後台可手動補發證書或重寄通知

5. 值得做嗎:
   - ROI summary（時間 / 人力 / 風險）:
     - 時間：降低 HR 人工批改與寄送行政時間
     - 人力：減少重複性人工作業依賴
     - 風險：降低誤寄、漏寄與錯判分數問題
     - 自動化：端到端流程自動化（測驗 → 判斷 → 文件 → 通知）
     - 可追蹤性：每次測驗結果與處理紀錄可完整追蹤

---

## # 需求點（Functional Requirements）

- 系統需接收 Google Forms 測驗結果（Google Sheets / Apps Script webhook）
- 系統需解析並取得每位員工的測驗分數與 email
- 系統需依據分數門檻（80分）進行自動判定
- 系統需自動生成 PDF 證書（及格者）
- 系統需自動發送 email（證書或重測通知）
- 系統需記錄所有處理結果（audit log）
- 系統需支援 retry 機制與 batch reconciliation 補償流程
- 系統需支援人工補發與查詢功能

---

## # 缺少資訊（Missing Requirements）

### 1. 業務規則缺失
- 是否允許多次重測
- 是否有考試版本或題庫版本管理
- 及格標準是否固定 80 或可調整

### 2. 系統整合缺失
- PDF 生成方式（Google Docs / third-party service）
- email 發送系統（Gmail / SMTP / enterprise mail）
- Google Forms → Sheets → trigger 架構是否已建立

### 3. 流程 / 權限缺失
- 人資是否可以覆寫判定結果
- 是否需要主管審核證書發送

### 4. 資料格式缺失
- 測驗資料 schema（name / email / score / timestamp）
- PDF 證書模板格式
- email template（語系 / HTML 格式）

---

## # 判斷價值（Business Value）

1. 時間節省
- 大幅減少 HR 批改與寄送證書的行政時間

2. 風險降低
- 避免人工錯誤（誤寄 / 漏寄 / 判分錯誤）

3. 自動化程度提升
- 完整流程自動化（測驗 → 判定 → 文件 → 通知）

4. 可追蹤性
- 所有測驗與通知流程皆可追蹤與稽核