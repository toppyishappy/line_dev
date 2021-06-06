from cryptography.fernet import Fernet

class CryptoGraphy:
    
    
    def __init__(self):
        pass

    def generate_key(self):
        """
            Generates a key and save it into a file
        """
        key = Fernet.generate_key()

        import pdb; pdb.set_trace()
    
    def encrypt_message(token):
        """
            Encrypts a message
        """
        # key = load_key()
        # f = Fernet(key)
        encoded_token = token.encode()
        encrypted_token = f.encrypt(encoded_token)
        return encrypted_token

    def decrypt_message(token):
        """
            Decrypts an encrypted message
        """
        # key = load_key()
        # f = Fernet(key)
        decrypted_token = f.decrypt(encrypted_token)
        return decrypted_token.decode()