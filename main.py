import youtube_search
import data_shaping
import nn
from apiclient.discovery import build
import os

# youtubeapi構築

YOUTUBE_API_KEY = input('APIkeyを入力してください:　')
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)


search_flag = int(input('画像収集は行いますか？yes→1,no→0：　'))#画像収集flag
load_flag = int(input('学習済みですか？（実行したことがあるか）yes→1,no→0：　'))#学習モデルの構築frag

os.makedirs('./data', exist_ok=True)
os.makedirs('./models', exist_ok=True)
os.makedirs('./testdata', exist_ok=True)

if search_flag == 1:
    loopnum = int(input('収集枚数は？50の倍数：　'))
    # youtube検索
    df = youtube_search.search(youtube,loopnum)
    # youtubeサムネイル取得_250枚
    print('サムネイル取得中')
    youtube_search.take_pic(df)

# 画像データの成型、分割
input_shape = (256, 256, 3)
num = 500000#50万回再生以上行くか
x_train, x_test, y_train, y_test = data_shaping.shape(youtube,input_shape,num)

if load_flag == 1:
    # model読み込み
    model = nn.load_model()
else:
    # モデルの作成
    model = nn.create_nn(input_shape)
    # 学習
    print('学習を開始します')
    model = nn.train_nn(model,x_train,y_train)

print('\n\n以下モデルの評価結果です。')
# 評価
nn.evaluate(model,x_test,y_test)

print('\n以下入力画像を推定します。')
# 予測
id = input('動画のidを入力してください：　')
nn.predict(id,model)
