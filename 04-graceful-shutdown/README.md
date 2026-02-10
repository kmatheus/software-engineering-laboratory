# 04 - Graceful Shutdown

## O Problema
Processos interrompidos abruptamente durante deploys ou reinicializações de servidor podem causar corrupção de dados ou estados inconsistentes em transações financeiras.

## O que foi aprendido:
- **Sinais do SO:** Captura de sinais `SIGINT` (interrupção) e `SIGTERM` (término).
- **Flag de Controle:** Uso de variáveis globais para impedir o início de novas tarefas enquanto finaliza a tarefa atual.
- **Resiliência em Deploy:** Como garantir que o Worker termine o boleto atual antes de permitir que o container seja destruído.