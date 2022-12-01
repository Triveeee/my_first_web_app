import os
from platform import *
from pandas import *

def menuStamp():
    print('\n------------------------------------ \n')
    print('#1 --> tempo reale')
    print('#2 --> media')
    print('\n------------------------------------ \n') 

def menu():
    n = 0
    while(n > 10 or n < 1):
        n =  int(input('scegli numero casa (1 / 10): '))
    topic = 'casa/' + str(n) + '/misurazioni'
    print(menuStamp())
    choose = int(input('scegli : '))
    return (topic , choose , n)

def clear():
    if(system() == 'Windows'):
        os.system('cls')
    if(system() == 'Linux'):
        os.system('clear')

def addElement(empty_dictionary, contenuto , nome ):
     empty_dictionary['cucina'].append(contenuto[0]['cucina'][nome])
     empty_dictionary['soggiorno'].append(contenuto[1]['soggiorno'][nome])
     empty_dictionary['mansarda'].append(contenuto[2]['mansarda'][nome])
     empty_dictionary['camera_da_letto'].append(contenuto[3]['camera_da_letto'][nome])
     return(empty_dictionary)   
    
def media(table):
    table_medie = {"cucina": 0, "soggiorno": 0, "mansarda": 0, "camera_da_letto": 0}
    medie = []
    for i in table:
        somma = 0
        for element in table[i]:
            somma = somma + element
            media = somma/len(table[i])
            medie.append(media)
    
    i = 0    
    for element in table_medie:
        table_medie[element] = medie[i]
        i+=1

    return(table_medie)


def findLastElement(items , n):
    table_temp = {"cucina": [], "soggiorno": [], "mansarda": [] , "camera_da_letto": []}
    table_umidita = {"cucina": [], "soggiorno": [], "mansarda": [] , "camera_da_letto": []}
    table_medie = {"cucina": 0, "soggiorno": 0, "mansarda": 0, "camera_da_letto": 0}
    items = items[(len(items) - n): ]

    for i in items:
        stanze = i['payload']['stanze']
        table_temp = addElement(table_temp, stanze , 'temperatura')
        table_umidita = addElement(table_umidita , stanze , 'umidita')
    
    table_medie = media(table_temp)    

    return(DataFrame(table_temp) , DataFrame(table_umidita) , Series(table_medie))

def createSeries(dati):
    serie = Series(dati)
    return(serie)

def show(dati):
    print('**TEMPERATURA**\n',dati[0], '\n')
    print('------------------------------------------------------------', '\n')
    print('**UMIDITA**\n',dati[1], '\n')
    print('------------------------------------------------------------', '\n')
    print('**MEDIA**\n',dati[2],'\n')
