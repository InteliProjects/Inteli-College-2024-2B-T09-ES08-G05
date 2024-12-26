import requests
from sqlalchemy import Column, Integer, Float, TIMESTAMP, Boolean, func
from sqlalchemy.orm import Session
from app.database import Base, get_db
from dotenv import load_dotenv
from app.classes.heartbeat_logger import HeartBeatLogger
import os

# Load the .env file
load_dotenv()

# Access environment variables
USER_HOST = os.getenv('USER_HOST')
SERVER_NAME = "USER"

logger = HeartBeatLogger()

# Define the model for the history_availability table
class HistoryAvailable(Base):
    __tablename__ = "history_availability"

    history_id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, default=func.now(), nullable=False)
    status = Column(Boolean, nullable=False)
    latency = Column(Float, nullable=False)


# Function to measure latency
def measure_latency():
    url = f"{USER_HOST}/heart"
    attempt = 1
    max_attempts = 3
    timeout = 1  # Timeout in seconds for each attempt

    while attempt <= max_attempts:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            latency = response.elapsed.total_seconds() * 1000
            logger.log_success(latency=latency, server_name=SERVER_NAME, attempt=attempt)
            return latency, True
        except requests.RequestException:
            logger.log_failure(attempt=attempt, server_name=SERVER_NAME)
            attempt += 1

    # After three attempts, return None, False
    logger.log_max_attempts_reached(server_name=SERVER_NAME)
    return None, False


# Function to save latency and status to the database
def save_history_to_db(db: Session, latency: float, status: str):
    history_entry = HistoryAvailable(latency=latency, status=status)
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)


# Main function
def main():
    # Measure latency and status
    latency, status = measure_latency()

    if not status:
        # Place redundancy logic here
        logger.redundancy(server_name=SERVER_NAME)
        pass 

    # Save to the database
    with next(get_db()) as db:
        save_history_to_db(db, latency, status)
    
    return latency, status


if __name__ == "__main__":
    main()
