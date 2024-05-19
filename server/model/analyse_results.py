import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import keras


model = keras.models.load_model('model.keras')
print(model.summary())

df = pd.read_csv('data.csv')
counts = df.groupby('g_x').count().iloc[:, 0]
counts_np = counts.to_numpy()
print(np.mean(counts_np))
print(np.std(counts_np))
print(counts.describe())
fig, ax = plt.subplots(2)
ax[0].hist(counts)
ax[1].boxplot(counts, vert=False)
ax[0].set(ylabel='Number of simulations')
ax[1].set(xlabel='Steps in simulation')
plt.show()
