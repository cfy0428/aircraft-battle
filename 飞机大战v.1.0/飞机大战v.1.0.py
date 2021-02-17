import pygame
import random
import math 
import os

p = pygame

#1. 初始化界面
p.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = p.display.set_mode((1000, 1000))
p.display.set_caption('飞机大战v.1.0')
icon = p.image.load('ufo.png')
p.display.set_icon(icon)
bgImg = p.image.load('bg.png')

#添加背景音效
p.mixer.music.load('bg.wav')
bao_sound = p.mixer.Sound('exp.wav')#创建射中音效
shut_sound = p.mixer.Sound('laser.wav')


p.mixer.music.play(-1) #单曲循环

textf = None	

#5.飞机
playerImg = p.image.load('player.png')
playerX = 400 #玩家的X坐标
playerY = 500 #玩家的Y坐标
playerStepx = 0 
playerStepy = 0
#玩家移动的速度

bg1 = -1000
bg2 = 0
bgstep = 1

#分数
score = 0
scorea = 0
golds = 0

levels = 1
lives = 100
bullet_timetick = 6
Text = None

key_using = False

font = p.font.SysFont('华文宋体',24) #宋体

timer = p.time.Clock()
timetick =0

level_timetick = 0
level_enemies_now = 0

bullet_hit_area = 0
extra_bullet_num = 0
real_bullet_timetick = 6

store1 = False
store2 = False
store3 = False
store4 = False

rage_mode = False

def textprint(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen = pygame.display.get_surface()
    screen.blit(imgText, (x,y))

def textprint2(textname,textname2,textfond,textcolor,screen):
    textname = textfond.render(textname, True,textcolor)
    textname2 = textname.get_rect()
    textname2.centerx = screen.get_rect().centerx
    textname2.centery = screen.get_rect().centery
    screen.blit(textname, textname2)


def show_text():
	global textf
	if lives > 0:
		texta = f"分数: {scorea+timetick}"
		textb = f"金币数：{golds}"
		textc = f"关卡：{levels}"
		textd = f"剩余敌人：{len(enemies)}"
		texte = f"生命:{lives}"
		if lives <= 20 and scorea+timetick >=40000:
			textf = "临死的倔强：狂暴模式"
		
	else:
		texta = "游戏结束"
		textb = f"你的分数是：{scorea+timetick}"
		textc = f"通关数：{levels}"
		textd = "按空格键或鼠标左键重新开始"
		texte = None
		textf = None
	textprint(font,600,10,texta)
	textprint(font,600,40,textb)
	textprint(font,600,70,textc)
	textprint(font,600,100,textd)
	textprint(font,600,130,texte)
	textprint(font,600,160,textf)



def store():
	global bullet_timetick,bullet_hit_area,store1,store2,store3,store4,golds,real_bullet_timetick,extra_bullet_num
	if bullet_timetick > 3:
		golds_inneed1 = int(((6.5-bullet_timetick)*2)**2*5+50)
		textg2 = f"需要金币：{golds_inneed1}  提升：{bullet_timetick}—{bullet_timetick-0.5} "
		if store1:
			if golds - golds_inneed1 > 0:
				bullet_timetick -= 0.5
				real_bullet_timetick -= 0.5
				golds -= golds_inneed1
			store1 = False
	else:
		if rage_mode:textg2 = f"狂暴模式中，暂不支持升级"
		else:textg2 = f"该技能已满级"
	textg1 = f"增加子弹发射频率（A）"			
	textprint(font,600,300,textg1)
	textprint(font,600,330,textg2)
	
	if bullet_hit_area < 50:
		golds_inneed2 = ((bullet_hit_area+10)//10)**2*5+50
		texth2 = f"需要金币：{golds_inneed2}  提升：{bullet_hit_area}—{bullet_hit_area+10}"
		if store2:
			if golds - golds_inneed2 > 0:
				bullet_hit_area += 10
				golds -= golds_inneed2
			store2 = False
	else:texth2 = f"该技能已满级"
	texth1 = f"增加子弹爆炸范围（S）"
	textprint(font,600,400,texth1)
	textprint(font,600,430,texth2)

	if extra_bullet_num < 5:
		golds_inneed3 = (extra_bullet_num+1)**2*5+50
		texti2 = f"需要金币：{golds_inneed3}  提升：{extra_bullet_num}—{extra_bullet_num+1}"
		if store3:
			if golds - golds_inneed3 > 0:
				extra_bullet_num += 1
				golds -= golds_inneed3
			store3 = False
	else:texti2 = f"该技能已满级"
	texti1 = f"增加额外子弹（D）"
	textprint(font,600,500,texti1)
	textprint(font,600,530,texti2)

	if store4:
		if golds - 50 > 0:
			enemies.clear()
			bullets_bye.clear()
			bao_sound.play()
			golds -= 50
			store4 = False
	textj1 = f"世界核平(F)"
	textj2 = f"需要金币：50"
	textprint(font,600,600,textj1)
	textprint(font,600,630,textj2)



	
	
		

	

def timeticks():
	global timetick,bullet_timetick,rage_mode
	if lives > 0:
		timetick += 1
	if lives <= 20 and scorea+timetick >40000 :
		bullet_timetick = 1
		rage_mode = True
	if timetick % bullet_timetick <= 0.5:
		bullets.append(Bullet())
	if timetick % 150 == 0:
		for x in range(extra_bullet_num):
			extra_bullets.append(Extra_bullet())
	


	

#游戏结束


over_font = p.font.SysFont('华文宋体', 64)

def check_is_over():
	if lives <= 0:
		enemies.clear()
		bullets.clear()
		bullets_bye.clear()

def show_bg():
	global bg1,bg2
	bg1 += bgstep+levels//2
	bg2 += bgstep+levels//2
	if bg1 >= 1000:
		bg1 = -1000
	if bg2 >= 1000:
		bg2 = -1000
	screen.blit(bgImg,(0,bg1))
	screen.blit(bgImg,(0,bg2))

def level():
	global levels,level_timetick,level_enemies_now
	level_enemies_all = (levels**2)*5
	level_newtime = random.randint(50-3*levels,100-3*levels)
	if level_newtime<30:level_newtime=30
	level_enemies_new = 10 + levels**2
	level_timetick += 1
	if level_timetick % level_newtime == 0 and level_enemies_now+level_enemies_new < level_enemies_all:
		level_enemies_num = random.randint(levels-1,levels+1)
		if level_enemies_num>5:level_enemies_num=5
		for x in range(level_enemies_num):
			enemies.append(Enemy())
			level_enemies_now += 1
	if enemies == [] and level_enemies_now+level_enemies_new >= level_enemies_all:
		level_enemies_now = 0
		level_timetick = 0
		levels += 1




#9. 添加敌人
number_of_enemies = 10 #敌人的数量
#敌人类
class Enemy():
	def __init__(self):
		self.sizenum = random.randint(1,27)
		self.x = random.randint(200, 400)
		self.y = random.randint(-250, 0)
		self.timetick = 0

		if self.sizenum == 1:
			self.img = p.image.load('enemy3.png')
			self.size = 256
			self.live = 9
			self.stepx = random.randint(1,3)/4+levels//4
			self.stepy = random.randint(2,6)/4+levels//2
			self.type = 3
		elif self.sizenum >=2 and self.sizenum <= 6:
			self.img = p.image.load('enemy2.png')
			self.size = 128
			self.live = 4
			self.stepx = random.randint(1,3)/2+levels//2
			self.stepy = random.randint(2,6)/2+levels
			self.type = 2
		else:
			self.img = p.image.load('enemy.png')
			self.size = 64
			self.live = 1
			self.stepx = random.randint(1,3) +levels
			self.stepy = random.randint(2,6) +levels*2
			self.type = 1

	
	def peng (self):
		global lives,playerX,playerY
		if distance(self.x,self.y,playerX,playerY) < 40:
			self.x = -10000
			lives -= 20
			bao_sound.play()
	

enemies = [] #保存所有的敌人d
for i in range(number_of_enemies):
	enemies.append(Enemy())


def reset_game():
	global timetick,score,lives,playerX,playerY,playerStep,scorea,levels,bullet_timetick,level_timetick,level_timetick,rage_mode,real_bullet_timetick
	timetick = 0
	score = 0
	scorea = 0
	lives = 100
	playerX = 400
	playerY = 900 
	playerStep = 0
	levels = 1
	bullet_timetick = 6
	level_timetick = 0
	level_timetick = 0
	real_bullet_timetick = 6
	rage_mode = False
	for i in range(number_of_enemies):
		enemies.append(Enemy())


#两个点之间的距离
def distance(bx, by, ex, ey):
	a = bx - ex
	b = by - ey
	return math.sqrt(a*a + b*b) #开根号

class bullet_bye:
	def __init__(self,xpos,ypos):
		self.img = p.image.load('bullet_bye.bmp')
		self.colorkey = self.img.get_at((0,0))
		self.img.set_colorkey(self.colorkey)
		self.x = xpos
		self.y = ypos
		self.stepx = (random.randint(10,50)+score)//10
		self.stepy = (random.randint(10,50)+score)//10
		if self.stepx > 5 :self.stepx = 5
		if self.stepy > 5 :self.stepy = 5
	

	def hit(self):
		global lives
		if distance(self.x+5,self.y+5,playerX+32,playerY+32) < 30:
				bao_sound.play()
				self.x = -10000
				lives -= 5

def fire ():
	for e in enemies:
		e.timetick += 1 
		time = random.randint(30,90)-(levels**2)
		if time < 10:time = 10
		if e.timetick % time == time-1:
			be = bullet_bye(e.x+e.size/2-5,e.y-5)
			bullets_bye.append(be)




#子弹类
class Bullet():
	def __init__(self):
		self.img = p.image.load('bullet.png')
		self.x = playerX + 16 #(64-32)/2
		self.y = playerY + 10
		self.step = 10 + levels * 2 #子弹移动的速度
	#击中
	def hit(self):
		global score,scorea,bullet_timetick,golds,rage_mode,textf
		for e in enemies:
			if(distance(self.x+16, self.y+16, e.x+e.size/2, e.y+e.size/2) < 30*e.size/64+bullet_hit_area):
				#射中啦
				shut_sound.play()
				e.live -=1
				shut = True
				if e.live == 0:
					scorea += (e.type**2)*300
					golds += (e.type**2)
					choose = random.randint(1,20)
					if choose == 1:
						bullet_timetick = real_bullet_timetick
						textf = None
						rage_mode = False
						g = gift(e.x+e.size/2-16,e.y+e.size/2-16)
						gifts.append(g)
					score += 1
					enemies.remove(e)
				if shut:
					self.x = -10000


class Extra_bullet():
	def __init__(self):
		self.img = p.image.load("extra_bullet.bmp")
		self.x = playerX + random.randint(-30,52)
		self.y = playerY + 10
		self.stepx = random.randint(-5,5)
		self.stepy = -random.randint(2,5)
		
	def hit(self):
		global score,scorea,golds,bullet_timetick,rage_mode,textf
		for e in enemies:
			if(distance(self.x+5, self.y+5, e.x+e.size/2, e.y+e.size/2) < 30*e.size/64+bullet_hit_area):
				shut_sound.play()
				scorea += (e.type**2)*300
				golds += (e.type**2)
				choose = random.randint(1,20)
				if choose == 1:
					bullet_timetick = real_bullet_timetick
					textf = None
					rage_mode = False
					g = gift(e.x+e.size/2-16,e.y+e.size/2-16)
					gifts.append(g)
				score += 1
				enemies.remove(e)
				for be in bullets_bye:
					if distance(self.x+5,self.y+5,be.x+5,be.y+5) < 5+bullet_hit_area:
						be.x = -10000
					self.x = -10000
				
					
					



		


	
class gift():
	def __init__(self,xpos,ypos):
		self.img = p.image.load("gift.png")
		self.x = xpos
		self.y = ypos
		self.step = 1 + levels//2
		
	def hit(self):
		global lives,bullet_timetick,textf,rage_mode
		if distance(self.x+16,self.y+16,playerX+32,playerY+32) < 30:
			self.x = -10000
			choose = random.randint(1,4)
			if choose == 1:
				lives += 20
				if lives > 100:
					lives = 100
				textf = "你获得了20生命值!"
			if choose == 2:
				enemies.clear()
				textf = "清除全屏敌人!"
			if choose == 3:
				bullets_bye.clear()
				textf = "清除全屏敌军子弹"
			if choose == 4:
				bullet_timetick = 1
				textf = "狂暴模式"
				rage_mode = True
			

	
				


bullets = [] #保存现有的子弹
bullets_bye = []
gifts = []
extra_bullets = []


#显示并移动子弹
def show_bullets():
	for b in bullets:
		screen.blit(b.img, (b.x, b.y))
		b.hit() #看看是否击中了敌人
		b.y -= b.step #移动子弹
		#判断子弹是否出了界面，如果出了就移除掉
		if b.y < 0:
			b.x =-10000
		

def show_bullets_bye():
	for be in bullets_bye:
		screen.blit(be.img, (be.x, be.y))
		be.hit() #看看是否击中了敌人
		be.x += be.stepx 
		be.y += be.stepy #移动子弹
		#判断子弹是否出了界面，如果出了就移除掉
		if be.y > 1000:be.x =-10000
		if be.x < 0:be.stepx = -be.stepx
		if be.x > 590:be.stepx = -be.stepx

def show_gifts():
	for g in gifts:
		screen.blit(g.img,(g.x,g.y))
		g.hit()
		g.y += g.step

def show_extra_bullets():
	for eb in extra_bullets:
		screen.blit(eb.img,(eb.x,eb.y))
		eb.hit()
		eb.x += eb.stepx 
		eb.y += eb.stepy #移动子弹
		#判断子弹是否出了界面，如果出了就移除掉
		if eb.y > 1000:eb.x =-10000
		if eb.x < 0:eb.stepx = -eb.stepx
		if eb.x > 590:eb.stepx = -eb.stepx

#显示敌人，并且实现敌人的移动和下沉
def show_enemy():
	for e in enemies:
		screen.blit(e.img,(e.x, e.y))
		e.x += e.stepx
		e.y += e.stepy
		if(e.x > 600-e.size or e.x < 0):
			e.stepx *= -1
		if e.y > 1000:enemies.remove(e)
		e.peng()


def move_player():
	global playerX,playerY
	playerX += playerStepx
	playerY += playerStepy
	#防止飞机出界
	if not key_using:
		playerX = p.mouse.get_pos()[0] - 32
		playerY = p.mouse.get_pos()[1] - 32
	if playerX > 536:playerX = 536
	if playerX < 0:playerX = 0	
	if playerY > 936:playerY = 936
	if playerY < 0:playerY = 0	

	



#2. 游戏主循环
running = True
while running:
	show_bg()
	for event in p.event.get():
		if event.type == p.QUIT:
			running = False
		#通过键盘事件控制飞机的移动
		if event.type == p.KEYDOWN: #按下就移动
			if event.key == p.K_ESCAPE:
				running = False
			if event.key == p.K_RIGHT:
				playerStepx = 10
				if not key_using:
					key_using = True
			elif event.key == p.K_LEFT:
				playerStepx = -10
				if not key_using:
					key_using = True

			if event.key == p.K_UP:
				playerStepy = -10
				if not key_using:
					key_using = True
			elif event.key == p.K_DOWN:
				playerStepy = 10
				if not key_using:
					key_using = True

			if event.key == p.K_SPACE:
				if lives <= 0:reset_game()
			
			if event.key == p.K_a:
				store1 = True
			
			if event.key == p.K_s:
				store2 = True
			
			if event.key == p.K_d:
				store3 = True

			if event.key == p.K_f:
 				store4 = True


		if event.type == p.MOUSEBUTTONDOWN:
			if p.mouse.get_pressed()[0]:
				if lives <= 0:reset_game()

			if p.mouse.get_pressed()[2]:
				if key_using:
					key_using = False

		if event.type == p.KEYUP: #抬起来就不动
			playerStepx = 0	
			playerStepy = 0



	new_time = 100 - (score*5)
	if new_time < 10:new_time = 10

	timer.tick(30)
	timeticks()
	p.draw.rect(screen, (0,0,0), (600,0,400,1000))
	if lives >0:
		move_player() #移动玩家
		show_enemy() #显示敌人
		show_bullets_bye()
		show_bullets() #显示子弹
		fire()
		show_gifts()
		store()
		show_extra_bullets()
	screen.blit(playerImg, (playerX, playerY))
	show_text() #显示分数
	check_is_over() #显示游戏结束字段
	level()
	p.display.update()


  