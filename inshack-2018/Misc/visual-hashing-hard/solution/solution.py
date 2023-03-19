from hashlib import sha1
from math import floor

colorCode = ['1B9C0E', 'B55855', 'BC6578', 'A047C9']

target = list()
for a in range(len(colorCode)):
    for b in range(3):
        target.append(int(colorCode[a][b*2 : b*2+2], 16))


loopN = 0
while True:
    print('%.2f'%(loopN / (26**5 - 1) * 100) + '%')
    guess = ''
    tmpLoopN = loopN
    while True:
        guess += chr(ord('a') + tmpLoopN % 26)
        tmpLoopN = floor(tmpLoopN / 26)
        if tmpLoopN == 0:
            break
    while len(guess) < 5:
        guess += 'a'
    guess = guess[::-1]

    hashed = sha1('INSA{{{}}}'.format(guess).encode('utf-8')).hexdigest()  # lol
    for i in zip(target, [int(hashed[x*2 : x*2+2], 16) for x in range(floor(len(hashed) / 2))]):
        if abs(i[0] - i[1]) > 4:  # ??
            break
    else:  # No break in for loop
        print('INSA{{{}}}'.format(guess))
        break

    if guess == 'zzzzz':
        print('No solution found!')
        break
    loopN += 1
