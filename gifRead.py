#!/usr/bin/env python

print('Starting...')

import wave, struct, math, sys
from PIL import Image
class GIFError(Exception): pass

# I don't know how this works either. Treat it as a black box.
def get_gif_num_frames(filename):
    frames = 0
    with open(filename, 'rb') as f:
        if f.read(6) not in ('GIF87a', 'GIF89a'):
            raise GIFError('not a valid GIF file')
        f.seek(4, 1)
        def skip_color_table(flags):
            if flags & 0x80: f.seek(3 << ((flags & 7) + 1), 1)
        flags = ord(f.read(1))
        f.seek(2, 1)
        skip_color_table(flags)
        while True:
            block = f.read(1)
            if block == ';': break
            if block == '!': f.seek(1, 1)
            elif block == ',':
                frames += 1
                f.seek(8, 1)
                skip_color_table(ord(f.read(1)))
                f.seek(1, 1)
            else: raise GIFError('unknown block type')
            while True:
                l = ord(f.read(1))
                if not l: break
                f.seek(l, 1)
    return frames


#initialize values (later to be used from args)
filename = sys.argv[1]
stepTime = int(sys.argv[2])
delay = int(sys.argv[3])

im = Image.open(filename)
sz = im.size
length = get_gif_num_frames(filename)

gif = []
#initialize gif array
for i in range(sz[0]):
    gif.append([])
    for j in range(sz[1]):
        gif[i].append([0]*(length + delay/stepTime))

k = 0
print "initialized..."
#populate gif array
try:
    while 1:
        rgb_im = im.convert('RGB')
        for i in range(sz[0]):
            for j in range(sz[1]):
                gif[i][j][k+delay/stepTime] = sum(rgb_im.getpixel((i,j)))
        im.seek(im.tell()+1)
        k += 1
except EOFError:
    pass

print gif

done = {}
print "populated..."
beep = [int(127*(math.cos(2*math.pi*440*T/8192))) for T in range(1200)]
blankBeep = [-128 for T in range(1200)]
blank = [-128]*(stepTime*8192-1200)

for i in range(sz[0]):
    for j in range(sz[1]):
        toWrite = [0]*length*8192*stepTime
        fname = str(i+1) + '_' + str(j+1) + '.wav'
        for k in range(1,length):
            indStart = (k-1)*8192*stepTime
            indEnd = k*8192*stepTime
            if(abs(gif[i][j][k-1] - gif[i][j][k]) > 0):
                toWrite[indStart:indStart + 1200] = beep;
            else:
                toWrite[indStart:indStart + 1200] = blankBeep;
            toWrite[indStart + 1200:indEnd] = blank;
        done[fname] = toWrite
print "writing files..."
for elt in done:
    cur = done[elt]
    newStr = ""
    for i in cur:
        newStr = newStr + (struct.pack("<b",i))
    wavFile = wave.open('wavs/' + elt, 'w')
    wavFile.setparams((1, 1, 8192, len(newStr), 'NONE', 'not compressed'))
    wavFile.writeframes(newStr)
    
target = open('wavs/size.txt', 'w')
target.write(str(sz[0]))
target.write('\n')
target.write(str(sz[1]))
target.close()

print "done!"





