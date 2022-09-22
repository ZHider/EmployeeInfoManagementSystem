import unittest

import lexer
import eims_struct


class MyTestCase(unittest.TestCase):
    def test_lexer_lcommand(self):
        self.assertEqual(lexer.check_lcommand('eid'), lexer.EmployeeInfoAttr.eid)
        self.assertEqual(lexer.check_lcommand('name=Bob'), lexer.EmployeeInfoAttr.ename)
        self.assertEqual(lexer.check_lcommand('phone==123'), lexer.EmployeeInfoAttr.phone)

        self.assertEqual(lexer.check_lcommand('ename==Bob'), None)
        self.assertEqual(lexer.check_lcommand('telegram'), None)
        self.assertEqual(lexer.check_lcommand('ssex'), None)
        self.assertEqual(lexer.check_lcommand('aage'), None)

    def test_lexer_op(self):
        self.assertEqual(lexer.check_operator('name==Bob', lexer.EmployeeInfoAttr.ename), lexer.OperatorType.eq)


if __name__ == '__main__':
    unittest.main()
