import hashlib
import random
import time
import numpy as np
import reedsolo

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
blockchain = {}
genesis_block = create_genesis_block()
blockchain[genesis_block.hash] = genesis_block

def add_block_to_blockchain(data):
    previous_block = list(blockchain.values())[-1]
    new_block = create_new_block(previous_block, data)
    blockchain[new_block.hash] = new_block

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
def verify_data(data_piece):
    hash_value = calculate_hash(data_piece)
    return hash_value in blockchain

# データの復号化（Reed-Solomon符号を用いたシミュレーション）
def decode_data(encoded_pieces, piece_size, data_size):
    rs = reedsolo.RSCodec(len(encoded_pieces) - data_size // piece_size)
    decoded_data = rs.decode(b''.join(encoded_pieces))
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

    # ノード間で符号化ピースをランダムに送受信
    nodes = [encoded_pieces.copy() for _ in range(num_nodes)]
    for node in range(num_nodes):
        # 一部の符号化ピースを改ざん
        tampered_index = random.randint(0, total_pieces - 1)
        nodes[node][tampered_index] = bytearray(random.getrandbits(8) for _ in range(piece_size))
        tampered_indices.append(tampered_index)
        print(f"Node {node}: Tampered data piece at index {tampered_index}")

        # 他のノードからランダムに符号化ピースを受信
        received_pieces = []
        for _ in range(total_pieces):
            sender_node = random.randint(0, num_nodes - 1)
            piece_index = random.randint(0, total_pieces - 1)
            piece = nodes[sender_node][piece_index]
            if verify_data(piece):
                received_pieces.append(piece)
            else:
                print(f"Node {node}: Data piece {piece_index} from Node {sender_node} is corrupted!")
                if piece_index not in tampered_indices:
                    detected_tampered += 1

        # 改ざんされたピースを除外してデータの復号化
        if len(received_pieces) >= data_size // piece_size:
            try:
                decoded_data = decode_data(received_pieces, piece_size, data_size)
                if decoded_data[:data_size] == data:
                    successful_decodes += 1
                else:
                    print(f"Node {node}: Decoded data does not match original data!")
            except reedsolo.ReedSolomonError:
                print(f"Node {node}: Reed-Solomon decoding failed!")
        else:
            print(f"Node {node}: Not enough valid pieces to reconstruct the original data.")

        print(f"Node {node}: Simulation completed successfully.")
    
    tampered_rate = len(tampered_indices) / total_pieces
    detection_rate = detected_tampered / len(tampered_indices) if tampered_indices else 0
    decode_success_rate = successful_decodes / num_nodes

    print("\nSimulation Results:")
    print(f"Total pieces: {total_pieces}")
    print(f"Tampered pieces: {len(tampered_indices)}")
    print(f"Detected tampered pieces: {detected_tampered}")
    print(f"Successful decodes: {successful_decodes}")
    print(f"Tampered indices: {tampered_indices}")
    print(f"Tampered rate: {tampered_rate:.2f}")
    print(f"Detection rate: {detection_rate:.2f}")
    print(f"Decode success rate: {decode_success_rate:.2f}\n")

if __name__ == "__main__":
    data_sizes = [1024, 2048, 4096]  # データサイズのリスト
    piece_size = 128
    num_nodes = 5  # ノード数

    for data_size in data_sizes:
        start_time = time.time()
        run_simulation(data_size, piece_size, num_nodes)
        end_time = time.time()
        print(f"Data size: {data_size} bytes, Simulation time: {end_time - start_time} seconds")