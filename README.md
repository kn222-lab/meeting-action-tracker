# Meeting Action Tracker

会議で決まった「やること（アクション）」を、  
**会議単位でシンプルに管理するWebアプリ**です。

> Reframe /  
> ― 会議の見え方を、少しだけ変える

---

## 🌐 Demo

👉 https://meeting-action-tracker.onrender.com/ui/meetings

※ 認証なしで誰でも閲覧・操作できます  
※ Render Freeプランのため、初回アクセス時に数十秒かかる場合があります

---

## ✨ 主な機能

- 会議の一覧表示
- 会議の追加（日付付き）
- 会議の削除
- 会議ごとのアクション件数表示
- シンプルで直感的なUI

---

## 🖼 画面イメージ

- 会議一覧画面  
- 会議追加フォーム  
- 会議詳細画面（アクション管理）

※ 最小構成で「実務に耐える流れ」を重視しています

---

## 🛠 技術スタック

- **Backend**: Python / FastAPI
- **Template Engine**: Jinja2
- **Database**: SQLite
- **Frontend**: HTML / CSS（Vanilla）
- **Deployment**: Render
- **Version Control**: Git / GitHub

---

## 💡 このアプリを作った理由

会議で決まったタスクが、

- 議事録に埋もれる
- 誰の担当か分からなくなる
- 実行されないまま次の会議を迎える

という経験から、  
**「会議」と「アクション」を最小単位で結びつけるツール**を作りました。

機能を盛りすぎず、

- 誰でも迷わず使える
- 実装・構成が読みやすい
- 拡張しやすい設計

を意識しています。

「会議＝記録」で終わらせず、  
**「会議＝次の一歩が見える場」へリフレームする**ことを目指しました。

---

## 🚀 今後の改善予定

- アクションの担当者設定
- 期限（Due Date）管理
- ステータス管理（未着手 / 進行中 / 完了）
- 認証機能（ユーザーごとに管理）
- UIの改善（モバイル対応）

---

## 📂 リポジトリ構成（抜粋）

app/
├── main.py
├── database.py
├── models/
├── schemas/
├── templates/
│ ├── base.html
│ ├── meetings.html
│ └── meeting_detail.html
├── static/
│ └── style.css



---

## 👤 Author

Namiki Kenta  
【Reframe /】

業務効率化 / Webアプリ開発 / DX支援  
現場の違和感を、仕組みで整える
