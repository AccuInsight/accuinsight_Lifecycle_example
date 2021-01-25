from tensorflow import keras
import numpy as np
import argparse

### Argument parser를 통해 하이퍼파라미터 설정
parser = argparse.ArgumentParser()
parser.add_argument('--num_nodes', type=int, default=128)
parser.add_argument('--learning_rate', type=float, default=0.01)
parser.add_argument('--batch_size', type=int, default=128)
args = parser.parse_args()

# filestorage에 저장되어있는 데이터를 불러옵니다.
train_images = np.load('filestorage/train_images.npy')
train_labels = np.load('filestorage/train_labels.npy')
valid_images = np.load('filestorage/valid_images.npy')
valid_labels = np.load('filestorage/valid_labels.npy')
test_images = np.load('filestorage/test_images.npy')
test_labels = np.load('filestorage/test_labels.npy')

train_images = train_images / 255.0
test_images = test_images / 255.0

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(args.num_nodes, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])

Adam = keras.optimizers.Adam(lr=args.learning_rate)

model.compile(optimizer=Adam,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, batch_size=args.batch_size, epochs=5)

valid_loss, valid_acc = model.evaluate(valid_images,  valid_labels, verbose=2)

### AutoDL에서 평가 지표를 수집할 수 있도록 Metrics Collector의 metricsFormat에 맞추어 평가 지표를 출력
print('valid_acc={:.4f}'.format(valid_acc))