import hashlib

def generate_signature(raw_value_str: str, key: str, iterations: int) -> str:
    password_bytes = key.encode('utf-8')
    salt_bytes = raw_value_str.encode('utf-8')

    hash_bytes = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password_bytes,
        salt=salt_bytes,
        iterations=iterations
    )

    return hash_bytes.hex()


def verify_packet(packet, config):

    raw_value = round(packet["metric_value"], 2)
    raw_value_str = f"{raw_value:.2f}"

    secret_key = config["processing"]["stateless_tasks"]["secret_key"]
    iterations = config["processing"]["stateless_tasks"]["iterations"]

    generated_signature = generate_signature(raw_value_str, secret_key, iterations)

    return generated_signature == packet["security_hash"]