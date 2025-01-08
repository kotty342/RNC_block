import hashlib
from blockchain import blockchain  # 自作のブロックチェーンモジュールをインポート

def generate_piece(data):
    return data  # 符号化ピースを生成するロジック

def calculate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def record_hash_on_blockchain(piece_hash):
    blockchain.record(piece_hash)

def verify_piece(piece):
    piece_hash = calculate_hash(piece)
    recorded_hash = blockchain.get_recorded_hash(piece_hash)
    return piece_hash == recorded_hash

# シミュレーション用のデータセット
data_set = ["example data 1", "example data 2", "example data 3"]

# 符号化ピースの生成とブロックチェーンへの記録
for data in data_set:
    piece = generate_piece(data)
    piece_hash = calculate_hash(piece)
    record_hash_on_blockchain(piece_hash)
    print(f"Recorded hash for '{data}': {piece_hash}")

# 正しいデータの検証
for data in data_set:
    received_piece = generate_piece(data)
    is_valid = verify_piece(received_piece)
    print(f"Verification for '{data}': {'Valid' if is_valid else 'Invalid'}")

# 改ざんされたデータの検証
tampered_data_set = ["tampered data 1", "tampered data 2", "tampered data 3"]
for data in tampered_data_set:
    received_piece = generate_piece(data)
    is_valid = verify_piece(received_piece)
    print(f"Verification for tampered '{data}': {'Valid' if is_valid else 'Invalid'}")