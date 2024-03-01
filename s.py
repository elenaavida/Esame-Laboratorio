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
            intestazione = True
            #leggo il file riga per riga
            for line in my_file:
                if intestazione:
                  intestazione = False
                  continue
                #faccio lo split sulla virgola
                elements = line.split(',')
                #se la riga ha due elementi
                if len(elements) >= 2:
                    #considero solo i primi due elementi scartando i successivi
                    elements = elements[0:2]
                    #controllo che il secondo elemento della lista sia un numero valido, lo converto in int arrotondandolo e
                    #pulendolo dai caratteri newline e dagli spazi
                    try:
                      elements[1] = int(float(elements[1].strip()))
                      if elements[1] < 0:
                        raise ExamException('Errore: numero di passeggeri non valido')
                    except ValueError:
                        raise ExamException('Errore: numero passeggeri non valido')
                    #controllo che il primo elemento sia di tipo data
                    #mi assicuro che ci sia un solo trattino e che sia all'indice -3
                    if not (elements[0].count('-') == 1 and elements[0][-3] == '-' and elements[0].index('-')>0):
                        #se non rispetta le condizioni allora alzo l'eccezione
                        raise ExamException('Errore: data non valida')
                    #visto che in elements[0] sono presenti sia anno che mese, li separo in due attributi diversi
                    anno = elements[0].split('-')[0]
                    mese = elements[0].split('-')[1]
                    #mi assicuro che nella parte dell'anno non ci siano caratteri non numerici
                    try:
                      int(anno)
                    except ValueError:
                      raise ExamException('Errore: data non valida')
                    #mi assicuro che il mese sia uno dei valori ammissibili
                    if not mese in ["01","02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
                        #se non è così alzo l'eccezione
                        raise ExamException('Errore: data non valida')

                    #salvo la data attuale per fare i controlli dei duplicati successivamente
                    data_attuale = elements[0]
                    #se la data attuale è già presente nella lista delle date controllate in precedenza alza un'eccezione
                    if len(time_series) == 0:
                      #date_accettate.append(data_attuale)
                      time_series.append(elements)
                    else:
                      ultimo_anno_accettato = time_series[-1][0].split('-')[0]
                      ultimo_mese_accettato = time_series[-1][0].split('-')[1]
                      #controllo che l'anno che sto esaminando sia maggiore dell'ultimo accettato oppure che, nel caso in cui l'anno sia lo stesso, il mese sia maggiore
                      #non serve, siccome vengono usati < e non <=, controllare che la data non sia duplicata
                      if (int(ultimo_anno_accettato) < int(anno)) or (int(ultimo_anno_accettato) == int(anno) and int(ultimo_mese_accettato) < int(mese)):
                        time_series.append(elements)
                      else:
                        raise ExamException('Errore: data non in ordine cronologico oppure duplicata')

            #chiudo il file
            my_file.close()
            return time_series

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

def find_min_max(time_series):
    #dizionario vuoto per memorizzare i risultati
    dizionario = {}
    dizionario_temp = {}
    #se la lista è vuota ritorno il dizionario vuoto
    for data_passeggeri in time_series:
      anno = data_passeggeri[0].split('-')[0] #str
      mese = data_passeggeri[0].split('-')[1] #str
      passeggeri = data_passeggeri[1] #int
      if anno in list(dizionario_temp.keys()):
        #controllo mesi
        if passeggeri == dizionario_temp[anno]["num_min_passeggeri"]:
          dizionario_temp[anno]["mesi_con_min"].append(mese)
        elif passeggeri == dizionario_temp[anno]["num_max_passeggeri"]:
          dizionario_temp[anno]["mesi_con_max"].append(mese)
        elif passeggeri < dizionario_temp[anno]["num_min_passeggeri"]:
          dizionario_temp[anno]["mesi_con_min"] = [mese]
          dizionario_temp[anno]["num_min_passeggeri"] = passeggeri
        elif passeggeri > dizionario_temp[anno]["num_max_passeggeri"]:
          dizionario_temp[anno]["mesi_con_max"] = [mese]
          dizionario_temp[anno]["num_max_passeggeri"] = passeggeri
      else:
        dizionario_temp[anno] = {"mesi_con_min":[mese],"mesi_con_max":[mese], "num_min_passeggeri": passeggeri, "num_max_passeggeri": passeggeri}
    for anno in list(dizionario_temp.keys()):
      dizionario[anno] = {"min":dizionario_temp[anno]["mesi_con_min"] ,"max":dizionario_temp[anno]["mesi_con_max"]}
    return dizionario

find_min_max(time_series)