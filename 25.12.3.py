M=2.9
count=0
while count<3:
    N=input("Enter number:")#while语句
    try:
        A=M*float(N)
        print(round(A,4))
        count+=1
    except ValueError:
        print("Please enter a number!")