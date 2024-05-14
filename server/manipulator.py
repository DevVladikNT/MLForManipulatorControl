import numpy as np


class Manipulator:
    length = None
    weight = None
    weight_centers = None
    m = None
    m_center = None

    angle = None
    speed = None
    accel = None
    adaptive_accel = None

    start_point = None
    goal = None

    current_moment = 0
    energy_lost = 0

    # accel_limit = np.array([np.pi/10, np.pi/10, np.pi/10])
    accel_limit = np.array([np.pi/100, np.pi/100, np.pi/100])
    goal_delta = 0
    g = 9.8

    def __init__(self, lengths: list, weights: list, m: float = 0):
        self.length = np.array(lengths)
        self.weight = np.array(weights)
        self.weight_centers = np.zeros(len(weights)) + 0.5
        self.m = m
        self.m_center = 0.5
        self.angle = np.zeros(len(lengths))
        self.speed = np.zeros(len(lengths))
        # adaptive_accel устанавливаем в 0, затем пытаемся установить в 0 исходное accel,
        # таким образом функцией закладывая в adaptive_accel величину, которая компенсирует
        # отклонение от положения равновесия в начале
        self.adaptive_accel = np.zeros(len(lengths))
        self.accel = self.get_correct_accel([0] * len(self.length))
        self.start_point = np.array([0, 0])
        self.goal_delta = np.sum(self.length) * 0.05

    def set_centers(self, centers: list, center: float):
        self.weight_centers = np.array(centers)
        self.m_center = center

    def set_angles(self, angles: list):
        self.angle = np.array(angles)

    def get_coord(self, scaled: bool = False):
        vectors = []
        sum_l = np.sum(self.length)
        for i in range(len(self.length)):
            vectors.append([
                self.length[i] * np.cos(self.angle[i]) / (sum_l if scaled else 1),
                self.length[i] * np.sin(self.angle[i]) / (sum_l if scaled else 1),
            ])
        return np.array(vectors)

    def get_r(self, delta: bool = False):
        vectors = self.get_coord()
        centers = (vectors.copy().T * self.weight_centers).T
        center = vectors.copy()[-1] * self.m_center
        for i in range(len(vectors) - 1):
            vectors[i + 1] = vectors[i + 1] + vectors[i]
            centers[i + 1] = centers[i + 1] + vectors[i]
        center = center + vectors[-2]
        r = []

        buff = 0.0
        for c in range(len(centers)):
            buff += centers[c, 0] * self.weight[c] * self.g
            buff += (center[0] * self.m * self.g) if delta else 0.0
        r.append(buff)

        for v in range(len(vectors) - 1):
            buff = 0.0
            for c in range(v + 1, len(centers)):
                buff += (centers[c, 0] - vectors[v, 0]) * self.weight[c] * self.g
                buff += ((center[0] - vectors[v, 0]) * self.m * self.g) if delta else 0.0
            r.append(buff)
        return np.array(r)

    def get_j(self, delta: bool = False):
        vectors = self.get_coord()
        centers = (vectors.copy().T * self.weight_centers).T
        center = vectors.copy()[-1] * self.m_center
        for i in range(len(vectors) - 1):
            vectors[i + 1] = vectors[i + 1] + vectors[i]
            centers[i + 1] = centers[i + 1] + vectors[i]
        center = center + vectors[-2]
        j = []

        buff = 0.0
        for c in range(len(centers)):
            buff += (centers[c, 0]**2 + centers[c, 1]**2) * self.weight[c]
            buff += ((center[0]**2 + center[1]**2) * self.m) if delta else 0.0
        j.append(buff)

        for v in range(len(vectors) - 1):
            buff = 0.0
            for c in range(v + 1, len(centers)):
                buff += (
                    (centers[c, 0] - vectors[v, 0])**2 +
                    (centers[c, 1] - vectors[v, 1])**2
                ) * self.weight[c]
                buff += ((
                    (center[0] - vectors[v, 0])**2 +
                    (center[1] - vectors[v, 1])**2
                ) * self.m) if delta else 0.0
            j.append(buff)
        return np.array(j)

    def get_correct_accel(self, accel: list, prediction: bool = False, disable_direction: bool = False):
        if not prediction and not disable_direction:
            # point = np.sum(self.get_coord(), axis=0)
            # goal = 0 if self.goal is None else self.goal
            # distance = np.sum(np.power(np.abs(goal - point), 2))
            # distance_k = distance / np.sum(np.power(self.length, 2))

            direction = np.array(accel) * self.adaptive_accel
            for i in range(len(accel)):
                if direction[i] < 0:
                    self.adaptive_accel[i] *= 0.9

        accel = np.array(accel)

        total_accel = accel + self.adaptive_accel
        self.current_moment = total_accel * self.get_j() + self.get_r()
        corrected = (self.current_moment - self.get_r(delta=True)) / self.get_j(delta=True)
        if not prediction:
            self.adaptive_accel = self.adaptive_accel + (accel - corrected)
        return corrected.tolist()

    def set_goal(self, coordinates: list):
        self.goal = np.array(coordinates)

    def get_goal(self, scaled: bool = False):
        return self.goal.copy() / (np.sum(self.length) if scaled else 1)

    def loss(self):
        point = np.sum(self.get_coord(), axis=0)
        mean_l = np.mean(self.length)
        if self.goal is None:
            return 0
        elif np.sum(np.power(np.abs(self.goal - point), 2)) < self.goal_delta:
            return 0
        else:
            distance_loss = np.sum(np.power(np.abs(self.goal - point), 2))
            speed_loss = (
                mean_l**3 * (np.sum(np.abs(self.speed / self.accel_limit)))
                / (np.sum(np.power(np.abs(self.goal - point), 2))**0.5 + mean_l)
            )
            scale_k = 1 / np.sum(np.power(self.length, 2))
            if (np.abs(self.speed) < self.accel_limit * 4).all():
                return (
                    distance_loss
                    * scale_k
                )
            else:
                return (
                    (distance_loss + speed_loss)
                    * scale_k
                )

    def make_step(self, accel: list, prediction: bool = False, disable_direction: bool = False):
        accel = np.array(accel)
        if self.loss() == 0:
            if np.sum(self.speed) == 0:
                return 0
            else:
                for i in range(len(self.speed)):
                    if self.speed[i] > self.accel_limit[i]:
                        self.accel[i] = self.accel_limit[i] * (-1 if self.speed[i] > 0 else 1)
                    else:
                        self.accel[i] = -1 * self.speed[i]
        else:
            self.accel = np.array(accel)
            for i in range(len(self.accel)):
                if self.accel[i] > self.accel_limit[i]:
                    self.accel[i] = self.accel_limit[i]
                elif self.accel[i] < (-1 * self.accel_limit[i]):
                    self.accel[i] = -1 * self.accel_limit[i]

        self.accel = self.get_correct_accel(accel, prediction, disable_direction)
        self.speed += self.accel
        self.angle += self.speed
        loss = self.loss()
        if prediction:
            self.angle -= self.speed
            self.speed -= self.accel
        else:
            energy_per_step = np.sum(np.abs(self.current_moment * self.speed))
            self.energy_lost += energy_per_step if energy_per_step > 0 else 0
        return loss

    def predict_step(self, accel: list):
        buff = self.accel
        prediction_loss = self.make_step(accel, prediction=True)
        self.accel = buff
        return prediction_loss

    def get_config(self):
        result = []
        vectors = self.get_coord(scaled=True)
        for vector in vectors:
            for part in vector:
                result.append(part)
        return [
            *result,
            *(self.speed / self.accel_limit),
            *(self.get_goal(scaled=True)),
        ]
