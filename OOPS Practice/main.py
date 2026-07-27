class Employee:
    
    def __init__(self,first,last):   #Constructor for default values to give each instance
        self.first = first
        self.last = last
        
    @property
    def email(self):
        return f'{self.first}.{self.last}@email.com'
    
    @property 
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    
    @fullname.setter
    def fullname(self,name):
        first,last = name.split(' ')
        self.first = first
        self.last = last
        
    @fullname.deleter
    def fullname(self):
        print("Deleted Name!")
        self.first = None
        self.last = None
    
    
    
emp1 = Employee('Tom', 'Hardy')
emp2 = Employee('Johnny', 'Depp')

print(emp1.email)
emp1.fullname = 'Tom Holland'
print(emp1.email)

del emp1.fullname