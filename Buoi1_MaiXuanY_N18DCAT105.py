import random

def vietfile():
    infile = open("solieu.txt", 'w')
    k = int(input("Nhap So Dong La So Nguyen Duong: "))
    while k<=0:
        k = int(input("Nhap So Dong La So Nguyen Duong: "))
    array = []
    for i in range(k):
        soLuong = random.randint(1,9)
        dsRandom = ' '.join(["%s"%random.randint(0,99) for _ in range(soLuong)])
        array.append(dsRandom)
    infile.write('\n'.join(array))
    print("Done.")

def xuli():
    infile = open("solieu.txt",'r').read()
    outfile = open("linetotal.txt",'w')
    array = []
    for row in infile.split('\n'):
        parseList = [int(number) for number in row.split(' ')]
        nSum = sum(parseList)
        array.append(str(nSum))
    outfile.write('\n'.join(array))
    outfile.close()
    print("Viet File Thanh Cong")

if __name__ == "__main__":
    vietfile()
    xuli()