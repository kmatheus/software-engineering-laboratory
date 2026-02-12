# 01 - Race Conditions & Data Integrity

## O Problema
Em sistemas que processam pagamentos simultâneos, pode ocorrer uma "Condição de Corrida", onde duas threads leem o mesmo saldo antes de uma delas atualizá-lo, resultando em dados inconsistentes (ex: saldo negativo indevido).

## 📊 Visualização do Fluxo (Lock)
```mermaid
sequenceDiagram
    participant TA as Thread A (Saque R$60)
    participant B as Objeto BankAccount
    participant TB as Thread B (Saque R$60)

    TA->>B: Tenta adquirir Lock
    B-->>TA: Lock Adquirido
    Note over TA,B: Área Crítica (Protegida)
    TA->>B: Lê Saldo (R$100)
    rect rgb(200, 220, 240)
    Note right of TB: Thread B aguarda (WAIT)
    end
    TA->>B: Subtrai R$60 (Saldo: R$40)
    TA->>B: Libera Lock
    
    TB->>B: Tenta adquirir Lock
    B-->>TB: Lock Adquirido
    TB->>B: Lê Saldo (R$40)
    Note right of TB: Saldo insuficiente para R$60
    TB->>B: Saque Negado
    TB->>B: Libera Lock
```

## O que foi aprendido:
- **Área Crítica:** Identificar trechos de código que manipulam recursos compartilhados.
- **Mutual Exclusion (Mutex):** Uso de `Lock` para garantir que apenas um processo altere o dado por vez.
- **Atomicidade:** Garantir que uma transação ocorra por completo ou não ocorra.

## Como rodar o experimento
```bash
python 01-race-conditions/secure_implementation.py
```

## 🖥️ Resultado no Terminal
Evidência da execução garantindo a integridade:

![Print do Terminal](./terminal_output.png)