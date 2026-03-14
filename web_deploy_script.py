import subprocess
import os
from termcolor import cprint

# --- CONFIGURACIÓN DEL PROYECTO URANIA ---
# Estos datos corresponden a tu configuración en Hostinger
VPS_USER = "root"
VPS_IP = "82.25.77.193"  
VPS_PORT = "2222" # <--- NUEVA VARIABLE DE PUERTO
REMOTE_PATH = "/var/www/urania/"
LOCAL_PROJECT_DIR = "./" # El directorio donde tienes tu index.html y assets

def deploy():
    cprint("🚀 Iniciando despliegue de Urania.vision...", "cyan", attrs=["bold"])
    
    # 1. Comando rsync:
    rsync_cmd = [
        "rsync", "-avz", "--delete",
        "-e", f"ssh -p {VPS_PORT}", # <--- SE AGREGA EL PUERTO AQUÍ
        "--exclude", ".git*",
        "--exclude", "__pycache__",
        "--exclude", "deploy.py",
        LOCAL_PROJECT_DIR,
        f"{VPS_USER}@{VPS_IP}:{REMOTE_PATH}"
    ]

    try:
        cprint("📦 Sincronizando archivos con el VPS de Hostinger...", "yellow")
        subprocess.run(rsync_cmd, check=True)
        
        # 2. Opcional: Reiniciar Nginx
        cprint("⚙️  Refrescando configuración de Nginx...", "yellow")
        ssh_cmd = [
            "ssh", "-p", VPS_PORT, f"{VPS_USER}@{VPS_IP}", # <--- SE AGREGA EL PUERTO AQUÍ (-p minúscula)
            "sudo systemctl restart nginx"
        ]
        subprocess.run(ssh_cmd, check=True)

        cprint("\n✅ ¡Despliegue exitoso en https://www.urania.vision!", "green", attrs=["bold"])
        
    except subprocess.CalledProcessError as e:
        cprint(f"\n❌ Error durante el despliegue: {e}", "red", attrs=["bold"])

if __name__ == "__main__":
    # Asegúrate de estar en el directorio correcto
    deploy()
