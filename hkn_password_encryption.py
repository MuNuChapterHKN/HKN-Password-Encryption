import xlrd
import binascii
from Crypto.Cipher import AES
from Crypto.Hash import SHA3_512
from Crypto.Util.Padding import pad, unpad


def encrypt():
    # raccogli i dati dal foglio Excel
    # analizza la prima riga
    done = False
    while not done:
        d = input("File xlsx: ")
        workbook = xlrd.open_workbook(d)
        worksheet = workbook.sheet_by_index(0)
        first_row = []
        for col in range(worksheet.ncols):
            first_row.append(worksheet.cell_value(0, col))
        if  'Sito' not in first_row or 'Username' not in first_row or 'Password' not in first_row:
            print('Nella prima riga devono essere presenti "Sito", "Username" e "Password"')
        else:
            done = True
    # crea un dizionario per ogni riga di dati
    data = []
    for row in range(1, worksheet.nrows):
        elm = {}
        for col in range(1, worksheet.ncols):
            elm[first_row[col]] = worksheet.cell_value(row, col)
        data.append(elm)
    data.sort(key=lambda x: x['Sito'])
    # richiedi una chiave
    key = ''
    while not key or len(key) > 16:
        key = input('Key (max 16 bytes): ')
    if len(key) < 16:
        key = pad(key.encode(), 16)
    else:
        key = key.encode()
    aes = AES.new(key, AES.MODE_ECB)
    # destinazione file password criptate
    path = input('File password criptate: ')
    f = open(path, 'w')
    # scrivi hash della chiave
    f.write(binascii.b2a_base64(SHA3_512.new(key).digest()).decode())
    # per ogni riga di dati che contiene una password scrivi il sito, lo username e la password criptata in base64
    for i in data:
        if i['Password']:
            f.write(i['Sito']+' '+i['Username']+' ')
            padded_password = pad(i['Password'].encode(), 16)
            f.write(binascii.b2a_base64(aes.encrypt(padded_password)).decode())
    f.close()


def decrypt():
    # destinazione file password criptate
    path = input('File password criptate: ')
    fe = open(path, 'r')
    # destinazione file password in chiaro
    path = input('File password decriptate: ')
    fd = open(path, 'w')
    # leggi l'hash della chiave di criptazione
    hashed_key = binascii.a2b_base64(fe.readline().encode())
    # richiedi chiave e verifica che i digest corrispondano
    hk = ''
    while hk != hashed_key:
        key = pad(input('Key: ').encode(), 16)
        hk = SHA3_512.new(key).digest()
        if hk != hashed_key:
            print('Wrong key!')
    # decripta le password e scrivile insieme al resto nel file di uscita
    aes = AES.new(key, AES.MODE_ECB)
    for i in fe:
        l = i.split()
        for j in range(len(l)-1):
            fd.write(l[j]+' ')
        fd.write(unpad(aes.decrypt(binascii.a2b_base64(l[-1].encode())), 16).decode()+'\n')
    fe.close()
    fd.close()


c = ''
while c != 'e' and c != 'd':
    c = input('Encrypt or decrypt passwords? (e/d) ')

if c == 'e':
    encrypt()
else:
    decrypt()
