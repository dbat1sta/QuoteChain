import hashlib
import secrets

class QuoteChain:
    def __init__(self):
        self.chain = []
        self.add_genesis_block()

    def add_genesis_block(self):
        genesis_block = {
            'quote': "Genesis block",
            'nonce': secrets.token_bytes(32),
            'prev_hash': None,
            'hash': None
        }
        genesis_block['hash'] = self.calculate_hash(genesis_block)
        self.chain.append(genesis_block)

    def add_block(self, quote):
        prev_block = self.chain[-1]
        nonce = self.proof_of_work(prev_block['hash'], quote)
        block = {
            'quote': quote,
            'nonce': nonce,
            'prev_hash': prev_block['hash']
        }
        block['hash'] = self.calculate_hash(block)
        self.chain.append(block)

    def proof_of_work(self, prev_hash, quote):
        if prev_hash is None:
            prev_hash = bytes(32)
        nonce = secrets.token_bytes(32)
        hash_input = prev_hash + nonce + quote.encode('utf-8')
        while not self.is_valid_hash(hash_input):
            nonce = secrets.token_bytes(32)
            hash_input = prev_hash + nonce + quote.encode('utf-8')
        return nonce

    def is_valid_hash(self, hash_input):
        sha = hashlib.sha256()
        sha.update(hash_input)
        hash_output = sha.digest()
        return hash_output[:1] == b'\x00' and hash_output[1] < 32

    def calculate_hash(self, block):
        prev_hash = block['prev_hash']
        if prev_hash is None:
            prev_hash = bytes(32)
        sha = hashlib.sha256()
        sha.update(prev_hash + block['nonce'] + block['quote'].encode('utf-8'))
        return sha.digest()

    def print_chain(self):
        for block in self.chain:
            print("Quote:", block['quote'])
            print("Nonce:", block['nonce'])
            print("Hash:", block['hash'].hex())
            print()

if __name__ == "__main__":
    quote_chain = QuoteChain()
    quotes = [
        "My name is David.",
        "I love cybersecurity!",
        "Whats for lunch today?"
    ]
    for quote in quotes:
        quote_chain.add_block(quote)

    quote_chain.print_chain()

