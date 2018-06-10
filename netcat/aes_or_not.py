import sys

sys.path.append('/home/infinite/PycharmProjects/')
sys.path.append('/home/infinite/PycharmProjects/cryptopals')

# import cryptopals
from cryptopals import block, util
import base64

cipher = 'SNXIDUFQW0Ul6GXI4NyU/LMHl+vRlVIYp4pvFstfpP1n1C9Xhbl/bNip6mK5l7TMPS+vw247XTYK3LKIGT4AZVh6zUB97fN3fOamkLvzpmA='
print(cipher)
decoded_cipher = base64.b64decode(cipher)
print(decoded_cipher)

for b in util.groups(decoded_cipher, block.BLOCK_SIZE):
    print(block, len(b))

print(block.detect_aes_ecb(decoded_cipher))
