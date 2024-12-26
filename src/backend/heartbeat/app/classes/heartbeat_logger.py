from .logger import Logger 

class HeartBeatLogger(Logger):
    def __init__(self):
        super().__init__(log_filename='heartbeat.log')
    
    def log_success(self, server_name, latency, attempt):
        log_message = f"HEARTBEAT SUCCESS - Server: {server_name} - Attempt: {attempt} - Latency: {latency:.2f}ms"
        self._logger.info(log_message)
    
    def log_failure(self, server_name, attempt):
        log_message = f"HEARTBEAT FAILURE - Server: {server_name} - Attempt: {attempt}"
        self._logger.error(log_message)
    
    def log_max_attempts_reached(self, server_name):
        log_message = f"HEARTBEAT FAILURE - Server: {server_name} - Max attempts reached."
        self._logger.critical(log_message)

    def redundancy(self, server_name):
        log_message = f"{server_name.upper()} REDUNDANCY CALLED."
        self._logger.info(log_message)