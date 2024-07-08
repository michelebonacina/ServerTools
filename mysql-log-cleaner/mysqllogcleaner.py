import sys
import datetime

def main(file_path, minutes):
    # memorizza il timestamp corrente
    current_time = datetime.datetime.now()
    
    # calcola il limite di tempo
    time_limit = current_time - datetime.timedelta(minutes=int(minutes))

    # legge il contenuto del file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # crea una nuova lista di righe senza quelle da cancellare
    new_lines = []
    for line in lines:
        # estrae il timestamp dalla riga
        timestamp_str = line.split(',')[0].strip('"')
        timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        
        # aggiunge la riga alla nuova lista se il timestamp non è troppo vecchio
        if timestamp >= time_limit:
            new_lines.append(line)

    # scrive di nuovo il file con le righe aggiornate
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python mysqllogcleaner.py <path_del_file> <numero_di_minuti>")
    else:
        main(sys.argv[1], sys.argv[2])
