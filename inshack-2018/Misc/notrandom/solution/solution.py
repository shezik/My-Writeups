import pwn
from mt19937predictor import MT19937Predictor
import hashlib

class Solution:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.conn = None
        self.predictor = MT19937Predictor()
        self.state = {'blind': '', 'credits': '', 'commitment': ''}

    def connect(self):
        self.conn = pwn.remote(self.ip, self.port)

    def analyzeBlind(self, n=624):
        i = 0
        while i < n:
            print('{} of {}'.format(i + 1, n))
            self.conn.send('a')  # Any non-integer value
            self.recvAndAnalyze()
            blind = self.state['blind']
            if blind != '':
                self.predictor.setrandbits(int(blind), 32)
                i += 1

    def run(self):
        self.connect()
        print('Analyzing server-side Mersenne Twister RNG...')
        self.analyzeBlind()
        print('Bruteforcing jackpot value...')
        while True:
            self.bruteforceJackpot()

    def bruteforceJackpot(self):
        commitment = self.state['commitment']
        predictedBlind = self.predictor.getrandbits(32)
        for i in range(2**10):
            if commitment == hashlib.md5(str(i + predictedBlind).encode()).hexdigest():
                self.conn.send(str(i))
                self.recvAndAnalyze()
                print('Found jackpot: {}\tCurrent credits: {}'.format(i, self.state['credits']))
                break
        else:
            raise Exception('No solution found! Bad prediction?')

    def recvAndAnalyze(self):
        while True:
            line = self.conn.recvline(timeout=0.1).decode('utf-8')
            if line == '':
                break
            elif line.find('Commitment values : ') != -1 and line.find(' + ') != -1:
                self.state['blind'] = line[line.find(' + ') + len(' + ') : -1]
            elif line.find(' credits remaining') != -1:
                self.state['credits'] = line[len('You have ') : line.find(' credits remaining')]
            elif line.find('INSA{') != -1:
                raise Exception('Flag found!!! {}'.format(line[ : -1]))  # Print flag and terminate
            elif line.find('To be sure we are fair, here is the commitment of our future jackpot ') != -1:
                self.state['commitment'] = line[len('To be sure we are fair, here is the commitment of our future jackpot ') : -1]

if __name__ == '__main__':
    solution = Solution('127.0.0.1', 10002)
    solution.run()
