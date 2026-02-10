import threading
import time
from decimal import Decimal

# Imagine que isso é uma tabela no seu banco de dados
class Account:
    def __init__(self, balance):
        self.balance = balance

account = Account(Decimal("100.00"))

def process_payment(amount, thread_name):
    print(f"[{thread_name}] Lendo saldo atual: R$ {account.balance}")
    
    # Simulando um delay de processamento (o tempo que o DB levaria)
    time.sleep(1) 
    
    if account.balance >= amount:
        print(f"[{thread_name}] Saldo suficiente! Subtraindo R$ {amount}...")
        account.balance -= amount
        print(f"[{thread_name}] Novo saldo: R$ {account.balance}")
    else:
        print(f"[{thread_name}] Erro: Saldo insuficiente.")

# Criando duas tentativas de pagamento ao mesmo tempo
t1 = threading.Thread(target=process_payment, args=(Decimal("60.00"), "Thread A"))
t2 = threading.Thread(target=process_payment, args=(Decimal("60.00"), "Thread B"))

t1.start()
t2.start()

t1.join()
t2.join()

print(f"\n--- RESULTADO FINAL NO BANCO: R$ {account.balance} ---")