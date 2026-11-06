# 適任證書刷題 — GitHub Pages 發布

此儲存庫只公開已驗收的 `pwa-site/` 網站和必要的發布設定。原始工作目錄的語音模型、Python 環境、測試瀏覽器、測試紀錄、成績備份及舊 ZIP 不在 Git 追蹤範圍。

- 題庫：142 題單選、367 題口語／聽力。
- 離線語音：Kokoro George 英式男聲，682 個預生成 MP3；不是 Google 原聲。
- 作答紀錄只保存在各裝置的瀏覽器／主畫面 App，不會上傳 GitHub，也不會跨裝置同步。
- 網站公開，題庫和前端程式碼也公開。使用者成績不隨儲存庫發布。
- 語音來源與授權位於 `pwa-site/licenses/`。

## 重點碼互傳（不接雲端）

「備份與說明」及「口語與聽力」提供「重點碼互傳」。從來源設備複製完整碼，傳到另一台的主畫面 PWA，貼上後預覽題數、確認取代。只換單選待查／口語重點，不動成績、答案、錯題或語音設定；不會把標註發布到 GitHub。碼未加密，持有者可以匯入。

替換前保存一份目的設備的本機重點備份，可在同一對話框還原；相同碼不重寫。空白／損壞／不同題庫碼拒絕，有效空清單須明確確認才清除重點。不要用原本「匯入備份」代替，該入口會取代全紀錄。

## 第一次發布（使用者操作）

1. GitHub Desktop：`File → Add local repository…`，選原專案資料夾 `E:\Projects\seafarer-exam-local`，不是其中的 HTML、ZIP 或 `pwa-site` 子資料夾。
2. `Publish repository`：建議名稱 `seafarer-exam-pwa`；取消 `Keep this code private`，確認自己的 GitHub 帳號後發布。不要另行 Clone 或建立巢狀專案。
3. GitHub 儲存庫：`Settings → Pages → Build and deployment → Source → GitHub Actions`。
4. 在 `Actions` 檢查 `Deploy seafarer exam PWA to Pages`。首次上傳可能早於 Pages 設定而在 `Setup Pages` 失敗；設定完成後只需對該次工作流程 `Re-run all jobs`，不要重複 Push。如果沒有工作流程執行紀錄，可在該流程選 `Run workflow`，分支 `main`。
5. 工作流程完成後，採用 `Settings → Pages` 或成功部署所顯示的實際網址；再核對遠端 commit、服務中的網站版本及音檔。發布儲存庫成功不等於網站已部署。

此專案不需要付費 API、個人成績後端或額外 Secrets。網站包已完成建置，Actions 不重新生成語音；只驗證檔案並上傳 `pwa-site/`。

## iPhone／iPad

1. 用 Safari 開啟已核驗的 HTTPS 網址，使用分享選單加入主畫面。
2. 從主畫面的 App 圖示開啟，在「安裝／離線」面板下載完整離線資料。下載期間保持前景開啟。
3. 等待所有 682 個音檔校驗完成並顯示可離線使用；首次播放須手動點一次，受 iOS 自動播放政策限制。
4. 開啟飛航模式並關閉 Wi-Fi，完全關閉後從主畫面重開，檢查題目、答案播放、換題及成績保存。
5. 每部裝置分別下載。Safari 和主畫面 App 的資料可能分開；搬移既有紀錄前先使用原 App 的 JSON 備份，匯入會取代目的地目前資料。

本機 Chrome 驗證不等於 iPhone／iPad 真機已驗收；系統清除網站資料或回收儲存空間時仍可能失去離線資料，請保留成績備份。

## 後續更新

保留 `pwa-site/** -text` 屬性：離線完整性校驗依賴精確檔案 bytes，不可讓 Git 改寫換行。新版網站須經原專案建置／驗證後，同步更新 `.github/pwa-release.json` 的版本與摘要；工作流程會阻擋缺檔、多餘檔案或內容不符的網站。

本機手動檢查：

```sh
python3 .github/scripts/verify_site.py
```

更新後仍由使用者 Push。使用者在 App 內確認更新，不需要清除網站資料或成績。
