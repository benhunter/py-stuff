positions = [0x40, # 64 e
             0x26, # 38 m
             0x43, # 67 _
             0x58, # 88
             0x15, # 21
             0x44, # 68
             0x5f, # 95
             0x24] # 36

# 21, 36, 38, 64, 67, 68, 88, 95
#  a,  b,  c,  d,  e,  f,  g,  h

def positions():
    print(sorted(positions))

def mask():
    mask = ''
    for i in range(max(positions)):
        print(i)
        next_char = '-'
        if i + 1 in positions:
            next_char = 'x'
        mask += next_char
    print(mask)

# mask = "---------------------a--------------x-m-------------------------e--_b-------------------o------x"
mask =   "---------------------{}--------------{}-{}-------------------------{}--{}{}-------------------{}------{}-------------------------------\n"
# mask = "---------------------a--------------b-c-------------------------d--ef-------------------g------h"
# from_mpeg_mask =   "---------------------a----------------m-------------------------e--_b-------------------o--------------------------------------"

def brute():
    # lines = []
    # 30-128 printable characters
    current = mask

    a = 'a'
    c = 'm'
    d = 'e'
    e = '_'
    f = 'b'
    g = 'o'

    with open("elementary_brute.txt", 'w') as out_file:
        # for a in range(32, 128):
        # print(chr(a))
        for b in range(32, 128):
            # for c in range(32, 128):
            # for d in range(32, 128):
            # for e in range(32, 128):
            # for f in range(32, 128):
            # for g in range(32, 128):
                for h in range(32, 128):
                    # print(mask.format(chr(a),chr(b),chr(c),chr(d),chr(e),chr(f),chr(g),chr(h)))
                    out_file.write(mask.format(a,chr(b),c,d,e,f,g,chr(h)))

brute()

