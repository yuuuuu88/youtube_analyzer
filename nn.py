from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPool2D
from keras.layers import Dense, Activation, Dropout, Flatten
import keras
import glob
import os
import requests
import numpy as np

# modelの構築
def create_nn(input_shape):
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mean_squared_error',
                  optimizer='Adam',
                  metrics=['accuracy'])
    return model

# 学習
def train_nn(model,x_train,y_train):
    #バッチサイズ
    batch_size = 100
    #エポック数
    epochs = 50
    es_cb = keras.callbacks.EarlyStopping(
        monitor='loss', min_delta=0.0001, patience=10, mode='auto')
    #学習
    history = model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              callbacks = [es_cb],
              verbose=1,
              validation_split=0.2)
    #保存
    path = "models"
    file_dir = "models/*"
    file_count = len(glob.glob(file_dir))
    filename = "model{0:04d}".format(file_count)
    model.save(os.path.join(path, filename))
    return model

# モデルをload
def load_model():
    path = "models"
    file_dir = "models/*"
    file_count = len(glob.glob(file_dir))
    filename = "model{0:04d}".format(file_count-1)
    model = keras.models.load_model(os.path.join(path, filename))
    return model

# modelの評価
def evaluate(model,x_test,y_test):
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)

    print('test_loss:',test_loss)
    # 0.07156232252293267
    print('test_acc:',test_acc)
    # 0.9786

# 画像の推定（今回は50万回再生以上行くサムネか）
def predict(vid,model):
    import cv2
    filename = 'testdata/' + vid + '.jpg'
    # filename = file_dir#自分の画像がある場合、ディレクトリを入れる。

    #idのサムネイルがなければとってくる
    if os.path.isfile(filename) == 0:
        #URLを入力して画像を取得
        url = 'https://i.ytimg.com/vi/{}/hqdefault.jpg'.format(vid)
        response = requests.get(url)
        image = response.content
        with open(filename, "wb") as f:
            f.write(image)
    #画像の加工
    img = cv2.imread(filename)
    res = cv2.resize(img, dsize=(256, 256), interpolation=cv2.INTER_CUBIC)
    res = res/255
    res = res[np.newaxis,:, :, :]

    #推定
    predictions = model.predict(res)
    print('再生回数が50万回以上行く確率は:',predictions[0][0]*100,'％')
    # 上手くいかないと値がマイナスになる。
    if predictions[0][0]<0:
        print("学習がうまくいってません")
