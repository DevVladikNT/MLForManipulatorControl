import pickle

import numpy as np
import keras

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from manipulator import Manipulator

description = """
This is description
"""

# tags_metadata = [
#     {
#         "name": "tinkoff",
#         "description": "Operations with prices and companies' info."
#                        "Information has been taken from Tinkoff API.",
#         "externalDocs": {
#             "description": "Tinkoff API",
#             "url": "https://developer.tinkoff.ru/docs/api",
#         },
#     },
#     {
#         "name": "user",
#         "description": "Operations with users.",
#     },
#     {
#         "name": "operation",
#         "description": "Financial operations.",
#     },
# ]

# Base.metadata.create_all(bind=engine)
app = FastAPI(
    title='Manipulator',
    description=description,
    version='0.0.1',
    contact={
        'name': 'Vladislav',
        'url': 'https://github.com/DevVladikNT',
    },
    # openapi_tags=tags_metadata
)

# app.include_router(operations_router)
# app.include_router(tinkoff_router)
# app.include_router(tokens_router)
# app.include_router(users_router)

origins = [
    'http://localhost:5173',  # npm run dev
    'http://localhost:4173',  # npm run preview
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# @app.get('/')
# async def main():
#     return FileResponse('./web_app/dist/index.html')
#
#
# @app.get('/assets/index-RE7RdWfF.js')
# async def main():
#     return FileResponse('./web_app/dist/assets/index-RE7RdWfF.js')
#
#
# @app.get('/assets/index-Uu9FJ874.css')
# async def main():
#     return FileResponse('./web_app/dist/assets/index-Uu9FJ874.css')

def converter(arr: list):
    return list(map(float, arr))


@app.post('/simple')
async def main(request: Request):
    data = await request.json()
    print(data)
    result = await gen_accel_simple(data)
    return result


@app.post('/greedy')
async def main(request: Request):
    data = await request.json()
    print(data)
    result = await gen_accel_greedy(data)
    return result


@app.post('/nn')
async def main(request: Request):
    data = await request.json()
    print(data)
    result = await gen_accel_nn(data)
    return result


model = None


async def gen_accel_simple(data):
    manipulator = Manipulator(converter(data['lengths']),
                              converter(data['weights']),
                              data['additional_m'])
    manipulator.set_angles(converter(data['angles']))
    manipulator.set_goal(converter(data['goal_point']))
    disable_direction = True

    t_k = float(data['target_time'])
    end_point = np.array(converter(data['target_angles']))
    const_accel = None

    counter = 0
    accel_arr = []
    coord_arr = []
    while counter <= t_k and manipulator.loss() != 0:
        counter += 1

        if const_accel is None:
            const_accel = (end_point - manipulator.angle) / (t_k / 2) ** 2

        if counter <= t_k / 2:
            result = const_accel
        elif counter < t_k:
            result = -1 * const_accel
        else:
            result = np.zeros(len(data['lengths']))

        item = {'step': counter}
        for i in range(len(result)):
            item[f'Звено {i+1}'] = result[i]
        accel_arr.append(item)
        manipulator.make_step(result, disable_direction=disable_direction)
        coord_arr.append(manipulator.get_coord(scaled=True).tolist())
    return {
        'accel': accel_arr,
        'coord': coord_arr,
        'goal': manipulator.get_goal(scaled=True).tolist(),
    }


async def gen_accel_greedy(data):
    manipulator = Manipulator(converter(data['lengths']),
                              converter(data['weights']),
                              data['additional_m'])
    manipulator.set_angles(converter(data['angles']))
    manipulator.set_goal(converter(data['goal_point']))
    disable_direction = False

    counter = 0
    accel_arr = []
    coord_arr = []
    while counter < 200 and manipulator.loss() != 0:
        counter += 1

        best_accel = [0] * len(manipulator.length)
        best_loss = manipulator.loss() * 2

        segments = 10
        for i in range(segments):
            for j in range(segments):
                for k in range(segments):
                    accel = [(segments / 2 - i) / (segments / 2) * manipulator.accel_limit[0],
                             (segments / 2 - j) / (segments / 2) * manipulator.accel_limit[1],
                             (segments / 2 - k) / (segments / 2) * manipulator.accel_limit[2]]
                    loss = manipulator.predict_step(accel)
                    if loss < best_loss:
                        best_loss = loss
                        best_accel = accel
        result = best_accel

        item = {'step': counter}
        for i in range(len(result)):
            item[f'Звено {i+1}'] = result[i]
        accel_arr.append(item)
        manipulator.make_step(best_accel, disable_direction=disable_direction)
        coord_arr.append(manipulator.get_coord(scaled=True).tolist())
    return {
        'accel': accel_arr,
        'coord': coord_arr,
        'goal': manipulator.get_goal(scaled=True).tolist(),
    }


async def gen_accel_nn(data):
    manipulator = Manipulator(converter(data['lengths']),
                              converter(data['weights']),
                              data['additional_m'])
    manipulator.set_angles(converter(data['angles']))
    manipulator.set_goal(converter(data['goal_point']))
    disable_direction = False

    counter = 0
    accel_arr = []
    coord_arr = []
    while counter < 200 and manipulator.loss() != 0:
        counter += 1

        config = manipulator.get_config()
        best_accel = model.predict([config], verbose=0)[0]
        result = best_accel * manipulator.accel_limit

        item = {'step': counter}
        for i in range(len(result)):
            item[f'Звено {i+1}'] = result[i]
        accel_arr.append(item)
        manipulator.make_step(result, disable_direction=disable_direction)
        coord_arr.append(manipulator.get_coord(scaled=True).tolist())
    return {
        'accel': accel_arr,
        'coord': coord_arr,
        'goal': manipulator.get_goal(scaled=True).tolist(),
    }


@app.on_event("startup")
async def startup():
    global model
    print('Loading model...')
    model = keras.models.load_model('model.keras')
    print('Model loaded!')


HOST, PORT = '127.0.0.1', 2000

if __name__ == '__main__':
    try:
        uvicorn.run(app, host=HOST, port=PORT)
    except KeyboardInterrupt:
        print('\nServer has been stopped!')
