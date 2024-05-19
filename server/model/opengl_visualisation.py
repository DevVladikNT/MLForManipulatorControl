import pickle
import random

import OpenGL.GL as gl
import OpenGL.GLUT as glut
import numpy as np
from matplotlib import pyplot as plt

from manipulator import Manipulator


# Параметры системы
window = None
chains = 3
lengths = [5., 3., 2.]
weights = [50., 30., 20.]

# angles = [np.pi/3, -np.pi/3, 0.]
angles = [2*np.pi/3, 4*np.pi/3, np.pi]
# angles = []
# for _ in range(chains):
#     angles.append(random.random() * np.pi)

# 1 - Релейное
# 2 - Жадный
# 3 - Нейросетевое
alg_num = 1

additional_m = 0
window_size = np.array([500, 500])
start_point = window_size / 2
auto_mode = False
auto_mode_slow_k = 5
auto_mode_counter = 0

# Релейное управление
t_k = 12
end_point = np.array([0.65554567, 5.8161352,  1.69646003])
const_accel = None
t_counter = 0

manipulator = Manipulator(lengths, weights, additional_m)
manipulator.set_angles(angles)
buff = random.random()
goal_point = [6, 4]
# goal_point = [
#     buff * np.sum(lengths),
#     random.random() * np.sum(lengths) * (1 - buff**2)**0.5
# ]
manipulator.set_goal(goal_point)


def transform_coord(coord):
    my_coord = coord.copy()
    for i in range(len(my_coord) - 1):
        my_coord[i + 1] = my_coord[i + 1] + my_coord[i]
    scaled_to_window = my_coord * (window_size / 2 - 20) + start_point
    return scaled_to_window


def func():
    global manipulator, auto_mode_counter
    if auto_mode:
        if auto_mode_counter != auto_mode_slow_k:
            auto_mode_counter += 1
        else:
            auto_mode_counter = 0
            my_func(1)

    # Белый фон
    gl.glColor3f(1.0, 1.0, 1.0)
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex2f(0, 0)
    gl.glVertex2f(500, 0)
    gl.glVertex2f(500, 500)
    gl.glEnd()
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex2f(0, 0)
    gl.glVertex2f(0, 500)
    gl.glVertex2f(500, 500)
    gl.glEnd()

    # Оси со стрелочками
    gl.glLineWidth(1)
    gl.glColor3f(0.0, 0.0, 0.0)
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(0, start_point[1])
    gl.glVertex2f(window_size[0] - 50, start_point[1])
    gl.glEnd()
    gl.glBegin(gl.GL_LINES)
    gl.glVertex2f(start_point[0], 0)
    gl.glVertex2f(start_point[0], window_size[1] - 50)
    gl.glEnd()
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex2f(window_size[0] - 20, start_point[1])
    gl.glVertex2f(window_size[0] - 50, start_point[1] + 5)
    gl.glVertex2f(window_size[0] - 50, start_point[1] - 5)
    gl.glEnd()
    gl.glBegin(gl.GL_TRIANGLES)
    gl.glVertex2f(start_point[0], window_size[1] - 20)
    gl.glVertex2f(start_point[0] + 5, window_size[1] - 50)
    gl.glVertex2f(start_point[0] - 5, window_size[1] - 50)
    gl.glEnd()

    # Цель
    goal = manipulator.get_goal(scaled=True) * (window_size/2 - 20) + start_point
    gl.glPointSize(200 * manipulator.goal_delta / np.sum(manipulator.length) )
    gl.glBegin(gl.GL_POINTS)
    gl.glVertex2f(goal[0], goal[1])
    gl.glEnd()

    # # Манипулятор с грузом
    # gl.glLineWidth(8)
    # gl.glColor3f(0.0, 0.9, 0.7)  # Set the color
    # gl.glBegin(gl.GL_LINES)  # Begin the sketch
    # gl.glVertex2f(coord_arr_m[0], coord_arr_m[1])
    # gl.glVertex2f(coord_arr_m[2], coord_arr_m[3])
    # gl.glVertex2f(coord_arr_m[2], coord_arr_m[3])
    # gl.glVertex2f(coord_arr_m[4], coord_arr_m[5])
    # gl.glVertex2f(coord_arr_m[4], coord_arr_m[5])
    # gl.glVertex2f(coord_arr_m[6], coord_arr_m[7])
    # gl.glEnd()
    #
    # # Груз
    # gl.glLineWidth(16)
    # gl.glBegin(gl.GL_LINES)
    # gl.glVertex2f(0.66 * coord_arr_m[4] + 0.33 * coord_arr_m[6], 0.66 * coord_arr_m[5] + 0.33 * coord_arr_m[7])
    # gl.glVertex2f(0.33 * coord_arr_m[4] + 0.66 * coord_arr_m[6], 0.33 * coord_arr_m[5] + 0.66 * coord_arr_m[7])
    # gl.glEnd()  # Mark the end of drawing

    # Манипулятор без груза
    coord_arr = manipulator.get_coord(scaled=True)
    coord_arr = transform_coord(coord_arr)
    gl.glLineWidth(8)
    gl.glColor3f(0.9, 0.7, 0.0)  # Set the color
    gl.glBegin(gl.GL_LINES)  # Begin the sketch
    gl.glVertex2f(*start_point)
    for i in range(len(coord_arr)-1):
        gl.glVertex2f(*coord_arr[i])
        gl.glVertex2f(*coord_arr[i])
    gl.glVertex2f(*coord_arr[-1])
    gl.glEnd()  # Mark the end of drawing


def iterate():
    gl.glViewport(0, 0, window_size[0], window_size[1])
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gl.glOrtho(0.0, window_size[0], 0.0, window_size[1], 0.0, 1.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()


def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)  # Remove everything from screen (ie displays all white)
    gl.glLoadIdentity()  # Reset all graphic/shape's position
    iterate()
    func()
    glut.glutSwapBuffers()


loss_arr = [[], [], []]
accel_arr = []
energy_arr = []


def append_loss():
    global manipulator
    loss_arr[0].append(manipulator.loss())
    loss_arr[1].append(
        np.sum(np.power(np.abs(manipulator.goal - np.sum(manipulator.get_coord(), axis=0)), 2))
        / np.sum(np.power(manipulator.length, 2))
    )
    loss_arr[2].append(
        (
                np.mean(manipulator.length) ** 3
                * (np.sum(np.abs(manipulator.speed / manipulator.accel_limit))
                   ) / (
                        np.sum(np.power(np.abs(manipulator.goal - np.sum(manipulator.get_coord(), axis=0)), 2)) ** 0.5
                        + np.mean(manipulator.length))
        )
        / np.sum(np.power(manipulator.length, 2))
    )


counter = 0


def my_func(direction):
    global manipulator, counter, auto_mode
    # if random.random() < 0.05:
    #     accel = greedy()
    # else:
    #     accel = ml_alg(manipulator)

    if alg_num == 1:
        disable_direction = True
        accel = rel_alg()
    elif alg_num == 2:
        disable_direction = False
        accel = greedy()
    else:
        disable_direction = False
        accel = ml_alg(manipulator)

    manipulator.make_step(accel, disable_direction=disable_direction)
    accel_arr.append(accel)
    energy_arr.append(manipulator.energy_lost)
    append_loss()

    if auto_mode and manipulator.loss() == 0:
        counter += 1
        if counter == 2:
            auto_mode = False
    else:
        counter = 0


if alg_num == 3:
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)


def ml_alg(m: Manipulator):
    config = m.get_config()
    best_accel = model.predict([config], verbose=0)[0]
    return best_accel * m.accel_limit


def rel_alg():
    global manipulator, const_accel, t_counter, auto_mode, t_k
    if const_accel is None:
        t_k += 1
        const_accel = (end_point - manipulator.angle) / (t_k/2)**2

    if t_counter <= t_k/2:
        result = const_accel
    elif t_counter < t_k:
        result = -1 * const_accel
    else:
        result = np.zeros(len(lengths))

    t_counter += 1
    if t_counter >= t_k:
        auto_mode = False
    return result


def greedy():
    global manipulator
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
    # if random.random() < 0.1:
    #     i = int(random.random() * 3000) % 3
    #     best_accel[i] = random.random() * manipulator.accel_limit / 2

    return best_accel


def keyboard(key, x, y):
    global manipulator, auto_mode, loss_arr
    if key == b'\x1b':
        glut.glutDestroyWindow(window)
    if key == b'a':
        auto_mode = not auto_mode
    if key == b's':
        print(f'End: {manipulator.angle}')
        print(f'Total energy spent: {manipulator.energy_lost}')

        time = np.arange(len(loss_arr[0]))
        figure, axis = plt.subplots(3, 1)
        for i in range(chains):
            axis[0].plot(time, np.array(accel_arr)[:, i], label=f'accel {i}')
        axis[0].set_ylabel('value')
        axis[0].legend()
        axis[1].plot(time, loss_arr[1], label='Distance part')
        axis[1].plot(time, loss_arr[2], label='Speed part')
        axis[1].plot(time, loss_arr[0], label='Total loss')
        axis[1].set_ylabel('value')
        axis[1].legend()
        axis[2].plot(time, energy_arr, label='Total energy')
        axis[2].set_xlabel('time')
        axis[2].set_ylabel('value')
        axis[2].legend()
        plt.show()
    if key == b'd':
        print(manipulator.angle)


if __name__ == '__main__':
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)  # Set the display mode to be colored
    glut.glutInitWindowSize(512, 512)  # Set the w and h of your window
    glut.glutInitWindowPosition(100, 100)  # Set the position at which this windows should appear
    window = glut.glutCreateWindow('Hello World')
    glut.glutDisplayFunc(display)
    glut.glutKeyboardFunc(keyboard)
    glut.glutIdleFunc(display)  # Keeps the window open
    glut.glutMainLoop()  # Keeps the above created window displaying/running in a loop
