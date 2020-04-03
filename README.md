# hkn_password_encryption

## Formato file Excel
Le password da criptare insieme al resto delle informazioni di login vengono fornite tramite foglio Excel. Lo script analizza la prima riga del foglio in cui devono essere indicate le sezioni nelle quali è suddiviso lo stesso. Il minimo set di informazioni necessario per poter associare una password ad un utente sono: Sito, Username e Password. Tali sezioni devono essere obbligatoriamente presenti nel foglio.

## Cifrario utilizzato
Il cifrario utilizzato è l’Advanced Encryption Standard. L’AES è un algoritmo di cifratura a blocchi, di 128 bit, con chiave privata, di lunghezza in questo caso anch’essa di 128 bit. Come specifica di padding è stato utilizzato il PKCS#7.

## Descrizione dello script
All’inizio del programma, scritto in linguaggio Python3, viene chiesta di effettuare una scelta tra il produrre un file contenente il set minimo di informazioni di login con password criptate oppure di ricavare le password da quest’ultimo.

La funzione encrypt analizza i dati presenti nel foglio Excel. Dopo ciò richiede di inserire una chiave per la cifratura. L’hash della stessa viene quindi scritto nel file di uscita. Per ogni riga del foglio in cui sia presente una password ne viene scritta una nel file di uscita contenente il sito di login, lo username e la password dell’utente criptata e formattata in base64.

La funzione decrypt richiede la chiave per la decodifica e ne produce un digest con lo stesso algoritmo di hashing usato dalla funzione encrypt. Viene quindi letta la prima riga del file criptato e confrontata con il digest. Se questa non corrisponde viene chiesto di reinserire la chiave, altrimenti viene prodotto un file analogo con le passsword in chiaro.
