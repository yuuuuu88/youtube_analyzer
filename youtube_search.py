import requests
import time
import os
import pandas as pd

def search(youtube,num):
    search_response = youtube.search().list(
    part='snippet',
    #検索クエリ
    q='歌い手',
    #視聴回数の多い順
    order='viewCount',
    type='video',
    #50件
    maxResults=50,
    #アップロード日が2020/07/01以降
    publishedAfter='2021-07-01T00:00:00Z',
    #アップロード日が2020/12/01以前
    publishedBefore='2022-12-01T00:00:00Z'
    )
    output = youtube.search().list(
    part='snippet',
    q='歌い手',
    order='viewCount',
    type='video',
    maxResults=50,
    publishedAfter='2021-07-01T00:00:00Z',
    publishedBefore='2022-12-01T00:00:00Z'
    ).execute()

    #ループ回数_50×num枚取得
    num = int(num/50)
    #動画情報を格納するリスト
    video_list = []
    for i in range(num):
        video_list = video_list + output['items']
        search_response = youtube.search().list_next(search_response, output)
        output = search_response.execute()
    # dfに格納
    df = pd.DataFrame(video_list)
    df1 = pd.DataFrame(list(df['id']))['videoId']
    df2 = pd.DataFrame(list(pd.DataFrame(list(pd.DataFrame(list(df['snippet']))['thumbnails']))['high']))['url']
    df = pd.concat([df1, df2], axis = 1)
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    return df


def take_pic(df):
    df_loop = df
    for i in range(len(df_loop)):
    #     idでfileの存在確認→画像取得
        vid = df_loop.loc[i,"videoId"]
        filename = 'data/' + vid + '.jpg'
        if os.path.isfile(filename) == 0:
            #URLを入力して画像そのものを取得
            response = requests.get(df_loop.loc[i, 'url'])
            image = response.content
            with open(filename, "wb") as f:
                f.write(image)
