from array import *
#array values from user
n=int(input("enter number of values in array: "))
vals = array('i',[])
for i in range (n):
    x = int(input("enter values"))
    vals.append(x)
vals.extend([11,22])
print(vals)
f=int(input("enter the element to be found:"))
for i in range(len(vals)):
    if f==vals[i]:
        print ("element found")
        break
else:
    print ("element not found")
# another way of finding element:
print ("another way")
for e in vals:
    if f==e:
        print("element found")
        break
else:
    print("element not found")
# printing index of array element:
print ("index of element: ", vals.index(f))
#general declarations
arr = array('i',[5,222,2,2,22,22,3])
print(arr)
arr.reverse()
print(arr)
# prints address & count of elements in array
print (arr.buffer_info())
# copying an array
newarr = (arr.typecode, [a*a for a in arr])
print (newarr)
for e in newarr:
    print (e)
print ("--end--")
# various ways of looping arrays #3, for loop variation:
for e in arr:
    print (e)
# various ways of looping arrays #2, using while loop:
i=0
print ("while loop")
while i < len(arr):
    print (arr[i])
    i+=1
# various ways of looping arrays #1, using for loop:
print ("for loop")
for i in range(len(arr)):
    print (arr[i])
