import os
import sys
import pathlib
import hashlib

import gradio as gr

import modules.scripts as scripts
import modules.sd_vae as sd_vae
import modules.devices
from modules import shared, processing, generation_parameters_copypaste

def create_infotext_ex(p, all_prompts, all_seeds, all_subseeds, comments, iteration=0, position_in_batch=0):
    infotext = create_infotext_original(p, all_prompts, all_seeds, all_subseeds, comments, iteration, position_in_batch)
    
    exs = {}

    model_sha256_path = shared.sd_model.sd_checkpoint_info.filename + '.sha256'
    if not os.path.exists(model_sha256_path):
        pathlib.Path(model_sha256_path).write_text(calc_hash('sha256', shared.sd_model.sd_checkpoint_info.filename))
    exs['Model sha256'] = pathlib.Path(model_sha256_path).read_text()[:16]

    if sd_vae.loaded_vae_file is not None:
        vae_sha256_path = sd_vae.loaded_vae_file + '.sha256'
        if not os.path.exists(vae_sha256_path):
            pathlib.Path(vae_sha256_path).write_text(calc_hash('sha256', sd_vae.loaded_vae_file))
        exs['VAE sha256'] = pathlib.Path(vae_sha256_path).read_text()[:16]

    if shared.loaded_hypernetwork is not None:
        hyper_sha256_path = shared.loaded_hypernetwork.filename + '.sha256'
        if not os.path.exists(hyper_sha256_path):
            pathlib.Path(hyper_sha256_path).write_text(calc_hash('sha256', shared.loaded_hypernetwork.filename))
        exs['Hypernet sha256'] = pathlib.Path(hyper_sha256_path).read_text()[:16]

    # 同一の生成が出来ない条件の列挙
    options = []
    if p.sampler_name == 'Euler a':
        options.append('euler_a')
    if shared.cmd_opts.xformers:
        options.append('xformers')
    if shared.cmd_opts.lowvram:
        options.append('lowvram')
    if shared.cmd_opts.medvram:
        options.append('medvram')
    if p.batch_size > 1:
        options.append('batch_size')
    try:
        import torch
        gpu = torch.cuda.get_device_name()
        # 再現性のある出力が出来ない型番
        if gpu.find('GTX 16') != -1:
            options.append('gtx_16x0')
    except:
        pass
    try:
        if get_optimal_device() == 'cpu':
            options.append('cpu')
    except:
        pass
    if options:
        exs['Options'] = " ".join(options)

    return infotext + ", " + ", ".join([k if k == v else f'{k}: {generation_parameters_copypaste.quote(v)}' for k, v in exs.items() if v is not None])

create_infotext_original = processing.create_infotext
processing.create_infotext = create_infotext_ex

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
