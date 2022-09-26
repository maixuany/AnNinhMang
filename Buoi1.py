import msvcrt

def vietfile():
    infile = open("solieu.txt", 'w')
    k = int(input("Nhap So Dong La So Nguyen Duong: "))
    while k<=0:
        k = int(input("Nhap So Dong La So Nguyen Duong: "))
    for x in range(k):
        number = int(input("Nhap Chuoi So: "))
        infile.writelines(str(number)+"\n")
    print("Done")

def xuli():
    infile = open("solieu.txt",'r')
    outfile = open("linetotal.txt",'w')
    for s in infile.readlines():
        text = s.strip()
        try:
            number = int(text)
        except:
            continue
        total = 0
        while number>0:
            total = total + number%10
            number = int(number/10)
        outfile.writelines(str(total)+'\n')
    outfile.close()
    infile.close()
    print("Viet File Thanh Cong")

if __name__ == "__main__":
    vietfile()
    xuli()