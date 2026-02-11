import time
import hashlib
import json

DATABASE = {}

IDEMPOTENCY_CACHE = {}

def generate_idempotency_key(payload):
    """
    Gera uma 'impressão digital' única baseada nos dados da requisição.
    Se os dados forem idênticos, a chave será idêntica.
    """
    dump = json.dumps(payload, sort_keys=True)
    return hashlib.md5(dump.encode()).hexdigest()

def process_billing(student_id, amount, request_id=None):
    # Se não vier um ID do front-end, nós geramos um baseado nos dados
    payload = {"student_id": student_id, "amount": amount}
    ikey = request_id or generate_idempotency_key(payload)

    # 1. CHECK: Verificamos se já existe um processamento para esta chave
    if ikey in IDEMPOTENCY_CACHE:
        cached_res = IDEMPOTENCY_CACHE[ikey]
        
        if cached_res['status'] == 'processing':
            return {"error": "Request in progress", "retry_after": 5}
            
        return {"status": "already_done", "data": cached_res['result']}

    # 2. LOCK: Marcamos como 'processing' no cache para ninguém mais entrar
    IDEMPOTENCY_CACHE[ikey] = {"status": "processing", "started_at": time.time()}

    try:
        # 3. EXECUTE: Lógica de negócio (ex: chamada para a Stone)
        print(f"Executando cobrança real de R$ {amount} para o aluno {student_id}...")
        time.sleep(2)
        
        # Simulação de sucesso
        transaction_id = f"TX-{ikey[:8].upper()}"
        result = {"transaction_id": transaction_id, "amount": amount, "date": "2024-05-20"}

        # Salva no banco de dados real
        DATABASE[transaction_id] = result

        # 4. UPDATE: Salva o resultado final no cache para futuras consultas
        IDEMPOTENCY_CACHE[ikey] = {"status": "completed", "result": result}
        
        return {"status": "success", "data": result}

    except Exception as e:
        del IDEMPOTENCY_CACHE[ikey]
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # --- ÁREA DE TESTE ---
    print("🧪 Iniciando Simulação de [03 - Idempotency Pattern]...\n")
    payload_aluno = {"student_id": 1, "amount": 500.0}

    print("--- 1ª Tentativa (Processamento Normal) ---")
    print(process_billing(**payload_aluno))

    print("\n--- 2ª Tentativa (Imediatamente após, simulando clique duplo) ---")
    print(process_billing(**payload_aluno))

    print(f"\n--- 📈️ FIM DA SIMULAÇÃO ---")