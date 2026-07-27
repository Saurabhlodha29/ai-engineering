class BankAccount:
    def __init__(self,first,last,balance = 0):
        self.first = first
        self.last = last
        self.balance = balance
        
    def deposit(self,amount):
        self.balance += amount
        return 'Deposited = {}, Total = {}'.format(amount,self.balance)
    
    def withdraw(self,amount):
        self.balance -= amount
        return 'Withdrawn = {}, Total = {}'.format(amount,self.balance)
    
    def get_balance(self):
        return "Balance = {}".format(self.balance)
    
    def __repr__(self):
        return f"Bank Account : Name = {self.first} {self.last}, Balance = {self.get_balance()}"
    
user1 = BankAccount("Bruce","Wayne")
print(user1.deposit(5000))
print(user1.withdraw(1900))
print(user1.get_balance())
print(user1.__repr__())
    
    