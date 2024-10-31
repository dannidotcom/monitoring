#!/bin/bash

# Obtenir l'utilisation du CPU
cpu_usage() {
    top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1"%"}'
}

# Obtenir l'utilisation de la mémoire
memory_usage() {
    free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'
}

# Obtenir l'utilisation de l'espace disque
disk_usage() {
    df -h | grep '^/dev/' | awk '{print "Disk Usage: "$5 " on "$1}'
}