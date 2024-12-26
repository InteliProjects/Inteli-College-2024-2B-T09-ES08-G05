from .logger import Logger 

class UserLogger(Logger):
    def __init__(self,):
        super().__init__(log_filename='user.log')
    
    def __log_info(self, user_id, action, message):
        """Logs a specific user action."""
        log_message = f"User ID: {user_id} - Action: {action} - {message}"
        self._logger.info(log_message)
    
    def user_register(self, email):
        """Logs a user register."""
        self.__log_info(email, "REGISTER", "registered user")

    def log_error(self, user_id, error_message):
        """Logs a user error."""
        log_message = f"User ID: {user_id} - ERROR: {error_message}"
        self._logger.error(log_message)

    def user_login(self, user_id):
        """Logs user login action."""
        self.__log_info(user_id, "LOGIN", "User logged in successfully.")

    def user_logout(self, user_id):
        """Logs user logout action."""
        self.__log_info(user_id, "LOGOUT", "User logged out successfully.")

    def user_login_failed(self, email):
        """Logs user login fail."""
        self._logger.info(f"User email: {email} - Action: LOGIN_FAILED - Invalid email or password")
