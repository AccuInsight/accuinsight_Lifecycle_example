import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import numpy as np
import argparse

### Argument parser를 통해 하이퍼파라미터 설정
parser = argparse.ArgumentParser()
parser.add_argument('--num_nodes', type=int, default=128)
parser.add_argument('--learning_rate', type=float, default=0.01)
args = parser.parse_args()

# filestorage에 저장되어있는 데이터를 불러옵니다.
X_train = pd.read_csv('filestorage/X_train.csv')
y_train = pd.read_csv('filestorage/y_train.csv')
X_valid = pd.read_csv('filestorage/X_valid.csv')
y_valid = pd.read_csv('filestorage/y_valid.csv')
X_test = pd.read_csv('filestorage/X_test.csv')
y_test = pd.read_csv('filestorage/y_test.csv')

# normalize
train_stats = X_train.describe().transpose()

def norm(x):
    return (x - train_stats['mean']) / train_stats['std']

normed_train = norm(X_train)
normed_valid = norm(X_valid)
normed_test = norm(X_test)

# model
def build_model():
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(X_train.keys())]),
        layers.Dense(args.num_nodes, activation='relu'),
        layers.Dense(1)
    ])

    optimizer = tf.keras.optimizers.RMSprop(args.learning_rate)

    model.compile(loss = 'mse',
                  optimizer = optimizer,
                  metrics = ['mae', 'mse'])
    return model

model = build_model()

# validation 평가
valid_loss, valid_mae, valid_mse = model.evaluate(normed_valid, y_valid, verbose=2)

### AutoDL에서 평가 지표를 수집할 수 있도록 Metrics Collector의 metricsFormat에 맞추어 평가 지표를 출력
print('valid_mae={:.4f}'.format(valid_mae))
