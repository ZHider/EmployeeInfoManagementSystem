import decimal
import os
import pickle
import typing
import zlib

import lexer
import eims_struct

SAVE_FILE_PATH = "ei.db"
DEFAULT_EMPLOYEE = eims_struct.EmployeeInfo(
    'Template Employee', eims_struct.Gender.other,
    200, eims_struct.Education.bachelor, decimal.Decimal(5000),
    "Atlantis", "+8615888888888"
)


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class DictManager:

    def __init__(self, path: str):
        """
        新建一个ListManager，path为文件加载路径
        :param path: pickle文件的路径
        """

        self.dict = dict()
        self.path = path

    def load(self):
        """加载一个pickle文件"""

        with open(self.path, 'rb') as f:
            decompressed = zlib.decompress(f.read())
            self.dict = pickle.loads(decompressed)

        return self

    def save(self):
        """保存list到文件"""

        with open(self.path, 'wb') as f:
            not_compressed = pickle.dumps(self.dict)
            f.write(zlib.compress(not_compressed))


        return self


class EmployeeManager(Singleton):

    def __init__(self):

        self.dm = DictManager(SAVE_FILE_PATH)
        self.dmd: typing.Dict[int, eims_struct.EmployeeInfo] = self.dm.dict

        if os.path.exists(self.dm.path):
            self.dm.load()
            self.dmd: typing.Dict[int, eims_struct.EmployeeInfo] = self.dm.dict
        else:
            # 没有文件时的初始化操作
            # self.dmd[0] = DEFAULT_EMPLOYEE
            self.dm.save()

    def check_eid_exists(self, eid):
        return eid in self.dmd.keys()

    def _raise_if_no_eid(self, eid):
        if not self.check_eid_exists(eid):
            raise ValueError(f"EID {eid} 不存在！")

    def append(self, employee_info: eims_struct.EmployeeInfo) -> int:
        """增加一个员工信息，返回新的eid"""

        def get_new_eid():
            # 获取到最后一个key
            it = self.dmd.keys()
            last_key = 0
            for last_key in it:
                # 所有key必定是整数
                assert isinstance(last_key, int)
                pass
            return last_key + 1

        new_eid = get_new_eid()
        self.dmd[new_eid] = employee_info

        self.dm.save()

        return new_eid

    def remove(self, eid: int):
        self._raise_if_no_eid(eid)
        del self.dmd[eid]
        self.dm.save()

    def modify(self, eid: int, new_einfo: eims_struct.EmployeeInfo):
        self._raise_if_no_eid(eid)
        self.dmd[eid] = new_einfo
        self.dm.save()

    def get_by_eid(self, eid: int) -> eims_struct.EmployeeInfo:
        self._raise_if_no_eid(eid)
        if not isinstance(eid, int):
            raise ValueError("eid should be int")
        return self.dmd[eid]

    def filter(self, expression: str) -> typing.List[int]:
        """
        根据条件过滤列表
        :param expression: 支持==|>=|<=,以逗号分割
        :return: 返回符合条件的eid列表
        """

        result: typing.List[int] = list()
        commands = expression.split(',')
        for eid, einfo in self.dmd.items():
            eid: int
            einfo: eims_struct.EmployeeInfo.__dict__

            append_to_result = True

            for command in commands:

                lcommand_type = lexer.check_lcommand(command)
                if not lcommand_type:
                    raise ValueError(f"命令不在可选范围内：{command}")

                op = lexer.check_operator(command, lcommand_type)
                if not op:
                    raise ValueError(f"操作符不合法：{command}")

                lcommand, rcommand = lexer.parse_exp(eid, einfo, command, lcommand_type, op)
                append_to_result &= lexer.evalop(lcommand, op, rcommand)

            if append_to_result:
                result.append(eid)

        return result
