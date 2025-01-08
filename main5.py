import numpy as np

def encode_data(data, k):
    """
    データを符号化ピースに分割する
    :param data: 入力データ
    :param k: 符号化ピースの数
    :return: 符号化ピースのリスト
    """
    data_matrix = np.array(data).reshape(-1, k)
    G = np.random.randint(0, 2, (k, k))  # ランダム生成行列
    encoded_pieces = np.dot(data_matrix, G) % 2
    return encoded_pieces, G

def distribute_pieces(encoded_pieces, nodes):
    """
    符号化ピースをノード間で分散する
    :param encoded_pieces: 符号化ピース
    :param nodes: ノードのリスト
    """
    for i, piece in enumerate(encoded_pieces):
        nodes[i % len(nodes)].append(piece)

def decode_data(received_pieces, G):
    """
    受信ノードが十分な符号化ピースを収集後、復号化する
    :param received_pieces: 受信した符号化ピース
    :param G: 生成行列
    :return: 復号化されたデータ
    """
    received_matrix = np.array(received_pieces)
    G_inv = np.linalg.inv(G) % 2
    decoded_data = np.dot(received_matrix, G_inv) % 2
    return decoded_data

# データの例
data = [1, 0, 1, 1, 0, 1, 0, 0]
k = 4  # 符号化ピースの数
nodes = [[] for _ in range(3)]  # 3つのノード

# 符号化
encoded_pieces, G = encode_data(data, k)
print("Encoded Pieces:", encoded_pieces)

# 分散
distribute_pieces(encoded_pieces, nodes)
print("Nodes after distribution:", nodes)

# 受信ノードが十分な符号化ピースを収集
received_pieces = [piece for node in nodes for piece in node]

# 復号化
decoded_data = decode_data(received_pieces, G)
print("Decoded Data:", decoded_data)