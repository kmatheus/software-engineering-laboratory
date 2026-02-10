import signal
import time
import sys

keep_running = True

def handle_shutdown(signum, frame):
    """
    Função chamada quando o sistema pede para o Python parar (SIGINT ou SIGTERM)
    """
    global keep_running
    print(f"\n[SINAL] Recebido sinal de desligamento ({signum}). Finalizando tarefas pendentes...")

    keep_running = False

# Registra os sinais de interrupção (Ctrl+C) e encerramento (Deploy/Kubernetes)
signal.signal(signal.SIGINT, handle_shutdown)
signal.signal(signal.SIGTERM, handle_shutdown)

def process_tasks():
    tasks = range(1, 11)
    
    for task_id in tasks:
        if not keep_running:
            print("[ALERTA] Shutdown em curso. Não iniciaremos o boleto", task_id)
            break
            
        print(f"[WORKER] Processando boleto #{task_id}...")
        
        # Simula o processamento de um boleto (2 segundos)
        time.sleep(2)
        
        print(f"[WORKER] Boleto #{task_id} finalizado com sucesso.")

    print("[SISTEMA] Todas as tarefas críticas foram salvas. Saindo agora com segurança.")
    sys.exit(0)

# --- EXECUÇÃO ---
print("Simulando Worker de Faturamento. Pressione Ctrl+C para testar o Shutdown Suave.")
process_tasks()