[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

[English](README.md) | [繁體中文](README-zh.md)

# Panasonic Smart App

Home Assistant 的 [Panasonic Smart App](https://play.google.com/store/apps/details?id=com.panasonic.smart&hl=zh_TW&gl=US) 整合套件

# 安裝方法

### 透過 HACS 安裝 (建議)

你需要先將本 repo 加入 HACS

1. 點擊 HACS 頁面右上的三點選單鈕
2. 選擇 "Custom repositories"
3. 將 `https://github.com/osk2/panasonic_smart_app` 貼入網址欄位
4. 將 `Category` 設定為 "Integration"

### 手動安裝

複製 `custom_components/panasonic_smart_app` 至你的 `custom_components/`

# 設定

1. 在「新增整合」的列表中搜尋 `Panasonic Smart App`
2. 依照介面上的指示完成設定

# 附錄

### 可用的實體

| 裝置類型 | 實體類型      | 備註                   |
| -------- | ------------- | ---------------------- |
| 冷氣     | climate       |                        |
|          | sensor        | 室外溫度偵測器         |
| 除濕機   | humidifier    |                        |
|          | number        | 定時開機（若裝置支援） |
|          | number        | 定時關機               |
|          | sensor        | 環境溼度偵測器         |
|          | binary_sensor | 水箱滿水偵測器         |

### 啟用除錯紀錄

將下列設定加入至 `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```

# 版權

本專案依 MIT 條款釋出，請參閱 [LICENSE](LICENSE) 以獲得完整資訊
