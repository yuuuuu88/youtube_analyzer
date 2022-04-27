# youtube_analyzer

youtubeのサムネをスクレイピングし、機械学習させ、視聴回数が50万回以上になるかを推測するシステムである。
 
# Features
 
作ったサムネイルの評価が行える。
50万再生行くのも夢じゃないかも！？
 
# Requirement

"youtube_analyzer"を動かすのに必要なライブラリなどを列挙する
 
* keras
* requests
* numpy
* pandas
* pillow
* sklearn
 
# Installation
 
Requirementで列挙したライブラリなどのインストール方法を説明する
 
```bash
pip install keras
pip install requests
pip install numpy
pip install pandas
pip install pillow
pip install sklearn
```
 
# Usage
 
使い方<br>

初めに、以下の記事を参考にしてYouTube Data API v3　のAPIキーを取得する<br>
https://masaki-blog.net/youtube-data-api<br>


main.pyを実行する。
```bash
git clone https://github.com/yuuuuu88/youtube_analyzer.git
cd youtube_analyzer
python main.py
```
<br>

次に指示に従い、収集または学習を行うか判断する。<br>
```bash
APIkeyを入力してください:　APIkey
画像収集は行いますか？yes→1,no→0：　0or1
学習済みですか？（実行したことがあるか）yes→1,no→0：　0or1
```
<br>

modelの評価を行う。<br>
ここではlossとaccを表示する。<br>
loss:損失値→小さいほど学習できている。<br>
acc:正解率<br>
<br>

最後に推測を行う。ここではわかりやすいように、youtubeから画像を取得し、その評価を行っている。
youtubeの動画のidが求められるが、以下の動画のアドレスを例に挙げると、v=の後がidとなる。
https://www.youtube.com/watch?v=XaFVb3FinMo
```bash
動画のidを入力してください:　id
```
<br>

また、自分が作成した画像がある場合は nn.py 内を変更する。
```bash
#nn.py
#~~~
def predict(vid,model):
    import cv2
    filename = 'testdata/' + vid + '.jpg'
    # filename = file_dir#自分の画像がある場合、ディレクトリを入れる。←←←
#~~~
```
 
# Note
 
APIで画像を収集する場合、収集しすぎると制限がかかるので注意してください。
また、サーバーに負荷をかけないように注意してください。
 
# Author
 
作成情報を列挙する
 
* yuuuuu88
* 電気通信大学
* u8te2su9791atgmail.com
 
# License
ライセンスを明示する
 
"youtube_analyzer" is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).

# References
* https://masaki-blog.net/youtube-data-api
* https://qiita.com/Sinhalite/items/39a302491873419af918
