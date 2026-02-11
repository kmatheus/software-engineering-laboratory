import logging
import json
import time
import random
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "context": record.__dict__.get("context", {})
        }
        return json.dumps(log_record)

logger = logging.getLogger("ResilientBilling")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def process_with_retry(student_id, amount, max_retries=3):
    start_time = time.time()
    attempt = 1
    success = False

    while attempt <= max_retries:
        log_context = {
            "student_id": student_id,
            "amount": amount,
            "attempt": attempt,
            "max_retries": max_retries
        }

        try:
            logger.info(f"Tentativa de processamento", extra={"context": log_context})
            
            # Simula instabilidade (falha em 70% das vezes na primeira tentativa)
            if attempt < 3 and random.random() < 0.7:
                raise ConnectionError("Timeout temporário na API de Notas Fiscais")

            duration = time.time() - start_time
            log_context["duration_ms"] = round(duration * 1000, 2)
            logger.info("Processamento concluído com sucesso", extra={"context": log_context})
            success = True
            break

        except Exception as e:
            log_context["error"] = str(e)
            if attempt < max_retries:
                logger.warning(f"Falha temporária, agendando nova tentativa", extra={"context": log_context})

                wait_time = 2 ** attempt 
                logger.warning(f"Falha temporária, aguardando {wait_time}s para reprocessar", extra={"context": log_context})
                time.sleep(wait_time)
            else:
                logger.error(f"Todas as tentativas falharam. Intervenção necessária.", extra={"context": log_context})
            
        attempt += 1

    return success

if __name__ == "__main__":
    # --- ÁREA DE TESTE ---
    print("🧪 Iniciando Simulação de [02 - Observability & Resiliency]...\n")

    process_with_retry(student_id=99, amount=250.0)
    
    print(f"\n--- 📈️ FIM DA SIMULAÇÃO ---")