a = float (input("A= "))
b = float (input("B= "))
c = float (input("C= "))
delta = b*b-a*4*c

if delta == 0:
    print("Nghiem kep: x = ", str(-b/2/a))
if delta < 0:
    print("Vo nghiem.")
if delta > 0:
    print("x1 = ", str((-b+delta**0.5)/2/a))       
    print("x2 = ", str((-b-delta**0.5)/2/a))        
     
