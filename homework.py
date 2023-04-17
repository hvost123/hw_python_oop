

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.distance = distance
        self.duration = duration
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        rez: str = (f'Тип тренировки: {self.training_type}; '
                    f'Длительность: {self.duration:.3f} ч.; '
                    f'Дистанция: {self.distance:.3f} км; '
                    f'Ср. скорость: {self.speed:.3f} км/ч; '
                    f'Потрачено ккал: {self.calories:.3f}.')
        return rez


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    H_IN_MIN: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__,
                          self.duration,
                          self.get_distance(),
                          self.get_mean_speed(),
                          self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight,)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.get_mean_speed()
                    + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM
                    * (self.duration * self.H_IN_MIN))
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    INDEX_1: float = 0.035
    INDEX_2: float = 0.029
    KMH_IN_MS: float = 0.278
    SM_M = 100

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight,)
        self.height = height

    def get_mean_speed(self) -> float:
        speed: float = self.get_distance() / self.duration * self.KMH_IN_MS
        return speed

    def get_spent_calories(self) -> float:
        calories = (((self.INDEX_1 * self.weight
                    + (self.get_mean_speed()**2 / (self.height / self.SM_M))
                    * self.INDEX_2 * self.weight) * self.duration
                    * self.H_IN_MIN))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    INDEX_1: float = 1.1
    INDEX_2: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight,)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        speed = (self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration)
        return speed

    def get_distance(self) -> float:
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.INDEX_1) * self.INDEX_2
                    * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    parameters_train = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    if workout_type in parameters_train:
        return parameters_train[workout_type](*data)
    else:
        raise ValueError("Тренировка не найдена")


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    return print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
