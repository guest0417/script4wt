U='r'
T=True
S=bytes
R=open
Q=hex
F='utf-8'
E='pause'
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as I
from Crypto.Hash import MD5
from binascii import a2b_hex as G
from script4win10_repair_min import export as J
import string,random,uuid as H,datetime as K,os as B,json,sys as C,logging as D
A=D.getLogger('license') 
A.setLevel(D.INFO)
handler=D.StreamHandler()
L=D.Formatter(fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',datefmt='%H:%M:%S')
handler.setFormatter(L)
A.addHandler(handler)
def M():
	L='ExpireDate';D=P();G=K.datetime.now().strftime('%Y%m%d');F=Q(H.getnode());I=F+'#'+D[L];J=D['Sign']
	if F!=D['MAC']:A.warn('Invalid host');B.system(E);C.exit(1)
	elif D[L]<G:A.warn('License is expired!');B.system(E);C.exit(1)
	elif N(J,I):A.info('License check passed!');return T
	else:A.warn('License is modified or it does not belong to you');B.system(E);C.exit(1)
def N(signature,data):A=R('pub_key.pem',U);B=RSA.importKey(A.read());C=O(data);D=I.new(B);A.close();return D.verify(C,G(signature))
def O(data):return MD5.new(data.encode(F))
def P():
	A={};B='./license.dat'
	with R(B,U)as C:A=json.load(C)
	return A
def V(content):
	H=AES.new(S(expire_date,encoding=F)*2,AES.MODE_CBC,S(expire_date,encoding=F)*2);D=H.decrypt(G(content.encode(F)))
	try:D=D.decode(F)
	except:A.warn('License is modified!');B.system(E);C.exit(1)
	return D
if __name__=='__main__':
	if not B.path.isfile(B.getcwd()+'\\license.dat'):A.info('请将以下字符串及订单号发送给服务提供商，待客服人员确认无误后将为阁下颁发使用证书:\n{}'.format(Q(H.getnode())));B.system(E);C.exit(1)
	while T:M();J()