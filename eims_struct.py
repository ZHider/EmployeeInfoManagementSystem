from dataclasses import dataclass
from enum import Enum
import decimal


class Gender(Enum):
    male = 0
    female = 1
    other = 2

    def __str__(self):
        return ('男', '女', '其他')[self.value]


class Education(Enum):
    none = 0
    primary = 1
    junior_high = 2
    senior_high = 3
    bachelor = 4
    master = 5
    doctor = 6
    other = 7

    def __str__(self):
        return ('文盲', '小学', '初中', '高中', '学士', '硕士', '博士')[self.value]


@dataclass
class EmployeeInfo:
    name: str
    sex: Gender
    age: int
    education: Education
    wage: decimal.Decimal
    address: str
    phone: str


