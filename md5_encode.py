import hashlib
    
m2 = hashlib.md5()

while True:
    str_in = input()
    m2.update(str(str_in).encode('ANSI'))
    print(str_in,'+',m2.hexdigest())