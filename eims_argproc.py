import copy
import pprint
import typing

from prettytable import PrettyTable

import eims_struct
import lexer
import manager

mng = manager.EmployeeManager()


def einfo2list(einfo: eims_struct.EmployeeInfo):
    return list(vars(einfo).values())


def prettyprinttable(d:
typing.Union[
    typing.List,
    eims_struct.EmployeeInfo
]):
    table_header = [str(k) for k in lexer.EmployeeInfoAttr]
    pt = PrettyTable(table_header)

    if isinstance(d, list):
        # 两种情况：[int, einfo结构体] 或 [int, einfo list展开]
        if len(d) == 0:
            pass
        elif isinstance(d[0][1], eims_struct.EmployeeInfo):
            for item in d:
                pt.add_row([item[0]] + einfo2list(item[1]))
        else:
            pt.add_rows(d)

    elif isinstance(d, eims_struct.EmployeeInfo):
        pt = PrettyTable(table_header[1:])
        pt.add_row(vars(d).values())

    else:
        print('无法解析下面的数据结构：')
        pprint.pp(d)
        return

    print(pt)


def show(args):
    result = list()

    if args.filter:
        eids = mng.filter(args.filter)
        for eid in eids:
            result.append([eid] + einfo2list(mng.get_by_eid(eid)))
    else:
        for k, v in mng.dmd.items():
            result.append([k] + einfo2list(v))

    # 默认升序排列
    sort_key = args.ascending or args.descending
    sort_reverse = args.ascending is None
    if sort_key:
        lcommand_type = lexer.check_lcommand(sort_key)
        if lcommand_type is None:
            raise ValueError(f"排序 {sort_key} 方式不受支持！")

        result.sort(key=lambda x: x[lcommand_type.value], reverse=sort_reverse)

    prettyprinttable(result)


def sign(args):
    print(args)
    new_eid = mng.append(
        eims_struct.EmployeeInfo(
            args.name, args.sex, args.age, args.education, args.wage, args.address, args.phone
        )
    )
    if not args.quiet:
        prettyprinttable(mng.get_by_eid(new_eid))


def modify(args):
    einfo = copy.copy(mng.get_by_eid(args.eid))

    if not args.quiet:
        print('Original: ')
        prettyprinttable(einfo)

    for item in lexer.EmployeeInfoAttr:

        if item is lexer.EmployeeInfoAttr.eid:
            continue
        elif item is lexer.EmployeeInfoAttr.ename:
            attr = 'name'
        else:
            attr = item.name

        new_value = eval(f"args.{attr}")
        if new_value:
            exec(f"einfo.{attr} = new_value")

    mng.modify(args.eid, einfo)
    if not args.quiet:
        print('Present: ')
        prettyprinttable(einfo)


def resign(args):
    if not args.quiet:
        print('Remove:')
        prettyprinttable(mng.get_by_eid(args.eid))

    mng.remove(args.eid)
