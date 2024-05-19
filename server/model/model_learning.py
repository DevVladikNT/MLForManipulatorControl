import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras
from keras import layers

input_layer = layers.Input(shape=(11,))
x = layers.Dense(12, activation='elu')(input_layer)
x = layers.Dense(24, activation='elu')(x)
x = layers.Dense(12, activation='relu')(x)
output = layers.Dense(3, activation='linear')(x)
model = keras.Model(input_layer, output)

model.compile(optimizer='adam', loss='mse')

df = pd.read_csv('data.csv', index_col=0)
x = df.drop(['a1', 'a2', 'a3'], axis=1).to_numpy()
y = df[['a1', 'a2', 'a3']].to_numpy()

history = model.fit(x, y, validation_split=0.2, epochs=200)
model.save('model.keras')
loss = history.history['loss']
v_loss = history.history['val_loss']
plt.plot(np.arange(len(loss)-1), loss[1:], label='train')
plt.plot(np.arange(len(loss)-1), v_loss[1:], label='val')
plt.xlabel('Epoch')
plt.ylabel('loss')
plt.legend()
plt.show()


