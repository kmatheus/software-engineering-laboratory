import time
import hashlib
import json

# [!] Simulação de um banco de dados de transações reais
DATABASE = {}

# [!] Simulação de um Cache rápido (como Redis) para travas temporárias
IDEMPOTENCY_CACHE = {}

def generate_idempotency_key(payload):
    """
    Gera uma 'impressão digital' única baseada nos dados da requisição.
    Se os dados forem idênticos, a chave será idêntica.
    """
    dump = json.dumps(payload, sort_keys=True) # [!] Garante que a ordem dos campos não mude o hash
    return hashlib.md5(dump.encode()).hexdigest()

def process_billing(student_id, amount, request_id=None):
    # Se não vier um ID do front-end, nós geramos um baseado nos dados
    payload = {"student_id": student_id, "amount": amount}
    ikey = request_id or generate_idempotency_key(payload)

    # 1. CHECK: Verificamos se já existe um processamento para esta chave
    if ikey in IDEMPOTENCY_CACHE:
        cached_res = IDEMPOTENCY_CACHE[ikey]
        
        # [!] Se ainda estiver processando, bloqueamos a nova tentativa (Lock de Idempotência)
        if cached_res['status'] == 'processing':
            return {"error": "Request in progress", "retry_after": 5}
            
        # [!] Se já finalizou, retornamos o resultado que já estava guardado
        return {"status": "already_done", "data": cached_res['result']}

    # 2. LOCK: Marcamos como 'processing' no cache para ninguém mais entrar
    IDEMPOTENCY_CACHE[ikey] = {"status": "processing", "started_at": time.time()}

    try:
        # 3. EXECUTE: Lógica de negócio (ex: chamada para a Stone)
        print(f"Executando cobrança real de R$ {amount} para o aluno {student_id}...")
        time.sleep(2) # [!] Simula delay de rede
        
        # Simulação de sucesso
        transaction_id = f"TX-{ikey[:8].upper()}"
        result = {"transaction_id": transaction_id, "amount": amount, "date": "2024-05-20"}

        # Salva no banco de dados real
        DATABASE[transaction_id] = result

        # 4. UPDATE: Salva o resultado final no cache para futuras consultas
        IDEMPOTENCY_CACHE[ikey] = {"status": "completed", "result": result}
        
        return {"status": "success", "data": result}

    except Exception as e:
        # [!] Em caso de erro crítico, removemos a trava para permitir nova tentativa
        del IDEMPOTENCY_CACHE[ikey]
        return {"status": "error", "message": str(e)}

# --- CENÁRIO DE TESTE ---
payload_aluno = {"student_id": 1, "amount": 500.0}

print("--- 1ª Tentativa (Processamento Normal) ---")
print(process_billing(**payload_aluno))

print("\n--- 2ª Tentativa (Imediatamente após, simulando clique duplo) ---")
# [!] Aqui ele deveria cair no 'already_done' ou 'in progress'
print(process_billing(**payload_aluno))