import zlib
import requests

# Function to calculate the CRC32 checksum from a URL
def generate_crc32_checksum_from_url(url: str) -> str:
    checksum = 0

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check for any HTTP request errors

        # Read the content in chunks
        for block in response.iter_content(4096):
            checksum = zlib.crc32(block, checksum)
        
        # Return the checksum in hexadecimal format
        return format(checksum & 0xFFFFFFFF, "08x")
    
    except requests.RequestException as e:
        raise RuntimeError(f"Error accessing the URL: {e}")
