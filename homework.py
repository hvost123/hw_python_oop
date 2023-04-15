

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.distance = distance
        self.duration = duration
        self.speed = speed
        self.calories = calories

    def get_message(self):
        rez = (f'Тип тренировки: {self.training_type};'
               f'Длительность: {self.duration} ч.;'
               f'Дистанция: {self.distance} км;'
               f'Ср. скорость: {self.speed} км/ч;'
               f'Потрачено ккал: {self.calories}.')
        return rez


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: str = 1000
    LEN_STEP: float = 0.65

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
        speed = self.duration / self.get_distance()
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories = 0
        return calories

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        mas = InfoMessage(self.__class__.__name__,
                          self.duration, self.get_distance(),
                          self.get_mean_speed(),
                          self.get_spent_calories())
        return mas


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    """Тренировка: бег."""
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
                    * (self.duration / 60))
        return calories


class SportsWalking(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029

    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height,
                 ) -> None:
        super().__init__(action, duration, weight,)
        self.height = height

    def get_spent_calories(self) -> float:
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.weight
                    + (self.get_mean_speed()**2 / self.height)
                    * self.CALORIES_MEAN_SPEED_SHIFT
                    * self.weight)
                    * (self.duration / 60))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    INDEX_1 = 1.1
    INDEX_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, weight, weight,)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        speed = (self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calories = ((self.get_mean_speed() + self.INDEX_1)
                    * self.INDEX_2 * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        test = Swimming(*data)

    elif workout_type == 'RUN':
        test = Running(*data)

    elif workout_type == 'WLK':
        test = SportsWalking(*data)
    return test


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
