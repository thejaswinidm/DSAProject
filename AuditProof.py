import os
from HashFunction import *

data=input('Enter data to be validated')
#data = str(data)
        
data = str(data)

#data='try1.txt'
if os.path.isfile(data):
    t = open(data, 'rb')
    temp1 = ''
    while True:
        d = t.read(8192)
        if not d:
            break
        #d=str(d)
        #print(d)
        temp=hash_fun_hex_str(hash_fun(d))
        temp1=hash_update(temp1,temp)
    t.close()
        # Otherwise it could be either 1) a directory 2) miscellaneous data (like json)
else:
    data2=bytes(data,"utf-8")
    temp1=hash_fun_hex_str(hash_fun(data2))

actual_hash=temp1
root_hash=input('Enter the root hash')

f = open('proof_to_user1.txt', 'r+')
f1=open('proof.txt','w')
count=1
for line in f.readlines():
    if(count%2==1):
        #print(line)
        line=line.strip('\n')
        if(line=='1'):
            #print('hello')
            flag=1
        else:
            flag=2
    if(count%2==0):
        #line1=bytes(line,"utf-8")
        test_hash=line.strip('\n')
        if(flag==1):
            temp_str=test_hash+'   +   '+actual_hash+'   =   '
            #print('test hash=',end=' ')
            #print(test_hash)
            actual_hash=test_hash+actual_hash
            
            
            actual_hash1=bytes(actual_hash,"utf-8")
            actual_hash=hash_fun_hex_str(hash_fun(actual_hash1))
            #print(actual_hash)
            temp_str=temp_str+actual_hash
            f1.write(temp_str+'\n')
        else:
            temp_str=actual_hash+'   +   '+test_hash+'   =   '
            actual_hash=actual_hash+test_hash
            actual_hash1=bytes(actual_hash,"utf-8")
            actual_hash=hash_fun_hex_str(hash_fun(actual_hash1))
            temp_str=temp_str+actual_hash
            #print(actual_hash)
            f1.write(temp_str+'\n')
    count=count+1
final_hash=actual_hash
print('The final hash is: ', end  = ' ')
print(final_hash)
print('The root hash is: ', end  = ' ')
print(root_hash)
if(actual_hash==root_hash):
    print("The data searched for is present in the Data Set")
    print("See proof in proof.txt")
else:
    print("The data searched for is not present in the Data Set")

f.close()
f1.close()
