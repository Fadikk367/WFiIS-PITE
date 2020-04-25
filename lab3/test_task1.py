
# Take your partners improved solution to task_1
# And make 10 tests with unittest
# Your code should be runnable as:
# "python -m unittest test_task1"
# If there is not enough code to make 10 tests,
# or the code can't be tested you need to alter the solution,
# so that it would be possible to test it.
# How to get your partners solution:
#  1. go to your own solution on github
#  2. go the adress bar in the browser
#  4. change your username, to your partners username
#  5. enjoy the easy and cheerful task of working with someone's else code
#  6. There is no point 3
#
# On your own, you need to copy his code into this repository!!!
# Remember to include it while commiting.
#
# Fill the data here in the comments
#
# I am using solution by {jblaszka}
# from the commit {638e0fba327a6ff4eefd39685d1af6bb4d5c8737}  
# WARNING --- inside methods I have changed some prints into return statements in order to have wider field for writing tests

import unittest

#from bank import Bank, Account, Account2
import bank

class TestBank(unittest.TestCase):
    
    def setUp(self):
        self.id1 = '001'
        self.id2 = '002'

        self.base = bank.Account.base(self.id1, 2000)

        bank.Bank.create(self.base, self.id2, 1000)


    def tearDown(self):
        del self.base

    def test_create(self):
        bank.Bank.create(self.base, 'test_id', 999)

        self.assertEqual(self.base['test_id'], 999)

    def test_withdraw(self):
        bank.Bank.withdraw(self.base, self.id1, 1000)

        self.assertEqual(self.base[self.id1], 1000)


    def test_too_big_withdraw_try(self):
        msg = bank.Bank.withdraw(self.base, self.id1, 100000)

        self.assertEqual(msg, 'You do not have enough funds in your account.')


    def test_deposit(self):
        bank.Bank.deposit(self.base, self.id1, 5000)

        self.assertEqual(self.base[self.id1], 7000)


    def test_deposit_with_invalid_id(self):
        msg = bank.Bank.deposit(self.base, 'df534', 5000)

        self.assertEqual(msg, 'You must first create an account.')


    def test_withdraw_with_invalid_id(self):
        msg = bank.Bank.withdraw(self.base, '93434343', 5000)

        self.assertEqual(msg, 'You must first create an account.')


    def test_transfer(self):
        bank.Bank.transfer(self.base, self.id1, self.id2, 500)

        self.assertEqual(self.base[self.id1], 1500)     
        self.assertEqual(self.base[self.id2], 1500)

    def test_too_big_transfer(self):
        msg = bank.Bank.transfer(self.base, self.id1, self.id2, 40000)

        self.assertEqual(msg, 'You do not have enough funds in your account. ')   

    def test_invalid_id(self):
        msg = bank.Bank.transfer(self.base, '66asd', self.id2, 40000)

        self.assertEqual(msg, 'Check that you have entered correct details')   



class Account(unittest.TestCase):
    
    def setUp(self):
        self.id = '001'
        self.acc = bank.Account.base(self.id, 2000)


    def tearDown(self):
        del self.acc

    def test_creating_account(self):
        self.assertEqual(self.acc[self.id], 2000)


if __name__ == "__main__":
    unittest.main()
    

    

    
