## 📄 `README.md`

````markdown
# 🎤 tiktok-voice-bot

TikTok Liveのコメント・フォロー・ギフトをリアルタイムで日本語音声で読み上げるPython製ボットです。  
非同期処理、キュー制御、TTS（音声合成）を組み合わせ、安定した音声出力が可能です。


## 🚀 特徴

- コメント、フォロー、ギフトを即時音声読み上げ
- gTTSでMP3を生成 → pydubでWAV変換 → playsoundで再生
- Queue + asyncio + threading による安定制御
- Windows環境に最適化

## 🛠 インストール

```bash
pip install -r requirements.txt
````

> ⚠️ 追加で `ffmpeg` が必要です。Windowsユーザーは下記から入手し、環境変数 `PATH` に追加してください：
> [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## 📦 使用方法

1. `main.py` の `USERNAME = "xxxxxxx"` をあなたのTikTok IDに変更
2. 実行

```bash
python tiktok-voice-bot.py
```

ライブ配信が始まると、コメントなどが読み上げられます！

## 🔧 設定・カスタマイズ

* 読み上げ音声：`gTTS` の `lang='ja'` で日本語。他言語対応も可能です。
* 音声再生：`playsound` を使用（MP3よりWAVの方が安定）

## 🤖 今後の拡張案

* 音声をRVCなどでボイス変換
* 読み上げキャラのセリフスタイルをカスタム
* OBS連携して画面上に表示も可能！

## 📄 ライセンス

MIT License

## 👤 Author

[@milkc0de](https://qiita.com/milkc0de)

