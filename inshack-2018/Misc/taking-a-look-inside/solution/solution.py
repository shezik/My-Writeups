import base64
from scapy.all import rdpcap
from Crypto.Cipher import AES

pcapSessions = rdpcap('taking-a-look-inside.pcap').sessions()
packets = pcapSessions['TCP 192.168.56.101:60182 > 192.168.56.1:42042']

data = b''
for packet in packets:
    if packet.haslayer('Raw'):
        data += packet.getlayer('Raw').original

cipher = AES.new(b'd3Adb3Efc4Feb4Be', AES.MODE_ECB)

decryptedData = b''
while len(data) > 0:
    blockSize = int.from_bytes(data[0 : 4], "big")  # 4 bytes
    blockData = data[4 : blockSize+4]  # blockSize includes 'SCN|' and '|NCS'
    data = data[blockSize+4 : ]

    decryptedData = cipher.decrypt(base64.b64decode(blockData[4 : -4]))

with open('decrypted.bin', 'wb') as file:
    file.write(decryptedData)
    file.close()
