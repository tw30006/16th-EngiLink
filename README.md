## 成員
- andyhuangdev `https://github.com/andyhuangdev`
- b89k57w62 `https://github.com/b89k57w62`
- ula0218 `https://github.com/ula0218`
- tw30006 `https://github.com/tw30006`
- yuling515 `https://github.com/yuling515`

## 安裝步驟
1. 安裝 `node` 和 `npm`
2. 通過 `pipx install poetry` 安裝 Python 和套件管理器 `poetry`
3. 執行 `brew install weasyprint` 安裝 WeasyPrint
4. 執行 `poetry shell` 以進入或激活虛擬環境
5. 執行 `make install` 安裝必要的套件
6. 執行 `npm run dev` 啟動前端伺服器
7. 如果需要，執行 `make migrate` 來應用數據庫遷移
8. 將 `.env.example` 文件改名為 `.env` 並向開發人員索取 KEY
9. 執行 `make server` 啟動伺服器
10. 訪問 `http://localhost:8000` 查看應用程序
