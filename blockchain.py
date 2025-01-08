class Blockchain:
    def __init__(self):
        self.chain = []

    def record(self, piece_hash):
        self.chain.append(piece_hash)

    def get_recorded_hash(self, piece_hash):
        return piece_hash if piece_hash in self.chain else None

# インスタンスを作成
blockchain = Blockchain()