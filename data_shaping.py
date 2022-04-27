import glob
import PIL
import keras
from keras.preprocessing import image
import numpy as np
from sklearn.model_selection import train_test_split

#統計情報を取得する関数
def get_statistics(id,youtube):
    statistics = youtube.videos().list(part = 'statistics', id = id).execute()['items'][0]['statistics']
    return statistics

def shape(youtube,input_shape,num):
    #画像データ
    x = []
    #ラベル(視聴数)
    y = []
    image_list = glob.glob('data/*.jpg')
    for f in image_list:
        x.append(image.img_to_array(image.load_img(f, target_size=input_shape[:2])))
        n1 = f.find('data')
        n2 = f.rfind('.jpg')
        name = f[n1+5:n2]
        statistics = get_statistics(name,youtube)
        y.append(int(statistics['viewCount']))

    #npに変換
    x = np.asarray(x)
    x /= 255
    y1 = np.asarray(y)
    # 50万回以上を1にする。
    y1 = np.where(y1>num, 1, 0)
    #データ分割
    x_train, x_test, y_train, y_test = train_test_split(x, y1, test_size=0.33, random_state= 3)

    return x_train, x_test, y_train, y_test
