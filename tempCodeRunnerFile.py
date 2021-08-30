hashids = Hashids(salt='This is my salt')  # saltにsalt値を指定
id = hashids.encode(randint(0, 1267650600228229401496703205376))

print('Hash: ' + id)