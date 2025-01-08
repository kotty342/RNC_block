import hashlib
import random
import time
import numpy as np

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_block_hash(index, previous_hash, timestamp, data):
    value = f"{index}{previous_hash}{timestamp}{data}".encode()
    return hashlib.sha256(value).hexdigest()

def create_genesis_block():
    return Block(0, "0", time.time(), "Genesis Block", calculate_block_hash(0, "0", time.time(), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    hash = calculate_block_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

# ブロックチェーンの初期化
blockchain = [create_genesis_block()]

def add_block_to_blockchain(data):
    previous_block = blockchain[-1]
    new_block = create_new_block(previous_block, data)
    blockchain.append(new_block)

# データをランダムに生成
def generate_data(size):
    return bytearray(random.getrandbits(8) for _ in range(size))

# データを符号化ピースに分割
def encode_data(data, piece_size):
    return [data[i:i + piece_size] for i in range(0, len(data), piece_size)]

# ハッシュ値を計算
def calculate_hash(data_piece):
    return hashlib.sha256(data_piece).hexdigest()

# データの正当性を確認
def verify_data(piece_index, data_piece):
    hash_value = calculate_hash(data_piece)
    for block in blockchain:
        if block.data == hash_value:
            return True
    return False

# データの復号化（線形代数を用いたシミュレーション）
def decode_data(encoded_pieces, piece_size, data_size):
    num_pieces = len(encoded_pieces)
    A = np.random.randint(0, 256, (num_pieces, num_pieces), dtype=np.uint8)
    A_inv = np.linalg.inv(A).astype(np.uint8)
    encoded_matrix = np.array([list(piece) for piece in encoded_pieces], dtype=np.uint8)
    decoded_matrix = np.dot(A_inv, encoded_matrix)[:data_size // piece_size]
    decoded_data = decoded_matrix.flatten().tobytes()
    return decoded_data

# シミュレーションの実行
def run_simulation(data_size, piece_size, num_nodes):
    data = generate_data(data_size)
    encoded_pieces = encode_data(data, piece_size)

    # 符号化ピースのハッシュ値を計算してブロックチェーンに記録
    for i, piece in enumerate(encoded_pieces):
        hash_value = calculate_hash(piece)
        add_block_to_blockchain(hash_value)

    total_pieces = len(encoded_pieces)
    tampered_indices = []
    detected_tampered = 0
    successful_decodes = 0

    # 各ノードでデータを受信し、改ざんをシミュレート
    for node in range(num_nodes):
        # 一部の符号化ピースを改ざん
        tampered_index = random.randint(0, total_pieces - 1)
        encoded_pieces[tampered_index] = bytearray(random.getrandbits(8) for _ in range(piece_size))
        tampered_indices.append(tampered_index)
        print(f"Node {node}: Tampered data piece at index {tampered_index}")

        # データの受信と検証
        received_pieces = []
        for i, piece in enumerate(encoded_pieces):
            if verify_data(i, piece):
                received_pieces.append(piece)
            else:
                print(f"Node {node}: Data piece {i} is corrupted!")
                detected_tampered += 1

        # 改ざんされたピースを除外してデータの復号化
        if len(received_pieces) * piece_size >= data_size:
            decoded_data = decode_data(received_pieces[:data_size // piece_size], piece_size, data_size)
            if decoded_data == data:
                successful_decodes += 1
            else:
                print(f"Node {node}: Decoded data does not match original data!")
        else:
            print(f"Node {node}: Not enough valid pieces to reconstruct the original data.")

        print(f"Node {node}: Simulation completed successfully.")
    
    tampered_rate = len(tampered_indices) / total_pieces
    detection_rate = detected_tampered / len(tampered_indices)
    decode_success_rate = successful_decodes / num_nodes

    print(f"Tampered indices: {tampered_indices}")
    print(f"Tampered rate: {tampered_rate:.2f}")
    print(f"Detection rate: {detection_rate:.2f}")
    print(f"Decode success rate: {decode_success_rate:.2f}")

if __name__ == "__main__":
    data_sizes = [1024, 2048, 4096]  # データサイズのリスト
    piece_size = 128
    num_nodes = 5  # ノード数

    for data_size in data_sizes:
        start_time = time.time()
        run_simulation(data_size, piece_size, num_nodes)
        end_time = time.time()
        print(f"Data size: {data_size} bytes, Simulation time: {end_time - start_time} seconds")