from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (
            f"Тип тренировки: {self.training_type};"
            f" Длительность: {self.duration:.3f} ч.;"
            f" Дистанция: {self.distance:.3f} км;"
            f" Ср. скорость: {self.speed:.3f} км/ч;"
            f" Потрачено ккал: {self.calories:.3f}."
        )


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000.00
    MIN_IN_HOUR: ClassVar[float] = 60.00

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            "Определите метод get_spent_calories"
            " в %s." % (self.__class__.__name__)
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    RUN_COEFF_CALORIE_1: ClassVar[float] = 18
    RUN_COEFF_CALORIE_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        return (
            (
                self.RUN_COEFF_CALORIE_1 * self.get_mean_speed()
                - self.RUN_COEFF_CALORIE_2
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    WLK_COEFF_CALORIE_1: ClassVar[float] = 0.035
    WLK_COEFF_CALORIE_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        return (
            (
                self.WLK_COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WLK_COEFF_CALORIE_2
                * self.weight
            )
            * self.duration
            * self.MIN_IN_HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    weight: float
    length_pool: float
    count_pool: float
    SWM_COEFF_CALORIE_1: ClassVar[float] = 1.1
    SWM_COEFF_CALORIE_2: ClassVar[float] = 2.0
    LEN_STEP: ClassVar[float] = 1.38

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.SWM_COEFF_CALORIE_1)
            * self.SWM_COEFF_CALORIE_2
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_workout_type = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    kls = dict_workout_type.get(workout_type)
    if kls is None:
        kls = Training
        raise NameError(
            f"Функция read_package - Тип тренировки {workout_type}:"
            "отсутствует в справочнике dict_workout_type"
        )
    return kls(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
