import sys

class calculator:
    def add(self, x, y):
        return x + y

    def increment(self, x):
        x += 1;
        return x;

#creating object of class
calculatorObj = calculator()
#capturing input from command line and casting to integer
z = calculatorObj.add(1, 2)
#printing result on console
print(z)
sys.stdout.flush()
