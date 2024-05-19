import os
import copy
import random
import time
import numpy as np
import pandas as pd

from manipulator import Manipulator

if __name__ == '__main__':
    history = []

    stop_counter = 3
    simulations = 100

    for sim in range(1, simulations+1):
        random_m = np.random.random()
        print(f'Simulation #{sim}\nm = {random_m}\n')

        lengths = [5., 3., 2.]
        weights = [50., 30., 20.]
        manipulator = Manipulator(lengths, weights, random_m)
        manipulator.set_angles([
            random.random() * np.pi,
            random.random() * np.pi,
            random.random() * np.pi
        ])
        buff = random.random()
        goal_point = [
            buff * np.sum(lengths),
            random.random() * np.sum(lengths) * (1 - buff ** 2) ** 0.5
        ]
        manipulator.set_goal(goal_point)

        counter = 0
        steps = 0
        time_start = time.time()
        while counter != stop_counter:
            best_accel = [0] * 3
            best_loss = manipulator.loss() * 2

            segments = 10
            for i1 in range(segments):
                for j1 in range(segments):
                    for k1 in range(segments):
                        manipulator1 = copy.deepcopy(manipulator)
                        accel1 = [(segments/2 - i1) / (segments/2) * manipulator.accel_limit[0],
                                  (segments/2 - j1) / (segments/2) * manipulator.accel_limit[1],
                                  (segments/2 - k1) / (segments/2) * manipulator.accel_limit[2]]
                        manipulator1.make_step(accel1)

                        loss = manipulator1.loss()
                        if loss < best_loss:
                            best_loss = loss
                            best_accel = accel1

            history.append([*manipulator.get_config(), *(np.array(best_accel)/manipulator.accel_limit)])

            manipulator.make_step(best_accel)

            steps += 1
            if steps % 10 == 0:
                print(f'{steps} steps')
                print(f'Time: {(time.time() - time_start) / 10 :.3f} sec per step\n')
                time_start = time.time()

            if manipulator.loss() == 0:
                counter += 1
            else:
                counter = 0

    exists = os.path.exists('data.csv')
    df_new = pd.DataFrame(data=history, columns=['v1_x', 'v1_y',
                                                 'v2_x', 'v2_y',
                                                 'v3_x', 'v3_y',
                                                 's1', 's2', 's3',
                                                 'g_x', 'g_y',
                                                 'a1', 'a2', 'a3'])
    if not exists:
        df_new.to_csv('data.csv')
    else:
        df = pd.read_csv('data.csv', index_col=0)
        df = pd.concat([df, df_new])
        df.reset_index(inplace=True, drop=True)
        df.to_csv('data.csv')
