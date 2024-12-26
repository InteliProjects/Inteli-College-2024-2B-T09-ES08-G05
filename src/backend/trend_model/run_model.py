import time
from .trend_model import create_time_series, predict_next_n_failures

def main():
    while True:
        # Atualizar a série temporal
        df = create_time_series()
        print("Série Temporal de Falhas Atualizada:")
        print(df)

        # Prever as próximas 10 falhas
        next_failures = predict_next_n_failures(df, n=10, window_size=5)
        if next_failures:
            print("\nPróximas 10 falhas previstas:")
            for i, failure in enumerate(next_failures, 1):
                print(f"{i}: {failure}")
        else:
            print("\nNão foi possível fazer a previsão devido a poucos dados.")

        # Esperar 1 hora antes de rodar novamente
        time.sleep(3600)

if __name__ == "__main__":
    main()
