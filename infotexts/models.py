import os
import pathlib
import json

from modules import sd_models

param_keys = [
    "model_hash",
    "hypernet",
    "model_sha256",
    "vae_sha256",
    "hypernet_sha256",
    "steps",
    "sampler",
    "cfg_scale",
    "width",
    "height",
    "seed",
    "clip_skip",
    "prompt",
    "negative_prompt",
    "hypernet_strength",
    "eta",
    "ensd",
    "subseed",
    "subseed_strength",
	"seed_resize_from_w",
    "seed_resize_from_h",
    "denoising_strength",
]

default_webp_settings = {
    "webp_quality": "90",
    "upscaler": "R-ESRGAN 2x+",
    "upscaling_resize": "2",
    "upscaling_resize_w": "0",
    "upscaling_resize_h": "0",
    "upscaling_crop": "1",
    "imagefont_truetype": "Arial.ttf",
    "imagefont_truetype_index": "0",
    "imagefont_truetype_size": "24",
    "draw_text_left": "0",
    "draw_text_top": "0",
    "draw_text_color": "Black",
    "draw_text": ""
}

default_generate_settings = {
    "input_dir": "",
    "output_dir": "",
    "ignore_keys": [],
    "webp_dir": "",
}
def load_webp_settings():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'webp.json')
    settings = default_webp_settings
    if os.path.exists(filepath):
        with open(filepath) as f:
            settings.update(json.load(f))
    return settings

def save_webp_settings(*input_settings):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'webp.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    i = 0
    for k in default_webp_settings.keys():
        data.update({k: input_settings[i]})
        i += 1
    with open(filepath, "w") as f:
        json.dump(data, f)
    return json.dumps(data)

def load_generate_settings():
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'generate.json')
    settings = default_generate_settings
    if os.path.exists(filepath):
        with open(filepath) as f:
            settings.update(json.load(f))
    return settings

def save_generate_settings(*input_settings):
    p = pathlib.Path(__file__).parts[-4:-2]
    filepath = os.path.join(p[0], p[1], 'config', 'generate.json')
    data = {}
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    i = 0
    for k in default_generate_settings.keys():
        data.update({k: input_settings[i]})
        i += 1
    with open(filepath, "w") as f:
        json.dump(data, f)
    return json.dumps(data)

def list():
    p = pathlib.Path(__file__).parts[-3]

    rs = []
    for filepath in list_dirs():
        if not os.path.exists(filepath):
            continue

        filename = os.path.basename(filepath)

        r = {}

        r['title'] = filename
        r['filename'] = filename
        r['filepath'] = filepath
        r['files'] = sum(os.path.isfile(os.path.join(filepath, name)) for name in os.listdir(filepath))

        rs.append(r)

    return rs

def list_dirs():
    p = pathlib.Path(__file__).parts[-4:-2]
    dirs = [
        os.path.join(p[0], p[1], 'txt'),
        os.path.join(p[0], p[1], 'png'),
        os.path.join(p[0], p[1], 'json'),
        os.path.join(p[0], p[1], 'edit_txt'),
        os.path.join(p[0], p[1], 'output'),
        os.path.join(p[0], p[1], 'webp'),
    ]

    return dirs

def get_generate_input_dir():
    cfg = load_generate_settings()
    if cfg['input_dir']:
        return cfg['input_dir']

    p = pathlib.Path(__file__).parts[-4:-2]
    return os.path.join(p[0], p[1], 'edit_txt')

def get_generate_output_dir(is_default = True):
    cfg = load_generate_settings()
    if cfg['output_dir']:
        return cfg['output_dir']
    if not is_default:
        return ''

    p = pathlib.Path(__file__).parts[-4:-2]
    return os.path.join(p[0], p[1], 'output')

def get_generate_webp_dir(is_default = False):
    cfg = load_generate_settings()
    if cfg['webp_dir']:
        return cfg['webp_dir']
    if not is_default:
        return ''

    p = pathlib.Path(__file__).parts[-4:-2]
    return os.path.join(p[0], p[1], 'webp')

def get_ignore_keys():
    cfg = load_generate_settings()
    if cfg['ignore_keys']:
        return cfg['ignore_keys']
    return []

def txt_to_dict(filepath, is_array = False):
    import modules.generation_parameters_copypaste as parameters_copypaste
    with open(filepath, 'r', encoding="utf-8") as f:
        text = f.read()
    params = parameters_copypaste.parse_generation_parameters(text)

    res = {}
    for k, v in params.items():
        k = k.replace(' ', '_')
        if k == 'Size-1':
            k = 'Width'
        elif k == 'Size-2':
            k = 'Height'
        if is_array and k not in ['Prompt', 'Negative_Prompt']:
            res[k] = [v]
        else:
            res[k] = v
    return res

def dict_to_text(job):
    text = ''

    if 'Prompt' in job:
        text += job['Prompt'] + "\n"
        del job['Prompt']
    if 'Megative_Prompt' in job:
        text += job['Megative_Prompt'] + "\n"
        del job['Megative_Prompt']
    if 'Steps' in job:
        text += f"Steps: {job['Steps']}, "
        del job['Steps']

    pairs = []
    for k, v in job.items():
        pairs.append(f"{k}: {v}")
    text += f"{', '.join(pairs)}\n"

    return text
