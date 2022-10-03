import hashlib
import os
import sys

def hash_file(filename):

   h = hashlib.md5()

   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return  h.hexdigest()

def save_hash(path_folder):
    arr = os.listdir(path_folder)
    file = open("/home/mike/AnNinhMang/save_hash.txt",'w')
    for x in arr:
        if(x=="save_hash.txt"):
            continue
        else:
            path = path_folder+str(x)
            if(os.path.isfile(path)):
                file.write(path+","+hash_file(path)+'\n')
            else:
                file.write(path+"\n")

def check_hash(path_folder):
    arr = os.listdir(path_folder)
    file = open("/home/mike/AnNinhMang/save_hash.txt",'r')
    listText = file.read().split('\n')
    for x in arr:
        if(x=="save_hash.txt"):
            continue
        else:
            path = path_folder+str(x)
            if(os.path.isfile(path)):
                print(path+": "+str((path+","+hash_file(path)) in listText))
            else:
                print(path+": "+str((path) in listText))

def editFile(path):
    file = open(path,'w')
    file.write("Hello")

if __name__ == "__main__":
    root_path = sys.argv[1]
    if(os.path.exists(root_path)):
        save_hash(root_path)
        editFile("./ip.txt")
        check_hash(root_path)
    else:
        print('Duong Dan Sai')
