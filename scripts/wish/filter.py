import re

def filter(filep="products/products.csv",out_filep="products/products.csv.new"):
    #pattern = '(?!)'
    f = open(filep,'r')
    out_file = open(out_filep,'w')
    #pattern = re.compile('((.*\5){17}(?!\5)*)')
    pattern = re.compile('((.*\5){17}[^\5]*)')
    i = 0
    for line in f:
        result = pattern.match(line)
        if not result:
            i = i + 1
            print line
        else:
            out_file.write(line)

    f.close()
    out_file.close()
    return i

if __name__ == "__main__":
    print filter()
