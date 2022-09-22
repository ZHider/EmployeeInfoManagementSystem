import argparse
import decimal

import eims_struct
import eims_argproc

FILTER_HELP = """
使用过滤器进行筛选。
    示例：
        %(prog)s -f age<30,wage>10000
        表示筛选出年龄小于30，薪资大于10000的员工。
    每个筛选以半角逗号分隔，每条筛选间为AND关系。
"""


def type_gen(type):
    def type_x(x):
        return type(int(x))

    return type_x


type_gender = type_gen(eims_struct.Gender)
type_education = type_gen(eims_struct.Education)

# create the top-level parser
parser = argparse.ArgumentParser(prog='EIMS', description="Employee Information Management System")
sub_parser = parser.add_subparsers(title='command', description='支持的命令')

# create the parser for the "show" command
show_parser = sub_parser.add_parser('show', help='显示成员信息')
show_parser.add_argument('--filter', '-f',
                         help=FILTER_HELP)
sort_parser = show_parser.add_mutually_exclusive_group()
sort_parser.add_argument('--ascending', '-a', help='升序排列', metavar='column')
sort_parser.add_argument('--descending', '-d', help='降序排列', metavar='column')
sort_parser.set_defaults(func=eims_argproc.show)

# create the parser for the "sign" command
sign_parser = sub_parser.add_parser('sign', help='登记新雇员信息')
sign_parser.add_argument('name', help='员工名称')
sign_parser.add_argument('sex', help='员工性别  0：男性，1：女性，2：其他',
                         type=type_gender)
sign_parser.add_argument('age', help='员工年龄', type=int)
sign_parser.add_argument('education', help='员工教育程度\n'
                                           '0：文盲，1：小学，2：初中，3：高中，4：学士，5：硕士，6：博士，7：其他',
                         type=type_education)
sign_parser.add_argument('wage', help='员工工资', type=decimal.Decimal)
sign_parser.add_argument('address', help='员工地址')
sign_parser.add_argument('phone', help='员工电话号')
sign_parser.add_argument('--quiet', '-q', help='静默模式', action='store_true')
sign_parser.set_defaults(func=eims_argproc.sign)

# create the parser for the "modify" command
modify_parser = sub_parser.add_parser('modify', help='修改雇员信息')
modify_parser.add_argument('eid', help='要修改员工的eid', type=int)
modify_parser.add_argument('--name', '-n', help='员工名称')
modify_parser.add_argument('--sex', '-s', help='员工性别  0：男性，1：女性，2：其他',
                           type=type_gender)
modify_parser.add_argument('--age', '-a', help='员工年龄', type=int)
modify_parser.add_argument('--education', '-e', help="员工教育程度\n"
                                                     "0：文盲，1：小学，2：初中，3：高中，4：学士，"
                                                     "5：硕士，6：博士，7：其他",
                           type=type_education)
modify_parser.add_argument('--wage', '-w', help='员工工资', type=decimal.Decimal)
modify_parser.add_argument('--address', '-A', help='员工地址')
modify_parser.add_argument('--phone', '-p', help='员工电话号')
modify_parser.add_argument('--quiet', '-q', help='静默模式', action='store_true')
modify_parser.set_defaults(func=eims_argproc.modify)

# create the parser for the "resign" command
resign_parser = sub_parser.add_parser('resign', help='从系统中移除雇员信息')
resign_parser.add_argument('eid', help='要移除的员工eid', type=int)
resign_parser.add_argument('--quiet', '-q', help='静默模式', action='store_true')
resign_parser.set_defaults(func=eims_argproc.resign)


# args = parser.parse_args("show -f name==奥林其他".split())
args = parser.parse_args()
# print(args)
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
