import time
import numpy as np
from fastapi.testclient import TestClient

from main import app

data_for_simple = {
    'lengths': [5, 3, 2],
    'weights': [50, 30, 20],
    'angles': [0., 0., 0.],
    'goal_point': [6, 4],
    'additional_m': 1,
    'target_angles': [np.pi/3, -np.pi/3, 0.],
    'target_time': 10,
}
data = {
    'lengths': [5, 3, 2],
    'weights': [50, 30, 20],
    'angles': [np.pi/3, -np.pi/3, 0.],
    'goal_point': [6, 4],
    'additional_m': 1,
}

server = TestClient(app)
max_time_connection = 1e-2
max_time_nn = 1e-1  # best = 7e-2
max_time_greedy = 2e-1  # best = 1.4e-1


def test_connection():
    s = time.time()
    server.get('/test')
    e = time.time()
    assert e - s < max_time_connection


def test_nn_inference():
    with TestClient(app) as tmp_server:
        s = time.time()
        result = server.post('/nn_step', json=data)
        e = time.time()
        assert result.status_code == 200
        assert e - s < max_time_nn


def test_greedy_inference():
    s = time.time()
    result = server.post('/greedy_step', json=data)
    e = time.time()
    assert result.status_code == 200
    assert e - s < max_time_greedy


def test_simple_alg():
    result = server.post('/simple', json=data_for_simple)
    assert result.status_code == 200


def test_greedy_alg():
    result = server.post('/greedy', json=data)
    assert result.status_code == 200


def test_nn_alg():
    with TestClient(app) as tmp_server:
        result = tmp_server.post('/nn', json=data)
        assert result.status_code == 200
