import threading
import time
from decimal import Decimal

class BankAccount:
    def __init__(self, balance):
        self.balance = balance
        self._lock = threading.Lock()

    def withdraw(self, amount, thread_name):
        print(f"[{thread_name}] Tentando sacar R$ {amount}...")
        
        # Garante que apenas UMA thread execute no bloco
        with self._lock:
            print(f"[{thread_name}] Entrou na área crítica. Saldo: R$ {self.balance}")
            
            # Simula um tempo de IO/Banco de dados
            time.sleep(1) 
            
            if self.balance >= amount:
                self.balance -= amount
                print(f"[{thread_name}] Saque realizado! Novo saldo: R$ {self.balance}")
            else:
                print(f"[{thread_name}] Saque negado: Saldo insuficiente.")
        
        # O Lock é liberado automaticamente para a próxima thread

# Simulação
account = BankAccount(Decimal("100.00"))

first_thread = threading.Thread(target=account.withdraw, args=(Decimal("60.00"), "Thread A"))
second_thread = threading.Thread(target=account.withdraw, args=(Decimal("60.00"), "Thread B"))

first_thread.start()
second_thread.start()

first_thread.join()
second_thread.join()

print(f"\n--- RESULTADO FINAL SEGURO: R$ {account.balance} ---")