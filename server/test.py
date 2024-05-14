import requests
import numpy as np

data = {
    'lengths': [5, 3, 2],
    'weights': [50, 30, 20],
    'angles': [np.pi/3, -np.pi/3, 0.],
    'goal_point': [6, 4],
    'additional_m': 1,
}

result = requests.post('http://127.0.0.1:2000/nn', json=data)
print(result.text)
