# sd_infotexts
Perfect Reproduction Generate from Infotexts

- for Stable Diffusion web UI AUTOMATIC1111

## Infotext

これらをInfotextと呼ぶ。
- PNG Infoのparameters
- Image BrowserのGenerate Info
- txt2imgで生成した時に右下に出るログ

このExtensionは、画像とInfotextを相互変換する目的で作られた。

### Infotextは不完全である

- sd_model_hashが衝突する
- Hypernetの名前が重複する
- VAEの情報が無い
- 再現性の妨げになる情報が記録されない

この問題を改善した形式をInfotext Exと呼ぶ。

このExtensionにはInfotext Ex出力機能が同梱されている。

# 画像の保存と生成

txt2imgで生成したPNGを保存する時には PNG Info を残す形で保存することが望ましい。

以下の操作をすると PNG Infoは失われる
- PNGを jpeg や webp などの別形式で保存する
- PNGを別のソフトウェアで加工する
- SD Upscaler以外で拡大処理を行う
- PNGをimgurやtwitterなどの画像圧縮するサービスにアップロードする

## PNGから Infotext を取り出す

- png/ に画像を入れる
- Convertタブを開く
- PNG to TXTを選択する
- Convertボタンを押す

これで txt/ もしくは指定したディレクトリに Infotext が出力される

## Infotext から 画像を生成する

- 生成の設定は Generate タブでおこなう。
- txt2imgのScriptから Generate from Infotexts を選んでから Generate ボタンを押す。
  - edit_txt/ 内のすべての Infotext から画像が生成される

以下は高度な使い方の説明である。

# JSON形式

- 以前は Generate from json として使われていた。
  - 下記のExtensionをインストールする必要は無い。
- Generate from json
  - https://github.com/aka7774/generate_from_json
- Infotextの各要素をJSON形式の配列にすることで、txtを複数に増やすことが出来る。
- TXT to JSON で json形式に変換する。
- jsonファイルを任意の方法(スクリプト等)で加工する。
- JSON to EDIT TXTs で txt形式に戻す。この時txtファイルが複数になる。
- sd_model_hashは、model_hashに改名されたので注意。

# Infotextの一括編集機能

- Macroタブを開いてマクロを作成することが出来る。
- マクロとは文字列置換ルールが記されたテキストファイルを指す。
- マクロはタブ区切りで4列から成る。
  - 1列目は置換対象のInfotextの範囲を示す。
  - 2列目は置換方法を示す。
  - 3列目は、1列目がParamならKeyを示す。2列目がReplaceなら置換前の文字列、re.subなら正規表現を示す。
  - 4列目は、1列目がParamならValueを示す。2列目がReplaceかre.subなら置換後の文字列を示す。
- マクロは1行1件で、上から順に実行される。
- マクロは config/macro.txt に保存される。
- マクロを実行するには、Convertタブの MACRO TXT を選択して Convert を押す

# Infotextの一括生成機能

- JSONやマクロで編集したInfotextから画像を生成することが出来る。
- 完全に再現するにはInfotext Ex形式かついくつかの条件を満たす必要がある。
  - 下記のExtensionをインストールする必要は無い。
- Infotext Ex
  - https://github.com/aka7774/sd_infotext_ex
- 生成の設定は Generate タブでおこなう。
- Output WEBP Directoryを空にすることで、webpの生成を抑止することが出来る。
- 生成は、txt2imgのScriptから Generate from Infotexts を選んでから Generate ボタンを押す。
  - すべての checkpoints, vae, hypernetworksのsha256を計算しファイルに保存する
  - すべての hypernetworksの内部nameを取得しファイルに保存する

# webp生成機能

- Generate from jsonのおまけ機能を移植したもの
  - https://github.com/aka7774/generate_from_json/blob/main/CONFIG.md
- Output WEBP Directoryが指定してあれば、Generateのついでにwebpを生成する
- あるいは、Convertタブの OUTPUT to WEBP でも生成できる
