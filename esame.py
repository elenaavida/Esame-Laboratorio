#classe per le eccezioni
class ExamException(Exception):
    pass

class CSVTimeSeriesFile:
    #inizializzatore che prende il nome del file in input e lo salva nell'attributo
    def __init__(self, name):
        #nome del file
        self.name = name
        #apro e provo a leggere una riga
        self.can_read = True
        try:
            file = open(self.name, 'r')
            file.readline()
        #se non riesco a leggere la riga setto a False
        except Exception as e:
            self.can_read = False
    def get_data(self):
        #se can_read è falso alzo un'eccezione 
        if not self.can_read:
            raise ExamException('Errore: file non leggibile o non esistente')
        else:
            #creo la lista in cui salvare i dati
            time_series = []
            #attributo per tenere traccia dell'anno
            anno = None
            #attributo per tenere traccia del mese
            mese = None
            #apro il file
            my_file = open(self.name, 'r')
            #setto intestazione a True
            intestazione = True
            #leggo il file riga per riga
            for line in my_file:
                #escludo la prima riga di intestazione e la cambio in false
                if intestazione:
                  intestazione = False
                  continue
                #faccio lo split sulla virgola nella riga, elements quindi conterrà una singola riga del file
                elements = line.split(',')
                #se la riga ha almeno due elementi
                if len(elements) >= 2:
                    #considero solo i primi due elementi scartando i successivi
                    elements = elements[0:2]
                    #controllo che il secondo elemento della lista sia un numero valido, lo converto in int e
                    #lo "pulisco" dai caratteri newline e dagli spazi
                    try:
                      elements[1] = int(float(elements[1].strip()))
                    #se il valore non è convertibile a numero allora non è valido, ignoro la riga
                    except ValueError:
                        continue
                    #se il numero di passeggeri è negativo ignoro la riga
                    if elements[1] < 0:
                      continue
                    #controllo che il primo elemento sia di tipo data
                    #mi assicuro che ci sia un solo trattino (tramite la funzione count che conta le occorrenze), che sia all'indice -3 e 
                    #che il suo indice sia maggiore di zero (quindi che non sia all'inizio), se le condizioni non sono rispettate ignoro la riga
                    if not (elements[0].count('-') == 1 and elements[0][-3] == '-' and elements[0].index('-') > 0):
                        continue
                    #visto che in elements[0] sono presenti sia anno che mese, li separo in due attributi diversi
                    anno = elements[0].split('-')[0]
                    mese = elements[0].split('-')[1]
                    #mi assicuro che nella parte dell'anno non ci siano caratteri non numerici, altrimenti ignoro la riga
                    try:
                      int(anno)
                    except ValueError:
                      continue
                    #mi assicuro che il mese sia uno dei valori ammissibili, altrimenti salto la riga
                    if not mese in ["01","02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
                        continue
                    #se la lunghezza della lista è 0 allora aggiungo elements (succederà solo nella prima iterazione)
                    if len(time_series) == 0:
                      time_series.append(elements)
                    #salvo l'ultimo anno/mese che ho accettato in time_series per fare i controlli
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
            #ritorno la lista
            return time_series

def find_min_max(time_series):
    #dizionario vuoto per memorizzare i risultati
    dizionario = {}
    #dizionario temporaneo per salvare i dati e aggiornarli mentre scorro i dati
    dizionario_temp = {}
    #per ogni coppia di data e passeggeri nella lista time_series suddivido anno, mese e passeggeri
    for data_passeggeri in time_series:
      anno = data_passeggeri[0].split('-')[0]
      mese = data_passeggeri[0].split('-')[1]
      passeggeri = data_passeggeri[1]
      #se l'anno si trova già tra le chiavi del dizionario temporaneo allora faccio i controlli dei valori
      if anno in list(dizionario_temp.keys()):
        #se il numero dei passeggeri della data attuale è uguale al numero minimo di passeggeri per quell'anno allora aggiungo ai mesi con il minimo per quell'anno
        if passeggeri == dizionario_temp[anno]["num_min_passeggeri"]:
          dizionario_temp[anno]["mesi_con_min"].append(mese)
        #se il numero dei passeggeri della data attuale è uguale al numero massimo di passeggeri per quell'anno allora aggiungo ai mesi con il massimo per quell'anno
        elif passeggeri == dizionario_temp[anno]["num_max_passeggeri"]:
          dizionario_temp[anno]["mesi_con_max"].append(mese)
        #se il numero di passeggeri della data attuale è minore dei mesi con il minimo allora verranno sostituiti sia il mese che il numero di passeggeri con quelli attuali
        elif passeggeri < dizionario_temp[anno]["num_min_passeggeri"]:
          dizionario_temp[anno]["mesi_con_min"] = [mese]
          dizionario_temp[anno]["num_min_passeggeri"] = passeggeri
        #se il numero di passeggeri della data attuale è maggiore dei mesi con il massimo allora verranno sostituiti sia il mese che il numero di passeggeri con quelli attuali
        elif passeggeri > dizionario_temp[anno]["num_max_passeggeri"]:
          dizionario_temp[anno]["mesi_con_max"] = [mese]
          dizionario_temp[anno]["num_max_passeggeri"] = passeggeri
      #se l'anno non è nella lista delle chiavi aggiungo al dizionario temporaneo la chiave anno, uso tutti i valori correnti perché è la prima occorrenza per quell'anno
      else:
        dizionario_temp[anno] = {"mesi_con_min":[mese],"mesi_con_max":[mese], "num_min_passeggeri": passeggeri, "num_max_passeggeri": passeggeri}
    #per ogni anno presente nella lista delle chiavi del dizionario temporaneo creo il dizionario definitivo con anno, massimo e minimo
    for anno in list(dizionario_temp.keys()):
      dizionario[anno] = {"min":dizionario_temp[anno]["mesi_con_min"] ,"max":dizionario_temp[anno]["mesi_con_max"]}
    #ritorno il dizionario definitivo
    return dizionario