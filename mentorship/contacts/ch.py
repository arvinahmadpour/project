import re



def checkmail(self):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

email = input()
if checkmail(email) is not None:
    print(checkmail(email))
else:
    print('error')