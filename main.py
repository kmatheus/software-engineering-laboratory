import subprocess
import sys

def run_script(path):
    """Executa um script Python em um processo separado."""
    print(f"\n🚀 Executando: {path}")
    print("-" * 40)
    try:
        result = subprocess.run([sys.executable, path], check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao executar o laboratório: {path}")
    except KeyboardInterrupt:
        print(f"\n⚠️ Simulação interrompida pelo usuário.")
    print("-" * 40)

def main():
    labs = {
        "1": "01-race-conditions/secure_implementation.py",
        "2": "02-observability/resilient_logging.py",
        "3": "03-idempotency/idempotent_engine.py",
        "4": "04-graceful-shutdown/graceful_worker.py"
    }

    while True:
        print("\n 🛠️  SOFTWARE ENGINEERING LABORATORY")
        print("1. Race Conditions & Data Integrity")
        print("2. Observability & Resiliency")
        print("3. Idempotency Pattern")
        print("4. Graceful Shutdown")
        print("5. Rodar TODOS em sequência")
        print("0. Sair")
        
        choice = input("\nEscolha um lab: ")

        if choice == "0":
            break
        elif choice == "5":
            for path in labs.values():
                run_script(path)
        elif choice in labs:
            run_script(labs[choice])
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()