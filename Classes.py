class employee:
    raise_amount=1.04
    NoOfEmps=0
    def __init__(self,fname,lname,pay):
        self.fname=fname
        self.lname=lname
        self.email=fname+'.'+lname+'@company.name'
        self.pay=pay

        employee.NoOfEmps+=1

    def fullname(self):
        return '{}{}'.format(self.fname,self.lname)
    def raise_pay(self):
        self.pay=self.pay*self.raise_amount


emp1=employee('balaji','meka',100000)
emp2=employee ('Sai','meka',150000)
emp3=employee('sandhya','meka',150000)
print(employee.NoOfEmps)

# emp3.raise_amount=1.10
# emp3.raise_pay()
# print(emp3.pay)
# print(emp3.__dict__)
# print (emp2.fullname())


