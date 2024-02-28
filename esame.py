#classe per le eccezioni
class ExamException(Exception):
    pass

class CSVFile:
    #inizializzatore che prende il nome del file in input e lo salva nell'attributo
    def __init__(self, name):
        #nome del file
        self.name = name
        
        #apro e leggo una riga
        self.can_read = True
        try:
            file = open(self.name, 'r')
            file.readline()
        except Exception as e:
            self.can_read = False
        
class CSVTimeSeriesFile(CSVFile):
    def get_data(self):
        #definisco la lista di liste che verrà ritornata, il primo elemento della lista annidata è la data e il secondo il numero di passeggeri
        if not self.can_read:
            raise ExamException('Errore nel file, non leggibile o non esistente')

        else:
            #creo la lista in cui salvare i dati
            time_series = []
            #apro il file
            my_file = open(self.name, 'r')
            
            #leggo il file riga per riga
            for line in my_file:
                #faccio lo split sulla virgola
                elements = line.split(',')

                #se la riga ha due elementi
                if len(elements) >= 2:
                    #pulisco l'ultimo elemento dai caratteri newline e dagli spazi
                    elements[-1] = elements[-1].strip()
                    #attributo per capire se i valori della lista elements sono accettabili oppure no, inizialmente setto a True
                    valori_accettabili = True
                    # Controllo se tutti gli elementi numerici sono accettabili
                    valori_accettabili = all(element.isdigit() for element in elements[1:])
                    #se sono accettabili li aggiungo a time_series
                    if valori_accettabili:
                        time_series.append([elements[0], int(elements[1])])
            my_file.close()
            for line in time_series:
                print(line)
            return time_series

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()


#funzione che deve ritornare il dizionario di dizionari con l'anno come chiave del dizionario esterno e come valore un altro dizionario che avrà come 
#due chiavi min e max che avranno due valori ovvero le liste che conterranno i mesi con i passeggeri minimi e massimi
#def find_min_max(time_series):
#    dict_min_max = {}
#    
#    return dict_min_max