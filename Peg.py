#
# Pyxelを使った物理エンジン 釘ゲーム
# 「ゲームで学ぶJavaScript入門 増補改訂版」物理エンジンTiny2Dを参考にしました．
# cf. https://thinkit.co.jp/article/8467
#
# Apr 08, 2024 ver.1 (Pyxel/Pythonに移植しました)
#
import random
import math
import pyxel
from Engine import *

class Peg:

    def __init__( self ):

        # エンジン初期化 & イベントハンドラ設定
        self.engine = Engine(-20, -20, 160, 160, 0, 9.8)
        
        # 壁
        r = RectangleEntity(-10, 0, 20, 100)
        r.color = 2 # 紫色
        self.engine.entities.append(r)

        r = RectangleEntity(110, 0, 20, 100)
        r.color = 2 # 紫色
        self.engine.entities.append(r)
        
        # 釘
        for i in range(9):
            for j in range(8 + i % 2):
                x = (j * 10 + 25) - 5 * (i % 2)
                r = CircleEntity(x, i * 10 + 20, 1, BodyStatic)
                r.onhit = self.__callback
                r.color = 12 # 青色
                self.engine.entities.append(r);

        # その他(Timer)の初期化
        self.dir = math.pi / 2 # ラジアン(0からπまで)
        self.score = 0
        self.elapsed = 0
        self.timer = True # On
        self.cannon = [ [-4,-2],[6,-2],[6,2],[-4,2],[-4,-2] ]
        
        # Pyxel初期化
        pyxel.init( 120, 120, title="Peg", fps=30)
        self.__set_sound()
        pyxel.run(self.update, self.draw)

    # コールバック
    def __callback(self, me, peer):
        if (me.color == 12): # 青色
            me.color = 14 # 赤色
            self.score += 1
            self.__play()
        elif (me.color == 14): # 赤色
            me.color = 11 # 緑色
            self.score += 1
            self.__play()
        elif (me.color == 11): # 緑色
            me.color = 9 # 橙色
            self.score += 1
            self.__play()
            
        if (self.score >= 76 * 3 and self.timer):
            self.timer = False # 停止

    # 効果音
    def __play(self):
        pyxel.play(self.ch1, [self.sound00], loop=False)
        self.is_play = True
    def __stop(self):
        pyxel.stop()
        self.is_play = False
    def __set_sound(self):
        self.ch1 = 0
        self.sound00 = 0
        self.notes = "c2d2e2f2g2a2b2c3"
        self.tones = "p"
        self.volumes = "6"
        self.effects = "n"
        self.speed = 5
        pyxel.sounds[self.sound00].set(
            self.notes,
            self.tones,
            self.volumes ,
            self.effects ,
            self.speed,
        )
        
    def update( self ):
        if pyxel.btnp(pyxel.KEY_SPACE): # 連射なし
#        if pyxel.btn(pyxel.KEY_SPACE): # 連射あり
            vx = 2 * math.cos(self.dir) # 速度(X方向)
            vy = 2 * math.sin(self.dir) # 速度(y方向)
            ball = CircleEntity(60+vx*3, 0+vy*3, 2, BodyDynamic, 0.9)
            ball.velocity.x = vx
            ball.velocity.y = vy
            ball.color = random.randint(2,15) # 乱数
            self.engine.entities.append(ball)
        elif pyxel.btn(pyxel.KEY_LEFT) and self.dir < math.pi:
            self.dir += math.pi / 20
        elif pyxel.btn(pyxel.KEY_RIGHT) and self.dir > 0:
            self.dir -= math.pi / 20

        self.engine.step(0.01) # 物理エンジンの時刻を進める

    def draw( self ):
        # 背景クリア
        pyxel.cls(1)

        # 発射台描画
        rot = []
        for xy in self.cannon:
            rot.append([self.x_(xy[0],xy[1]),self.y_(xy[0],xy[1])])
        for n in range(len(rot)-1):
            pyxel.line(rot[n][0],rot[n][1],rot[n+1][0],rot[n+1][1],2)
        pyxel.fill( 60, 0, 2)

        # ボール・壁・釘の描画
        for e in self.engine.entities:
            if (e.shape == ShapeCircle):
                pyxel.circ(e.x,e.y,e.radius,e.color)
            elif (e.shape == ShapeLine):
                pyxel.line(e.x0,e.y0,e.x1,e.y1,e.color)
            elif (e.shape == ShapeRectangle):
                pyxel.rect(e.x,e.y,e.w,e.h,e.color)

        # 各種情報表示
        if self.timer: 
            self.elapsed = pyxel.frame_count / 30
        else:
            pyxel.text(44, 60, "CLEARED!!" , 8)

        # 点数表示
        pyxel.text(12, 110, "Time: " + f"{self.elapsed:.0f}", 6)
        pyxel.text(58, 110, "Score: " + f"{self.score:d}" + "/228", 6)

    # 座標回転
    def x_( self, x, y ): return( x * math.cos(self.dir) - y * math.sin(self.dir) + 60)
    def y_( self, x, y ): return( x * math.sin(self.dir) + y * math.cos(self.dir) )
        
# Main
Peg()

# End of Peg.py
