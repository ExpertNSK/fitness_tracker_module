class InfoMessage:
    """Класс сообщения."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_H = 60  # Кол-во минут в часе
    CM_IN_M = 100  # Кол-во см в метре
    KM_H_IN_M_S_COEFF = 3.6  # Коеффициент для перевода км/ч в м/с
    LEN_STEP = 0.65  # Длинна шага
    M_IN_KM = 1000  # Кол-во метров в километре
    S_IN_H = 60  # Кол-во секунд в часе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Возвращает дистанцию в километрах."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Возвращает количество сожженых килокалорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Возвращает объект сообщения."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Класс тренировки типа Бег."""
    # Коэффициенты для вычисления калорий
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Переопределяем формулу каллорий для данного типа тренировки."""
        duration_in_m = self.duration * self.M_IN_H
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * duration_in_m)


class SportsWalking(Training):
    """Класс тренировки типа Спортивная ходьба."""
    # Коэффициенты для вычисления калорий
    WALKING_TYPE_COEFF = 0.035
    SPEED_ON_HEIGHT_COEEF = 0.029

    def __init__(
            self, action: int,
            duration: float,
            weight: float,
            height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Переопределяем формулу каллорий для данного типа тренировки."""
        mean_speed_m_s = self.get_mean_speed() / self.KM_H_IN_M_S_COEFF
        height_in_m = self.height / self.CM_IN_M
        duration_in_m = self.duration * self.M_IN_H
        return ((self.WALKING_TYPE_COEFF * self.weight
                + (mean_speed_m_s**2 / height_in_m)
                * self.SPEED_ON_HEIGHT_COEEF * self.weight)
                * duration_in_m)


class Swimming(Training):
    """Класс тренировки типа Плавание."""
    LEN_STEP = 1.38  # Длинна гребка

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопределяем формулу средней скорости для плавания."""
        return (self.length_pool * self.count_pool /
                self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Переопределяем формулу каллорий для данного типа тренировки."""
        return ((self.get_mean_speed() + 1.1) * 2 *
                self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    training_type: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    return training_type[workout_type](*data)


def main(trainig: Training) -> None:
    msg_obj = trainig.show_training_info()
    info = msg_obj.get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [420, 4, 20]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
