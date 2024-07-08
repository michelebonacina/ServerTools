import sys
import datetime

def main(file_path, minutes):
    # memorizza il timestamp corrente
    current_time = datetime.datetime.now()
    
    # calcola il limite di tempo
    time_limit = current_time - datetime.timedelta(minutes=int(minutes))

    try:
        # legge il contenuto del file con la codifica UTF-8
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError as e:
        print(f"Errore di decodifica: {e}")
        return

    # crea una nuova lista di righe senza quelle da cancellare
    new_lines = []
    for line in lines:
        try:
            # estrae il timestamp dalla riga
            timestamp_str = line.split(',')[0].strip('"')
            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            
            # aggiunge la riga alla nuova lista se il timestamp non è troppo vecchio
            if timestamp >= time_limit:
                new_lines.append(line)
        except Exception as e:
            print(f"Errore nella lettura della riga: {e}")

    # scrive di nuovo il file con le righe aggiornate
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python mysqllogcleaner.py <path_del_file> <numero_di_minuti>")
    else:
        main(sys.argv[1], sys.argv[2])
