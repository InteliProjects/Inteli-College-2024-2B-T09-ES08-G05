import hashlib
import requests

# function to generate the SHA-256 hash of a file
def generate_sha256_hash_from_url(url: str):
    sha256_hash = hashlib.sha256()

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        for block in response.iter_content(4096):
            sha256_hash.update(block)
        
        return sha256_hash.hexdigest()
    
    except requests.RequestException as e:
        raise RuntimeError(f"Erro ao acessar a URL: {e}")
