import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras import backend
from keras.utils.np_utils import to_categorical


df_train = pd.read_csv('train_data.csv', index_col=False)
labels = df_train[['784']]

df_train.drop(df_train.columns[[784]], axis=1, inplace=True)
df_train.head()

np.random.seed(1212)

backend.set_image_data_format('channels_first')
labels = np.array(labels)
cat = to_categorical(labels, num_classes=17)

train_list = []
for i in range(60695):
    train_list.append(np.array(df_train[i:i + 1]).reshape(1, 28, 28))

np.random.seed(7)

model = Sequential()
model.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(15, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(17, activation='softmax'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(np.array(train_list), cat, epochs=1000, batch_size=200, shuffle=True, verbose=1)
model_json = model.to_json()
with open("model_final.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model_final.h5")
