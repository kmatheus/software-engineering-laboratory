# 04 - Graceful Shutdown

## O Problema
Processos interrompidos abruptamente durante deploys ou reinicializações de servidor podem causar corrupção de dados ou estados inconsistentes em transações financeiras.

## 📊 Visualização do Fluxo (Sinais do SO)
```mermaid
stateDiagram-v2
    [*] --> Running: Worker Iniciado
    Running --> Processing: Processando Tarefa #N
    Processing --> Running: Tarefa Finalizada
    
    state Signal_Caught <<choice>>
    Running --> Signal_Caught: Recebe SIGINT/SIGTERM
    Processing --> Signal_Caught: Recebe SIGINT/SIGTERM
    
    Signal_Caught --> Finishing: Finaliza Tarefa em Curso
    Finishing --> Cleanup: Executa Limpeza
    Cleanup --> [*]: Desligamento Seguro
```

## O que foi aprendido:
- **Sinais do SO:** Captura de sinais `SIGINT` (interrupção) e `SIGTERM` (término).
- **Flag de Controle:** Uso de variáveis globais para impedir o início de novas tarefas enquanto finaliza a tarefa atual.
- **Resiliência em Deploy:** Garantir que o Worker termine o boleto atual antes de permitir que o container seja destruído.

## Como rodar o experimento
```bash
python 04-graceful-shutdown/graceful_worker.py
```