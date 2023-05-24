# multi_threaded_local_data.py
import time
import threading
from threading import Thread

def my_sum(a,b):
    """ a simple function summing integers from a to b """
    
    # create an instance of local (per-thread) memory 
    # now "the_sum" is *explicitely* thread-specific
    the_sum = threading.local() 

    the_sum = 0    
    for i in range(a,b):
        the_sum += i
    print (f'Sum from {a} to {b} = {the_sum}')

if __name__ == '__main__':
    # common "global" objects
    MIN = 0
    MAX = 100_000_000

    # create 2 threads
    # both acting on the same function
    # each summing half of the values
    t1 = Thread(target=my_sum, args=(MIN,MAX//2,))
    t2 = Thread(target=my_sum, args=(MAX//2,MAX,))

    # start a timer
    start = time.time()

    # start both threads 
    # thread #1 and thread #2 are started ~ at the same time 
    # and will be executed concurrently or in parallel (depending on the architecture)
    t1.start()
    t2.start()

    # join both threads 
    # *join* => wait a thread to have completed its task
    t1.join()
    t2.join()

    # stop the timer
    end = time.time()

    print()
    print(f'Time taken = {end - start:.2f} sec')


'''
Sì, in Python l'esistenza del GIL (Global Interpreter Lock) tende ad annullare le differenze pratiche tra 
l'utilizzo di variabili condivise e variabili locali per thread.

Il GIL è un meccanismo di protezione implementato nell'interprete CPython 
(l'implementazione di riferimento di Python) che consente l'esecuzione di un solo 
thread Python alla volta. Questo significa che anche se si utilizzano thread multipli
per suddividere il carico di lavoro, essi verranno comunque eseguiti sequenzialmente, 
uno alla volta, a causa del GIL.

In effetti, il GIL limita l'effettiva parallellizzazione del codice Python su più 
core di CPU, poiché consente a un solo thread di eseguire codice Python in un 
determinato momento, bloccando gli altri thread. Questo può comportare un 
risultato simile a quello che si otterrebbe se si utilizzassero variabili condivise 
tra i thread, poiché i thread si alternano nell'accesso e nella modifica delle 
variabili condivise, anche se vengono utilizzate variabili locali per thread.

Tuttavia, è importante sottolineare che il GIL non influisce sulla gestione dei 
dati locali per thread o sulla loro utilità concettuale nell'organizzare il codice. 
Sebbene il GIL possa limitare l'effettiva concorrenza tra i thread in Python, 
le variabili locali per thread possono comunque essere utili per garantire una 
corretta separazione dei dati e prevenire interferenze tra i thread.

In definitiva, mentre il GIL riduce l'impatto pratico delle differenze tra 
l'utilizzo di variabili condivise e variabili locali per thread, l'uso di variabili 
locali per thread può ancora avere vantaggi concettuali e organizzativi nel 
codice sorgente.
'''