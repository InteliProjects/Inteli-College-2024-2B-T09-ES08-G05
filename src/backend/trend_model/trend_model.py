import pandas as pd
from sqlalchemy import text
from .database import get_db

def create_time_series():
    """
    Cria uma série temporal baseada nos timestamps de falhas registradas no banco de dados.
    """
    with next(get_db()) as db:  # Sessão de banco de dados
        query = db.execute(
            text("SELECT timestamp FROM history_availability WHERE status = false ORDER BY timestamp")
        ).mappings()

        # Extrair timestamps dos resultados
        timestamps = [row['timestamp'] for row in query]

    # Criar um DataFrame com os dados das falhas
    df = pd.DataFrame({'timestamp': timestamps})

    # Calcular os intervalos entre falhas em minutos
    df['interval_minutes'] = df['timestamp'].diff().dt.total_seconds() / 60
    return df

def predict_next_failure(df, window_size=5):
    """
    Prediz a próxima falha com base na média móvel dos intervalos entre falhas.
    """
    if df.shape[0] < window_size + 1:
        print("Dados insuficientes para fazer previsões.")
        return None

    df['moving_avg_interval'] = df['interval_minutes'].rolling(window=window_size).mean()
    last_timestamp = df['timestamp'].iloc[-1]
    last_moving_avg = df['moving_avg_interval'].iloc[-1]
    predicted_timestamp = last_timestamp + pd.Timedelta(minutes=last_moving_avg)

    return predicted_timestamp

def predict_next_n_failures(df, n=10, window_size=5):
    """
    Prediz os próximos N momentos de falha.
    """
    if df.shape[0] < window_size + 1:
        print("Dados insuficientes para fazer previsões.")
        return []

    df['moving_avg_interval'] = df['interval_minutes'].rolling(window=window_size).mean()
    last_timestamp = df['timestamp'].iloc[-1]
    last_moving_avg = df['moving_avg_interval'].iloc[-1]

    predictions = []
    for _ in range(n):
        last_timestamp += pd.Timedelta(minutes=last_moving_avg)
        predictions.append(last_timestamp)

    return predictions
