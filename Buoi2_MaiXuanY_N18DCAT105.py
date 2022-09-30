def findIPinFile():
    infile = open('ip.txt', 'r')
    textFile = infile.read()
    listText = textFile.split('\n')
    ip = input("Nhap IP: ")
    temp = ''
    for i, text in enumerate(listText, start=1):
        temp+=text
        if(temp.find(ip)!=-1):
            print(i)
            temp=''


if __name__ == "__main__":
    findIPinFile()
