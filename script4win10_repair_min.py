_c='pause'
_b='script started'
_a='Windows:///?title_re=War Thunder*'
_Z='/log'
_Y='battle quited'
_X='LEFT'
_W='./img/wtlogo.png'
_V='./img/rtb.png'
_U='not in battle'
_T='./img/plane.png'
_S=False
_R='text acquired: {}'
_Q='chi_sim'
_P='in battle'
_O='./img/confirm1.png'
_N='./img/start.png'
_M='ESCAPE'
_L='D'
_K='A'
_J='./img/crew.png'
_I='./img/join.png'
_H='UP'
_G='LALT'
_F='S'
_E='8'
_D='7'
_C='ENTER'
_B='DOWN'
_A=True
__author__='guest0417'
from genericpath import exists
from re import X
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.win.win import *
from airtest.aircv import *
import numpy as np,pytesseract,cv2,traceback,os,sys,logging,datetime,time,json,win32api
logger=logging.getLogger('airtest')
logger.setLevel(logging.INFO)
loc_logger=logging.getLogger('main')
loc_logger.setLevel(logging.INFO)
handler=logging.StreamHandler()
formatter=logging.Formatter(fmt='[%(asctime)s][%(levelname)s]<%(name)s> %(message)s',datefmt='%H:%M:%S')
handler.setFormatter(formatter)
loc_logger.addHandler(handler)
width=0
height=0
flag=_A
turn=_A
back=_A
hit_turn=_A
ST.FIND_TIMEOUT_TMP=0.8
ST.FIND_TIMEOUT=0.8
testdata_dir_config='--tessdata-dir "'+os.getcwd()+'\\Tesseract-OCR\\tessdata"'
class LoopException(Exception):0
class LicenseCheck(Exception):0
def parse_setting_file():
	setting_dic={};setting_file='./settings.txt'
	with open(setting_file,'r',encoding='UTF-8')as LF:setting_dic=json.load(LF)
	return setting_dic
setting_dic=parse_setting_file()
loc_logger.info('setting: {}'.format(setting_dic))
def click(key):loc_logger.info('clicked: {}'.format(key));key_press(key);sleep(0.1);key_release(key)
def init():
	loc_logger.info('initialising...');temp=0
	while exists(Template('./img/6.png',threshold=0.95)):
		temp+=1
		if temp>=10:raise LoopException
		click('6');sleep(0.5)
	temp=0
	while exists(Template('./img/7.png',threshold=0.95)):
		temp+=1
		if temp>=10:raise LoopException
		click(_D);sleep(0.5)
	temp=0
	while exists(Template('./img/8.png',threshold=0.95)):
		temp+=1
		if temp>=10:raise LoopException
		click(_E);sleep(0.5)
def init_speed():
	A='W';global setting_dic;loc_logger.info('speed initialised');key_press(A);sleep(1.5);key_release(A)
	for i in range(int(setting_dic['speed'])):click(_F)
def check_repair():
	loc_logger.info('checking repair');global back;global hit_turn;fire=exists(Template('./img/fire.png',threshold=0.45,rgb=_A))
	if fire and exists(Template('./img/6active.png',threshold=0.6,rgb=_A)):click('6');click('G');click(_D);click(_E);key_press(_F);key_press(_D);key_press(_E);sleep(3.5);key_release(_F);key_release(_D);key_release(_E);back=_A
	elif fire:0
	elif exists(Template('./img/8active.png',threshold=0.6,rgb=_A)):click(_E)
	elif exists(Template('./img/7active.png',threshold=0.6,rgb=_A)):
		click(_D)
		if hit_turn==_A:key_press(_K);sleep(3.0);key_release(_K);hit_turn=not hit_turn
		else:key_press(_L);sleep(3.0);key_release(_L);hit_turn=not hit_turn
	elif back==_A:init_speed();back=not back
def check_crash(text):
	global flag;global setting_dic;loc_logger.info('checking crash')
	if'返回'in text or'战场'in text or'水深'in text or'不足'in text or'放'in text or'弃'in text or'载'in text or'具'in text or'倒'in text or'计'in text or'时'in text:
		loc_logger.info('crashing');key_press(_F);sleep(int(setting_dic['crash_s']))
		if flag==_A:key_press(_K)
		else:key_press(_L)
		sleep(int(setting_dic['crash_s_turn']))
		if flag==_A:key_release(_K)
		else:key_release(_L)
		key_release(_F);init_speed();flag=not flag
	return _A
def check_target():
	loc_logger.info('checking target');temp=0
	while not exists(Template('./img/target.png',threshold=0.9)):
		temp+=1
		if temp>=10:raise LoopException
		click('E');sleep(0.5)
	return _A
def check_weapon():
	B='3';A='2';loc_logger.info('checking weapon');temp=0
	while not exists(Template('./img/AA.png'))and not exists(Template('./img/secondary.png')):
		temp+=1
		if temp>=10:raise LoopException
		key_press(_G);key_press(A);sleep(0.1);key_release(A);key_release(_G);key_press(_G);key_press(B);sleep(0.1);key_release(B);key_release(_G);sleep(0.1);break
	return _A
def check_purchase():
	D='./img/purchase.png';C='RIGHT';B='./img/researchable.png';A='./img/navy.png';loc_logger.info('checking purchase')
	if not exists(Template(A,threshold=0.9)):touch(Template('./img/tech_tree.png'))
	sleep(0.5)
	for i in range(3):
		touch(Template(A,threshold=0.9));touch(Template(B,threshold=0.9));click(_B)
		for i in range(i):click(C)
		while _A:
			if exists(Template('./img/choose_crew.png',threshold=0.95))or exists(Template('./img/res.png',threshold=0.95)):click(_B)
			elif exists(Template(D,threshold=0.95)):
				touch(Template(D,threshold=0.95));touch(Template('./img/purchase_confirm.png'));sleep(0.5);touch(Template('./img/crew_cancel.png'));touch(Template(B,threshold=0.9));click(_B)
				for i in range(i):click(C)
			else:break
		for i in range(10):click(_H)
def start():
	G.DEVICE.set_foreground();temp=0
	while not exists(Template(_N,threshold=0.95)):
		temp+=1
		if temp>=10:raise LoopException
		loc_logger.info('awaiting to start a new game...');sleep(5)
	click(_C);sleep(0.5)
	if exists(Template(_N,threshold=0.95)):click(_C)
def join():
	G.DEVICE.set_foreground()
	while not exists(Template(_I,threshold=0.95)):
		if exists(Template(_O,threshold=0.95)):raise LoopException
		sleep(5)
	sleep(int(setting_dic['respawn_delay']));click(_C);sleep(0.5)
	if exists(Template(_I,threshold=0.95)):click(_C)
	loc_logger.info('respawned')
def battle():
	global turn;global width;global height;depth=0;fail=0;G.DEVICE.set_foreground()
	while not exists(Template(_J)):sleep(5)
	while _A:
		screen=G.DEVICE.snapshot()
		if depth==0:loc_logger.info(_P);init_speed();click('Z');x,y=win32api.GetCursorPos();G.DEVICE.mouse_move((x,y-10*height));check_weapon();check_target()
		if depth%10==0:init()
		if turn==_A:check_repair()
		depth+=1;local=aircv.crop_image(screen,(width/5*2,height/2,width/5*3,height/3*2));hsv=cv2.cvtColor(local,cv2.COLOR_BGR2HSV);lower=np.array([0,43,46]);higher=np.array([10,255,255]);mask=cv2.inRange(hsv,lower,higher);sleep(0.1);text=pytesseract.image_to_string(mask,lang=_Q,config=testdata_dir_config);loc_logger.info(_R.format(text))
		if turn==_S:check_crash(text)
		turn=not turn
		if not exists(Template(_J))and not exists(Template(_T)):
			fail+=1
			if fail>=2:break
			else:0
	loc_logger.info(_U);G.DEVICE.set_foreground();sleep(3.0)
	if exists(Template(_V,threshold=0.9))or exists(Template(_I,threshold=0.9)):
		temp=0
		while not exists(Template(_W,threshold=0.9)):
			temp+=1
			if temp>=10:raise LoopException
			G.DEVICE.set_foreground();click(_M);sleep(0.5)
		sleep(0.1);click(_B);sleep(0.1);click(_B);sleep(0.1);click(_H);sleep(0.1);click(_H)
		for i in range(6):click(_B);sleep(0.1)
		click(_C);sleep(0.1);click(_X);sleep(0.1);click(_C);quit()
	else:quit()
	loc_logger.info(_Y)
def battle_mult():
	global turn;global width;global height;depth=0;fail=0;G.DEVICE.set_foreground()
	while not exists(Template(_J)):sleep(5)
	while _A:
		screen=G.DEVICE.snapshot()
		if depth==0:loc_logger.info(_P);init_speed();click('Z');x,y=win32api.GetCursorPos();G.DEVICE.mouse_move((x,y-10*height));check_weapon();check_target()
		if depth%10==0:init()
		if turn==_A:check_repair()
		depth+=1;local=aircv.crop_image(screen,(width/5*2,height/2,width/5*3,height/3*2));hsv=cv2.cvtColor(local,cv2.COLOR_BGR2HSV);lower=np.array([0,43,46]);higher=np.array([10,255,255]);mask=cv2.inRange(hsv,lower,higher);sleep(0.1);text=pytesseract.image_to_string(mask,lang=_Q,config=testdata_dir_config);loc_logger.info(_R.format(text))
		if turn==_S:check_crash(text)
		turn=not turn
		if not exists(Template(_J))and not exists(Template(_T)):
			sleep(5.0)
			if exists(Template(_I,threshold=0.9)):click(_C)
			else:
				fail+=1
				if fail>=2:break
				else:0
	loc_logger.info(_U);G.DEVICE.set_foreground();sleep(3.0)
	if exists(Template(_V,threshold=0.9)):
		temp=0
		while not exists(Template(_W,threshold=0.9)):
			temp+=1
			if temp>=10:raise LoopException
			G.DEVICE.set_foreground();click(_M);sleep(0.5)
		sleep(0.1);click(_B);sleep(0.1);click(_B);sleep(0.1);click(_H);sleep(0.1);click(_H)
		for i in range(6):click(_B);sleep(0.1)
		click(_C);sleep(0.1);click(_X);sleep(0.1);click(_C);quit()
	else:quit()
	loc_logger.info(_Y)
def quit():
	C='./img/improvement.png';B='confirm';A='./img/confirm.png';temp=0
	while not exists(Template(_N,threshold=0.95)):
		G.DEVICE.set_foreground();temp+=1
		if temp>=10:raise LoopException
		if exists(Template(A,threshold=0.9)):loc_logger.info(B);touch(Template(A,threshold=0.9))
		elif exists(Template(_O,threshold=0.9)):loc_logger.info(B);touch(Template(_O,threshold=0.9))
		elif exists(Template(C,threshold=0.9)):loc_logger.info('improvement');touch(Template(C,threshold=0.9))
		elif exists(Template('./img/close.png',threshold=0.8,rgb=_A)):loc_logger.info('close');click(_M)
		elif exists(Template('./img/research.png',threshold=0.9)):loc_logger.info('research');touch(Template('./img/research1.png',threshold=0.6))
		else:click(_M);sleep(3.0)
def main():
	A='respawn';global width;global height;global setting_dic;G.DEVICE.set_foreground();width,height=G.DEVICE.get_current_resolution();temp=time.time();click(_G)
	if exists(Template(_I,threshold=0.95)):
		join()
		if int(setting_dic[A])==0:battle()
		else:battle_mult()
	elif exists(Template(_J)):
		if int(setting_dic[A])==0:battle()
		else:battle_mult()
	else:0
	_time=0
	while time.time()-temp<43200:
		_time+=1
		if _time%int(setting_dic['purchase'])==0:check_purchase()
		quit();start();join()
		if int(setting_dic[A])==0:battle()
		else:battle_mult()
	quit();raise LicenseCheck
def export():
	try:
		if not cli_setup():auto_setup(__file__,logdir=os.getcwd()+_Z,devices=[_a])
		G.DEVICE.set_foreground();loc_logger.info(_b)
		while _A:
			try:main()
			except (AttributeError,TargetNotFoundError,LoopException):pass
			except LicenseCheck:return _A
	except Exception as e:loc_logger.error(e);traceback.print_exc()
	os.system(_c)
if __name__=='__main__':
	try:
		if not cli_setup():auto_setup(__file__,logdir=False,devices=[_a])
		G.DEVICE.set_foreground();loc_logger.info(_b)
		while _A:
			try:main()
			except (AttributeError,TargetNotFoundError,LoopException):pass
			except: pass
	except Exception as e:loc_logger.error(e);traceback.print_exc()
	os.system(_c)