import typing
from decimal import Decimal
from enum import Enum

import eims_struct

EInfoTypes = typing.Union[str, int, Decimal, eims_struct.Gender, eims_struct.Education]


class OperatorType(Enum):
    eq = 0
    ne = 1
    gt = 2
    ge = 3
    lt = 4
    le = 5

    def __len__(self):
        return (2, 2, 1, 2, 1, 2)[self.value]


class EmployeeInfoAttr(Enum):
    eid = 0
    ename = 1
    sex = 2
    age = 3
    education = 4
    wage = 5
    address = 6
    phone = 7

    def __str__(self):
        return ('EID', '姓名', '性别', '年龄', '学历', '薪资', '地址', '电话')[self.value]

    def get_name(self):
        """请使用此方法代替 EmployeeInfoAttr.name 以和 EmployeeInfo 保持名称兼容"""
        return self.name if self is not EmployeeInfoAttr.ename else 'name'


def check_lcommand(command: str) -> typing.Union[EmployeeInfoAttr, None]:
    """判断符号左侧符合规定返回枚举，否则返回None"""
    for einfo_type in EmployeeInfoAttr:
        if command.find(einfo_type.get_name()) == 0:
            return einfo_type
    return None


def check_operator(command: str, rtype: EmployeeInfoAttr) -> typing.Union[OperatorType, None]:
    """检测中间符号是否在允许的范围内，成功返回符号类型，否则返回None"""

    rlen = len(rtype.get_name())

    result = {
        '==': OperatorType.eq,
        '!=': OperatorType.ne,
        '>=': OperatorType.ge,
        '<=': OperatorType.le
    }.get(command[rlen: rlen + 2], None)

    if result is None:
        result = {
            '>': OperatorType.gt,
            '<': OperatorType.lt
        }.get(command[rlen], None)

    return result


def parse_exp(eid: int, einfo: eims_struct.EmployeeInfo,
              filter: str, attr: EmployeeInfoAttr, op: OperatorType) -> (EInfoTypes, EInfoTypes):
    """将一个filter exp的左边转换成相应einfo的对象，右边规范成相应对象以便相互比较"""

    attr_name = attr.get_name()

    # 默认rcommand是在filter exp中取的右边值
    rcommand = filter[len(attr_name) + len(op):]

    try:
        # lcommand 默认值是eid。若非判断eid，就再在einfo里取。
        lcommand = eid
        if attr is EmployeeInfoAttr.eid:
            rcommand = int(rcommand)
        else:
            lcommand = einfo.__dict__[attr_name]

            if attr is EmployeeInfoAttr.sex:
                rcommand = eims_struct.Gender(int(rcommand))
            elif attr is EmployeeInfoAttr.age:
                rcommand = int(rcommand)
            elif attr is EmployeeInfoAttr.education:
                # 使education可比较
                lcommand = lcommand.value
                # rcommand = eims_struct.Education(int(rcommand))
                rcommand = int(rcommand)
            elif attr is EmployeeInfoAttr.wage:
                rcommand = Decimal(rcommand)

    except ValueError as e:
        raise ValueError(f'filter "{filter}" 不合法！\n错误信息：{e}')

    if attr in (EmployeeInfoAttr.sex, EmployeeInfoAttr.address, EmployeeInfoAttr.phone) \
            and op not in (OperatorType.eq, OperatorType.ne):
        raise ValueError(f"{attr} 不支持 {op} 操作！")

    return lcommand, rcommand


def evalop(lcommand, op: OperatorType, rcommand) -> bool:
    if op is OperatorType.eq:
        return lcommand == rcommand
    elif op is OperatorType.ge:
        return lcommand >= rcommand
    elif op is OperatorType.le:
        return lcommand <= rcommand
    elif op is OperatorType.gt:
        return lcommand > rcommand
    elif op is OperatorType.lt:
        return lcommand < rcommand
    elif op is OperatorType.ne:
        return lcommand != rcommand
    else:
        raise ValueError(f"{op} 操作符不支持！")
