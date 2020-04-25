class Account:
    def base(ID_Number, cash):
        base = {}
        base[ID_Number] = cash
        return (base)

class Account2():
    def base2(ID_Number, cash):
        base2 = {}
        base2[ID_Number] = cash
        return (base2)

class Bank():
    def create(base, ID_Number, cash):
        base[ID_Number] = cash
        return (base)

    def withdraw(base, ID_Number, withdraw):
            if ID_Number in base:
                if withdraw > base[ID_Number]:
                    return 'You do not have enough funds in your account.'
                else:
                    base[ID_Number] -= withdraw
                    return (base)
            else: return 'You must first create an account.'

    def deposit(base, ID_Number, deposit):
            if ID_Number in base:
                base[ID_Number] += deposit
                return (base)
            else:  return 'You must first create an account.'

    def transfer(base, ID_Number, ID_Number2, transfer):
        if ID_Number and ID_Number in base:
            if transfer > base[ID_Number]:
                return 'You do not have enough funds in your account. '
            else:
                    base[ID_Number] -= transfer
                    base[ID_Number2] += transfer
                    return (base)
        else: return 'Check that you have entered correct details'

    def print(base, ID_Number):
        if ID_Number and ID_Number in base:
            print(base[ID_Number])


if __name__ == '__main__':
    base = Account.base('123456789',1000)
    print(Bank.create(base, '147258369', 5000))
    print(Bank.create(base,'741852963',750))
    print(Bank.transfer(base,'147258369','123456789',50))
    print(Bank.withdraw(base, '123456789',50))
    print(Bank.deposit(base,'123456789',500))
    Bank.print(base,'123456789')