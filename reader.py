#!/usr/bin/env python

print('Starting...')

import wave, struct, math, sys
from PIL import Image

import matplotlib.pyplot as plt

SAMPLERATE = 44100
CHIMELENGTH = 44100

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
length = get_gif_num_frames(filename) + delay/stepTime

gif = []
#initialize gif array
for i in range(sz[0]):
    gif.append([])
    for j in range(sz[1]):
        gif[i].append([765]*(length))

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

chime = wave.open('bell_short.wav', 'r')
beep_boop = chime.readframes(CHIMELENGTH)

# print(len(beep_boop))
beep = [struct.unpack("<h", beep_boop[i:i+2])[0] for i in range(0, len(beep_boop), 4)]
# print(len(unpacked))
# print(unpacked)
# print(len(unpacked))

# x = [i for i in range(len(unpacked))]
# y = unpacked
# print("about to plot")
# plt.plot(x,y)
# plt.show()

blankBeep = [0 for T in range(CHIMELENGTH)]
blank = [0]*(stepTime*SAMPLERATE-CHIMELENGTH)

for i in range(sz[0]):
    for j in range(sz[1]):
        toWrite = [0]*length*SAMPLERATE*stepTime
        fname = chr(i+65) + str(j+1) + '.wav'
        for k in range(1,length):
            indStart = (k)*SAMPLERATE*stepTime
            indEnd = k*SAMPLERATE*stepTime
            if(abs(gif[i][j][k-1] - gif[i][j][k]) > 0):
                toWrite[indStart:indStart + CHIMELENGTH] = beep;
            else:
                toWrite[indStart:indStart + CHIMELENGTH] = blankBeep;
            toWrite[indStart + CHIMELENGTH:indEnd] = blank;
        done[fname] = toWrite
print "writing files..."
for elt in done:
    cur = done[elt]
    newStr = ""
    for i in cur:
        newStr = newStr + (struct.pack("<h",i))
    wavFile = wave.open('wavs/' + elt, 'w')
    wavFile.setparams((1, 2, SAMPLERATE, len(newStr), 'NONE', 'not compressed'))
    wavFile.writeframes(newStr)
    # plt.plot([i for i in range(len(cur))], cur)
    # plt.show()
    
target = open('wavs/size.js', 'w')
target.write('dim_x = ' + str(sz[0]) + ';\n')
target.write('dim_y = ' + str(sz[1]) + ';')
target.close()

print "done!"





