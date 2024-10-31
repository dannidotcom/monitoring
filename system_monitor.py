import tkinter as tk
from tkinter import ttk
import subprocess
import time
import threading

# Fonction pour obtenir les ressources système
def get_system_resources():
    cpu_usage = float(subprocess.getoutput("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\\([0-9.]*\\)%* id.*/\\1/' | awk '{print 100 - $1}'"))
    memory_output = subprocess.getoutput("free -m | awk 'NR==2{printf \"%s %s %.2f\", $3,$2,$3*100/$2 }'").split()
    memory_used = int(memory_output[0])
    memory_total = int(memory_output[1])
    memory_usage = float(memory_output[2])

    # Récupération des pourcentages de chaque partition et calcul de la moyenne
    disk_usage_outputs = subprocess.getoutput("df -h | grep '^/dev/' | awk '{print $5}' | sed 's/%//'").split()
    disk_usage_values = [float(value) for value in disk_usage_outputs]
    disk_usage = sum(disk_usage_values) / len(disk_usage_values)  # Moyenne de toutes les partitions

    return cpu_usage, memory_usage, memory_used, memory_total, disk_usage

# Mise à jour de l'affichage des ressources
def update_display():
    while True:
        cpu_usage, memory_usage, memory_used, memory_total, disk_usage = get_system_resources()
        time_display.config(text=f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Mise à jour des barres de progression
        cpu_bar['value'] = cpu_usage
        cpu_label.config(text=f"CPU Usage: {cpu_usage:.2f}%")

        memory_bar['value'] = memory_usage
        memory_label.config(text=f"Memory Usage: {memory_used}/{memory_total}MB ({memory_usage:.2f}%)")

        disk_bar['value'] = disk_usage
        disk_label.config(text=f"Disk Usage: {disk_usage:.2f}%")
        
        # Pause avant la prochaine mise à jour
        time.sleep(1)

# Création de l'interface Tkinter
root = tk.Tk()
root.title("System Monitor")

# Dimensions de la fenêtre
window_width = 400
window_height = 300
# Calcul de la position de la fenêtre pour la centrer
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

# Définir la géométrie pour centrer la fenêtre
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

root.configure(bg="#2E2E2E")  # Couleur de fond gris foncé

# Styles pour les barres de progression
style = ttk.Style(root)
style.theme_use('clam')
style.configure("TProgressbar", thickness=20, troughcolor="#3A3A3A", background="#5DADE2")

# Affichage de l'heure
time_display = tk.Label(root, font=("Helvetica", 12), fg="#F7F9F9", bg="#2E2E2E")
time_display.pack(pady=10)

# Barre et label pour l'utilisation CPU
cpu_label = tk.Label(root, font=("Helvetica", 10), fg="#F7F9F9", bg="#2E2E2E")
cpu_label.pack(pady=5)
cpu_bar = ttk.Progressbar(root, style="TProgressbar", orient="horizontal", length=300, mode="determinate", maximum=100)
cpu_bar.pack()

# Barre et label pour l'utilisation Mémoire
memory_label = tk.Label(root, font=("Helvetica", 10), fg="#F7F9F9", bg="#2E2E2E")
memory_label.pack(pady=5)
memory_bar = ttk.Progressbar(root, style="TProgressbar", orient="horizontal", length=300, mode="determinate", maximum=100)
memory_bar.pack()

# Barre et label pour l'utilisation du Disque
disk_label = tk.Label(root, font=("Helvetica", 10), fg="#F7F9F9", bg="#2E2E2E")
disk_label.pack(pady=5)
disk_bar = ttk.Progressbar(root, style="TProgressbar", orient="horizontal", length=300, mode="determinate", maximum=100)
disk_bar.pack()

# Lancer la mise à jour en arrière-plan
thread = threading.Thread(target=update_display)
thread.daemon = True
thread.start()

# Lancer l'interface
root.mainloop()
