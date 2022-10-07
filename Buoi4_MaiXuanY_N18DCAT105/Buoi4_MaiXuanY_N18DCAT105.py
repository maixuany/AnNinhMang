import mysql.connector
from mysql.connector import Error
import os
import random
import hashlib
import sys

def hash_file(filename):

   h = hashlib.md5()

   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return  h.hexdigest()


def hashFileContent(fileDic):
    if os.path.isfile(fileDic):
        # file is exist
        return hash_file(fileDic)
    else:
        # not exist or is not file
        print ("Can't open '{}' file".format(fileDic))
        exit(0)
        return False

def hashString(fileDic):
    md5_returned = hashlib.md5(str(fileDic).encode()).hexdigest()
    return md5_returned


def isDirectory(directory):
    return os.path.isdir(directory)


def insertDatabase(rootdir):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='fileManager',
                                             user='root',
                                             password='2211',
                                             auth_plugin='mysql_native_password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            #print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            #print("You're connected to database: ", record)


            # set projTD
            projID=random.randint(0,500)

            #insert root element
            filehash=hashString(rootdir)
            sql = ('INSERT INTO hash(projID,isroot, ten, namehash, isfile,contenthash) VALUES (%s,%s,%s, %s,%s, %s)')
            cursor.execute(sql, (str(projID),'1',rootdir ,filehash, '0',''))
            connection.commit()
            
            # for loop directory
            for subdir, dirs, files in os.walk(rootdir):
                #print (dirs)
                print ('Thu muc:' + subdir)
                #list = os.listdir(subdir) # dir is your directory path
                #number_files = len(list)
                #print (number_files)
                #dem=0
                filehash=hashString(subdir)
                sql = ('INSERT INTO hash(projID,isroot, ten, namehash, isfile,contenthash) VALUES (%s,%s, %s, %s,%s, %s)')
                cursor.execute(sql, (str(projID),'0',subdir ,filehash, '0',''))
                connection.commit()
                for file in files:
                    #dem+=1
                    print (os.path.join(subdir, file))
                    filename=os.path.join(subdir, file)
                    filehash=hashString(filename)
                    contenthash=hashFileContent(filename)
                    sql = ('INSERT INTO hash(projID,isroot, ten, namehash, isfile,contenthash) VALUES (%s,%s, %s, %s,%s, %s)')
                    cursor.execute(sql, (str(projID),'0',filename ,filehash, '1',contenthash))
                    connection.commit()     
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

def checkExistDir(rootdir):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='fileManager',
                                             user='root',
                                             password='2211',
                                             auth_plugin='mysql_native_password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            #print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            #print("You're connected to database: ", record)

            sql = ("SELECT * from hash where isroot='1'")
            cursor.execute(sql)
            myresult = cursor.fetchall()
            for x in myresult:
                if x[3]==rootdir:
                    return True,x[1]
            return False,-1
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def getAll(projID):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='fileManager',
                                             user='root',
                                             password='2211',
                                             auth_plugin='mysql_native_password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()

            sql = ("SELECT * from hash where projID='"+str(projID)+"'")
            cursor.execute(sql)
            myresult = cursor.fetchall()
            return myresult
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
def deleteProj(projID):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='fileManager',
                                             user='root',
                                             password='2211',
                                             auth_plugin='mysql_native_password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()

            sql = ("DELETE from hash where projID='"+str(projID)+"'")
            cursor.execute(sql)
            connection.commit()  
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def checksumDir(rootdir,projID):
    verified=True
    print ("=============CHANGE LOG=============")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='fileManager',
                                             user='root',
                                             password='2211',
                                             auth_plugin='mysql_native_password')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor(buffered=True)
            # for loop directory
            for subdir, dirs, files in os.walk(rootdir):
                filehash=hashString(subdir)
                temp=subdir.replace('\\','\\\\')
                #print (subdir)
                sql = ("SELECT * FROM hash where projID='"+str(projID)+"' and ten='"+temp+"'")
                cursor.execute(sql)
                myresult = cursor.fetchone()
                if myresult is None:
                    sumfolder=''
                else:
                    sumfolder=myresult[4]
                    targetList.pop(targetList.index(subdir))
                if sumfolder!=hashString(subdir):
                    verified=False
                    print ('  [+] New folder: '+subdir)
                for file in files:
                    #dem+=1
                    #print (os.path.join(subdir, file))
                    filename=os.path.join(subdir, file)
                    filehash=hashString(filename)
                    contenthash=hashFileContent(filename)
                    temp=filename.replace('\\','\\\\')
                    sql = ("SELECT * FROM hash where projID='"+str(projID)+"' and ten='"+temp+"'")
                    cursor.execute(sql)
                    myresult1 = cursor.fetchone()
                    #print (sql)
                    #print (myresult1)
                    if myresult1 is None:
                        sumfile=''
                        sumcontent=''
                    else:
                        sumfile=myresult1[4]
                        sumcontent=myresult1[6]
                        targetList.pop(targetList.index(filename))
                    # check filename
                    if sumfile!=hashString(filename):
                        verified=False
                        print ('  [-] New file: '+filename)
                    # check content of file
                    if sumcontent!=hashFileContent(filename):
                        verified=False
                        print ('  [-] Content change in file: '+filename)

        if targetList:
            verified=False
            for file in targetList:
                print ('  [-] File removed: '+file)
        print ('====================================')
        if verified==False:
            print ("Check successfully. MD5 verification failed!")
        else:
            print ('Check successfully. MD5 verified')
        #print (targetList)
    
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
    

rootdir=str(sys.argv[1])
command=str(sys.argv[2])


helppr="""
Example: python3 {} 'C:/abc' update 
         python3 {} 'C:/abc' checksum
""".format(sys.argv[0],sys.argv[0])

if len(rootdir)<1:
    print (helppr)
    exit(0)

if isDirectory(rootdir)==False:
    print ('Directory not exist')
    exit()


isvalid,numID=checkExistDir(rootdir)
temp=getAll(numID)
targetList=[temp[x][3] for x in range(0,len(temp))]
if targetList:
    targetList.pop(0)

if command=="checksum":
    if isvalid:
        checksumDir(rootdir,numID)
    else:
        print ("Not found")
elif command=="update":
    if isvalid:
        print (numID)
        deleteProj(numID)
        insertDatabase(rootdir)
    else:
        insertDatabase(rootdir)
else:
    print (helppr)






