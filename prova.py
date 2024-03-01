#classe per le eccezioni
class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
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
    def get_data(self):
        #definisco la lista di liste che verrà ritornata: il primo elemento della lista annidata è la data e il secondo il numero di passeggeri
        if not self.can_read:
            raise ExamException('Errore: file non leggibile o non esistente')
        else:
            #creo la lista in cui salvare i dati
            time_series = []
            #variabile per tenere traccia dell'anno
            anno = None
            #variabile per tenere traccia del mese
            mese = None
            #apro il file
            my_file = open(self.name, 'r')
            #lista per tenere traccia delle date già controllate
            date_viste = []
            #leggo il file riga per riga
            for line in my_file:
                #faccio lo split sulla virgola
                elements = line.split(',')
                #se la riga ha due elementi
                if len(elements) >= 2:
                    #considero solo i primi due elementi scartando i successivi
                    elements = elements[0:2]
                    #visto che in elements sono presenti sia anno che mese, li separo in due attributi diversi
                    anno = elements[0].split('-')[0]#aggiungere qualche controllo sull'anno?
                    mese = elements[0].split('-')[1]
                    #mi assicuro che il mese sia uno dei valori corretti
                    if not mese in ["01","02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
                        #se non è così alzo l'eccezione
                        raise ExamException('Errore: formato data non valido')
                    #controllo che il secondo elemento della lista sia un intero
                    if not isinstance(elements[1], int):
                      #se non è un intero alzo l'eccezione
                        raise ExamException('Errore: dati non omogenei')
                    #controllo che il primo elemento sia di tipo data
                    #mi assicuro che il trattino sia presente, non all'inizio e deve essere all'indice -3
                    if not ('-' in elements[0] and elements[0].index('-') != 0 and elements[0][-3] == '-'):
                        #se non rispetta le condizioni allora alzo l'eccezione
                        raise ExamException('Errore: formato data non valido')
                    #pulisco l'ultimo elemento dai caratteri newline e dagli spazi
                    elements[-1] = elements[-1].strip()
                    #salvo la data attuale per fare i controlli dei duplicati successivamente
                    data_attuale = elements[0]
                    #se la data attuale è già presente nella lista delle date controllate in precedenza alza un'eccezione
                    if data_attuale in date_viste:
                        raise ExamException('Errore: data duplicata')
                    #altrimenti aggiungo la data attuale a quelle controllate se non è già presente
                    else:
                        date_viste.append(data_attuale)
                    #creo un attributo per capire se i valori della lista elements sono accettabili oppure no, inizialmente setto a True
                    valori_accettabili = True
                    #controllo se gli elementi numerici sono accettabili
                    valori_accettabili = elements[1].isdigit() #all(element.isdigit() for element in elements[1:])
                    #se sono accettabili li aggiungo a time_series
                    if valori_accettabili:
                        #prima di aggiungerli alla lista controllo che i timestamp siano ordinati cronologicamente
                            if anno is not None:
                                #se l'anno attuale è minore del precedente alzo un'eccezione
                                if int(elements[0].split('-')[0]) < anno:
                                    raise ExamException('Errore: data non in ordine cronologico')
                                #altrimenti se l'anno attuale è uguale al precedente valuto il mese
                                elif int(elements[0].split('-')[0]) == anno:
                                    #se il mese attuale è minore del precedente alzo un'eccezione
                                    if int(elements[0].split('-')[1]) < mese:
                                        raise ExamException('Errore: data non in ordine cronologico')
                                    #se il mese attuale è uguale al precedente allora la data è duplicata
                                    if int(elements[0].split('-')[1]) == mese:
                                        raise ExamException('Errore: data duplicata')
                            #aggiorno l'anno
                            anno = int(elements[0].split('-')[0])
                            #aggiorno il mese
                            mese = int(elements[0].split('-')[1])
                            #aggiungo alla lista anno e mese se sono validi
                            time_series.append([elements[0], int(elements[1])])
            #chiudo il file
            my_file.close()
            #stampo la lista di liste
            for line in time_series:
                print(line)
            #ritorno la lista di liste
            return time_series

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()