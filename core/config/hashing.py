# The PasswordManager class provides methods
# for hashing
# and verifying passwords using the bcrypt
# algorithm.
from envdatareader import EnvDataReader
import bcrypt

env = EnvDataReader()


class PasswordManager:
    @staticmethod
    def hash_password(password):
        rounds = int(env.get_value('BCRYPT_ROUNDS', default=12))

        salt = bcrypt.gensalt(rounds=rounds)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(input_password, hashed_password):
        return bcrypt.checkpw(
            input_password.encode('utf-8'),
            hashed_password.encode('utf-8'))
