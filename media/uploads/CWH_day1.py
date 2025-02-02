# a = int(input("Enter your age : "))
# print("age :" ,a)

# if (a>20):
#  print("You can drive")
# elif(a>18):
#  print("You cannnn drive")
# else:
#     print("You cannot drive")

import time
timestamp = time.strftime('%H:%M:%S')
print("time : ",timestamp)
hour = int(time.strftime('%H'))
if(hour > 6 and hour <=12 ):
    print("Good morning")
elif(hour >12 and hour < 18):
    print("Good Afternoon")
elif(hour>=18 and hour < 23):
    print("Good Evening") 
else:
    print("Good Night")           
# print(timestamp)
# timestamp = time.strftime('%M')
# print(timestamp)
# timestamp = time.strftime('%S')
# print(timestamp)