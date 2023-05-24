# multi_threaded_nolock.py
import time
import threading
from threading import Thread
from colorama import Fore, Style

def my_sum_mod(a,b,m):
    """ a simple function summing integers from a to b 
        also check whether the current value is a multiple of m; if so:
          - add +1 to a common counter 
          - store the current value in a common list
    """

    # use the COMMON_COUNTER and COMMON_LIST variables, common to all threads
    global COMMON_COUNTER
    global COMMON_LIST

    # create an instance of local (per-thread) memory 
    # now "the_sum" is *explicitely* thread-specific
    the_sum = threading.local() 

    the_sum = 0    
    for i in range(a,b):
        the_sum += i
        if i%m == 0:
            COMMON_COUNTER += 1
            COMMON_LIST.append(i)

    print (f'Sum from {a} to {b} = {the_sum}')

if __name__ == '__main__':
    # common "global" objects
    MIN = 0
    MAX = 100_000_000
    MOD = 1397
    COMMON_COUNTER = 0 
    COMMON_LIST    = [] 

    # create 2 threads
    # both acting on the same function
    # each summing half of the values
    t1 = Thread(target=my_sum_mod, args=(MIN,MAX//2,MOD))
    t2 = Thread(target=my_sum_mod, args=(MAX//2,MAX,MOD))

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

    if COMMON_COUNTER != len(COMMON_LIST):
        print(Fore.RED + Style.BRIGHT)
    print()
    print(f'Number of multiples of {MOD} in the sum from {MIN} to {MAX} = {COMMON_COUNTER}')
    print()
    print(f'First 100 items of the list of multiples of {MOD}:')
    print(COMMON_LIST[:100])
    print()
    print(f'Cross-check of the size of the list: {len(COMMON_LIST)}')
    print()
    print(f'Time taken = {end - start:.2f} sec')
    print(Style.RESET_ALL)



'''
Il nome "nolock" nel programma "multi_threaded_nolock.py" potrebbe essere fuorviante.
Non è corretto dire che non c'è nessun blocco o nessuna gestione del lock nel codice.
Il programma utilizza infatti un blocco implicito, chiamato Global Interpreter Lock 
(GIL), che controlla l'accesso simultaneo ai thread Python.

Il termine "nolock" potrebbe riferirsi al fatto che il codice non utilizza 
esplicitamente un oggetto di lock, come ad esempio `Lock` o `RLock` del modulo 
`threading`, per gestire l'accesso concorrente alle variabili condivise. 
Invece, il codice si affida al GIL per garantire che solo un thread alla volta possa 
ùeseguire il codice Python.

Tuttavia, è importante notare che il GIL non risolve tutti i problemi di concorrenza 
e accesso concorrente ai dati. Sebbene il GIL prevenga la simultanea esecuzione di 
più thread Python, non impedisce l'interferenza tra le operazioni di lettura e 
scrittura da parte di thread diversi su variabili condivise. Pertanto, sebbene il
programma non utilizzi esplicitamente un oggetto di lock, potrebbero verificarsi 
situazioni di race condition o inconsistenze nei dati condivisi.

In conclusione, il nome "nolock" nel programma potrebbe essere fuorviante 
perché non indica l'assenza di meccanismi di blocco, ma piuttosto il fatto 
che il codice si affida al GIL per la gestione dell'accesso concorrente.
'''