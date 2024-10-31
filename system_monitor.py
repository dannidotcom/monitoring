import subprocess
import time

def log_system_resources(log_file):
    with open(log_file, 'a') as f:
        while True:
            # Appel du script shell pour obtenir les informations système
            cpu_usage = subprocess.getoutput("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1\"%\"}'")
            memory_usage = subprocess.getoutput("free -m | awk 'NR==2{printf \"Memory Usage: %s/%sMB (%.2f%%)\", $3,$2,$3*100/$2 }'")
            disk_usage = subprocess.getoutput("df -h | grep '^/dev/' | awk '{print \"Disk Usage: \"$5 \" on \"$1}'")

            # Formatage des données à enregistrer
            log_entry = f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            log_entry += f"CPU Usage: {cpu_usage}\n"
            log_entry += f"{memory_usage}\n"
            log_entry += f"{disk_usage}\n"
            log_entry += "----------------------------------\n"

            # Enregistrement dans le fichier de log
            f.write(log_entry)
            print(log_entry)

            # Pause de 5 secondes avant la prochaine surveillance
            time.sleep(5)

# Lancer la surveillance et journalisation
if __name__ == "__main__":
    log_file_path = "system_monitor.log"
    log_system_resources(log_file_path)