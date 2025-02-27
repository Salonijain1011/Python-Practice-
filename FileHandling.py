# #Write into file
f = open('example.txt','w')
f.write("Hello")
f.close()


# # #Read a file
f = open('example.txt','r')
content = f.read()
print(content)
f.close()


# #Append 
f = open('example.txt','a')
f.write("World")
f.close()


                        
