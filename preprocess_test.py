# preprocess_test.py
from PIL import Image
import os, glob

def prepare(inp_dir, out_dir, size=(256,256)):
    os.makedirs(out_dir, exist_ok=True)
    files = glob.glob(os.path.join(inp_dir, '*'))
    cnt=0
    for f in files:
        try:
            im = Image.open(f).convert('RGB')
            im = im.resize(size, Image.LANCZOS)
            out = os.path.join(out_dir, f'{os.path.splitext(os.path.basename(f))[0]}_resized.png')
            im.save(out)
            cnt+=1
        except Exception as e:
            print('skip', f, e)
    return cnt

if __name__ == '__main__':
    real_in='data/real'
    cart_in='data/cartoon'
    out_base='outputs/preprocess'
    r=prepare(real_in, os.path.join(out_base,'real'))
    c=prepare(cart_in, os.path.join(out_base,'cartoon'))
    print(f'real processed: {r}, cartoon processed: {c}')
    print('Preview images saved in', out_base)
