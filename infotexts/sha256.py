import os
import shutil
import pathlib
import hashlib

def calc_hash(algo, filepath):
    # ハッシュオブジェクトを作ります
    h = hashlib.new(algo)

    # 分割する長さをブロックサイズの整数倍に決めます
    Length = hashlib.new(algo).block_size * 0x800

    # 大きなバイナリデータを用意します
    with open(filepath, 'rb') as f:
        BinaryData = f.read(Length)

        # データがなくなるまでループします
        while BinaryData:
            # ハッシュオブジェクトに追加して計算します。
            h.update(BinaryData)

            # データの続きを読み込む
            BinaryData = f.read(Length)

    # ハッシュオブジェクトを16進数で出力します
    return h.hexdigest()

def save_sha256_selected(filenames, list):
    for r in list:
        if r['filename'] not in filenames.split(','):
            continue
        save_sha256(r['filepath'], True)

def save_sha256(filepath, is_overwrite = False):
    sha256_path = filepath + '.sha256'
    
    if not os.path.exists(sha256_path) or is_overwrite:
        sha256 = calc_hash('sha256', filepath)
        with open(sha256_path, 'w') as f:
            f.write(sha256)

def list_sha256(dir, exts = []):
    if not os.path.exists(dir):
        return {}

    res = {}
    for filename in os.listdir(dir):
        if filename.endswith('.sha256'):
            continue
        filepath = os.path.join(dir, filename)
        sha256_name = filename + '.sha256'
        sha256_path = os.path.join(dir, sha256_name)

        # extsが指定されていなければ全拡張子を許可
        if exts:
            matched = False
            for ext in exts:
                # 列挙した拡張子に該当するものを許可
                if filename.endswith('.' + ext):
                    matched = True
                    break
            if not matched:
                continue

        if not os.path.exists(sha256_path):
            save_sha256(filepath)
        with open(sha256_path, 'r') as f:
            sha256 = f.read()
        res[sha256] = filepath
    return res

# 桁数を省略したsha256でも一致すれば返す
def match_sha256(sha256, sha256s):
    for k, v in sha256s.items():
        if k.startswith(sha256):
            return v
    return None
