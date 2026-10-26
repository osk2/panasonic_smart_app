[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
![Active Installations](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.panasonic_smart_app.total&style=for-the-badge&label=ACTIVE%20INSTALLATIONS&color=yellow)

![GitHub release (latest version)](https://img.shields.io/github/v/release/osk2/panasonic_smart_app?style=for-the-badge)
[![GitHub license](https://img.shields.io/github/license/osk2/panasonic_smart_app?style=for-the-badge)](https://github.com/osk2/panasonic_smart_app/blob/master/LICENSE)

<a href="https://www.buymeacoffee.com/osk2" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

[English](README.md) | [繁體中文](README-zh.md)

# Panasonic Smart App

Home Assistant 的 [Panasonic Smart App](https://play.google.com/store/apps/details?id=com.panasonic.smart&hl=zh_TW&gl=US) 整合套件

## 注意

本整合套件僅支援 Panasonic Smart App，若你使用的是 Panasonic Comfort Cloud，請改用 [sockless-coding/panasonic_cc](https://github.com/sockless-coding/panasonic_cc)

| ![smart-app-icon](https://raw.githubusercontent.com/osk2/panasonic_smart_app/master/assets/smart-app-icon.png) | ![comfort-cloud-icon](https://raw.githubusercontent.com/osk2/panasonic_smart_app/master/assets/comfort-cloud-icon.png) | ![smart-app-plus-icon](https://raw.githubusercontent.com/osk2/panasonic_smart_app/master/assets/smart-app-plus-icon.jpg) |
| :--: | :--: | :--: |
| ✅ 支援 | ❌ 不支援 | ❌ 不支援 |

本專案修改自 [PhantasWeng](https://github.com/PhantasWeng/) 開發的 [panasonic_smart_app](https://github.com/PhantasWeng/panasonic_smart_app)，主要差異為：

1. 支援更多裝置類型
2. 實作 config flow 以大幅簡化設定流程
3. 加入裝置資訊(Device Info)的支援

_完整的實體清單請見 [可用的實體](#可用的實體)_

# 安裝方法

### 透過 HACS 安裝 (建議)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=osk2&repository=panasonic_smart_app&category=integration)

在 HACS 中搜尋 `Panasonic Smart App` 並安裝

### 手動安裝

複製 `custom_components/panasonic_smart_app` 至你的 `custom_components/`

# 設定方法

1. 在「新增整合」的列表中搜尋 `Panasonic Smart App`
2. 依照介面上的指示完成設定

# 附錄

### 支援的裝置型號

經測試確認可支援的裝置清單請見[支援的裝置 / Supported devices](https://github.com/osk2/panasonic_smart_app/discussions/42)

### 可用的實體

| 裝置類型    | 實體類型        | 備註                     |
| ---------- | ------------- | ------------------------ |
| 通用        | sensor        | 用電量偵測器\*             |
|            | sensor        | 碳排量偵測器\*             |
| 冷氣        | climate       |                          |
|            | number        | 定時開機\*                |
|            | number        | 定時關機                  |
|            | sensor        | 室外溫度偵測器             |
|            | sensor        | PM2.5 偵測器\*            |
|            | switch        | nanoe 開關\*              |
|            | switch        | ECONAVI 開關\*            |
|            | switch        | 操控聲音開關\*             |
|            | switch        | 急速模式開關\*             |
|            | switch        | 自體淨開關\*               |
|            | switch        | 乾燥防霉開關\*             |
|            | switch        | 舒眠模式開關\*             |
|            | select        | 動向感應模式\*             |
|            | select        | 機體燈光模式\*             |
| 除濕機      | humidifier    |                          |
|            | number        | 定時開機\*                |
|            | number        | 定時關機                  |
|            | select        | 風量設定                  |
|            | sensor        | 環境溼度偵測器             |
|            | sensor        | PM2.5 偵測器\*            |
|            | binary_sensor | 水箱滿水偵測器             |
| 洗衣機      | sensor        | 洗衣時間偵測器             |
|            | sensor        | 運轉狀態偵測器             |
|            | sensor        | 洗衣模式偵測器             |
|            | sensor        | 洗衣行程偵測器             |
| 空氣清淨機   | switch        | 電源開關                  |
|            | select        | 風量設定\*                |
|            | switch        | nanoeX 開關\*            |
|            | sensor        | PM2.5 偵測器             |
| 電冰箱\**   | sensor        | 冷凍庫溫度偵測器           |
|            | sensor        | 冰藏庫溫度偵測器           |
|            | sensor        | 微凍結溫度偵測器           |
|            | sensor        | 新鮮急凍結等級偵測器        |
|            | sensor        | 冬季模式偵測器             |
|            | sensor        | 購物模式偵測器             |
|            | sensor        | 假日模式偵測器             |
|            | sensor        | 開門次數偵測器            |
|            | select        | 冷凍庫溫度等級設定         |
|            | select        | 冰藏庫溫度等級設定         |
|            | select        | 微凍結溫度等級設定         |
|            | select        | 製冰停止開關              |
|            | select        | 快速製冰開關              |
|            | binary_sensor | 除霜狀態偵測器            |
|            | binary_sensor | ECONAVI 狀態偵測器        |
|            | binary_sensor | nanoe 狀態偵測器          |
| 全熱交換器   | climate       |                         |
| 智慧開關     | switch        | 個別迴路開關               |

\*僅在裝置支援的情況下可用

\*\*只在 NR-D611XGS 上測試過

註：最低需要 Home Assistant 2024.12.0，否則部分實體可能無法使用

更多實體支援請至 [Issue](https://github.com/osk2/panasonic_smart_app/issues) 頁面許願，也歡迎發送 PR 💪

### 如何啟用除錯紀錄？

#### 建議方式
在套件總覽頁面中點選 Enable debug logging

#### 手動啟用紀錄
將下列設定加入至 `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.panasonic_smart_app: debug
```

# 版權

本專案依 MIT 條款釋出，請參閱 [LICENSE](LICENSE) 以獲得完整資訊
