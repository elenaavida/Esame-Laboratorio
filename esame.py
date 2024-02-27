#classe per le eccezioni
class ExamException(Exception):
    pass

class CSVFile:
    
    def __init__(self, name):
        self.name = name
        self.can_read = True
        try:
            file = open(self.name, 'r')
            file.readline()
        except Exception as e:
            self.can_read = False
        
class CSVTimeSeriesFile(CSVFile):
    #inizializzatore che prende il nome del file in input e lo salva nell'attributo
    def __init__(self, name):
        self.name = name

    def get_data(self):
        #definisco la lista di liste che verrà ritornata, il primo elemento della lista annidata è la data e il secondo il numero di passeggeri
        time_series = []
        
        return time_series

#funzione che deve ritornare il dizionario di dizionari con l'anno come chiave del dizionario esterno e come valore un altro dizionario che avrà come 
#due chiavi min e max che avranno due valori ovvero le liste che conterranno i mesi con i passeggeri minimi e massimi
def find_min_max(time_series):
    dict_min_max = {'min': [], 'max': []}
    
    return dict_min_max