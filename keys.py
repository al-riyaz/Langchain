import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


def get_api_key(engine="gemini"):
    try:
        decryption_key = os.environ["OPENAPI_DECRYPTION_KEY"]
        if engine == "gemini":
            encrypted_value = os.environ["GEMINI_API_KEY"]
        else:
            encrypted_value = os.environ["OPENAI_API_KEY"]
        cipher = Fernet(decryption_key.encode())
        api_key = cipher.decrypt(encrypted_value.encode()).decode()
    except Exception as e:
        print(f"Error Fetching API Key:{e}")

    return api_key
