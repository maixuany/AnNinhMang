def findIPinFile():
    infile = open('ip.txt', 'r')
    text = infile.read()
    format_text = text.replace('\n','').strip()
    listText = format_text.split(',')
    for x in listText:
        value = x.strip()
        try:
            parts = value.split('.')
            if len(parts) == 4 and all(0 <= int(part) < 256 for part in parts):
                print(value)
        except:
            continue
    

if __name__ == "__main__":
    findIPinFile()
