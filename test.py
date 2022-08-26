a = ['page_1.csv', 'page_10.py', 'page_100.csv', 'page_101.py']

for file in a:
    print(file[-4:])
    if file[-4:] != '.csv':
        a.remove(file)

print(a)