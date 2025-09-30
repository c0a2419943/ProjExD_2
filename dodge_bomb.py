import os
import random 
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct : pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True 
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False 
    return yoko , tate
    
def gameover(screen):
    cover = pg.Surface((WIDTH, HEIGHT))
    cover.fill((0, 0, 0))
    cover.set_alpha(180)
    font = pg.font.SysFont(None, 56, bold=True)  
    txt = font.render("Game Over", True, (255, 255, 255))
    txt_r = txt.get_rect(center=(WIDTH//2, HEIGHT//2))
    cry = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.0)
    left_r  = cry.get_rect(center=(WIDTH//2 - 200, HEIGHT//2))
    right_r = cry.get_rect(center=(WIDTH//2 + 200, HEIGHT//2))
    screen.blit(cover, (0, 0))
    screen.blit(cry, left_r)
    screen.blit(cry, right_r)
    screen.blit(txt, txt_r)
    pg.display.update()
    time.sleep(5)


def init_bb_imgs():
    bb_imgs = []
    for r in range(1, 11):  
        s = pg.Surface((20*r, 20*r))
        s.set_colorkey((0, 0, 0))
        pg.draw.circle(s, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(s)
    bb_accs = [a for a in range(1, 11)] 
    return bb_imgs, bb_accs

def get_kk_imgs():
    base = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_dict = {
        (0, 0):  base,                               
        (+5, 0): pg.transform.rotozoom(base,   0, 1),
        (-5, 0): pg.transform.rotozoom(base, 180, 1),
        (0, -5): pg.transform.rotozoom(base,  90, 1),   
        (0, +5): pg.transform.rotozoom(base, -90, 1),   
        (+5,-5): pg.transform.rotozoom(base,  45, 1),   
        (+5,+5): pg.transform.rotozoom(base, -45, 1),   
        (-5,-5): pg.transform.rotozoom(base, 135, 1),   
        (-5,+5): pg.transform.rotozoom(base, -135, 1),  
    }
    return kk_dict


def calc_orientation(org: pg.Rect, dst: pg.Rect, current_xy: tuple[float, float]) -> tuple[float, float]:
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery
    norm = (dx*dx + dy*dy) ** 0.5
    if norm == 0:
        return current_xy
    if norm < 300:
        return current_xy
    dx = dx / norm * 5
    dy = dy / norm * 5
    return dx, dy


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    bb_img = pg.Surface((20,20)) 
    pg.draw.circle(bb_img, (255, 0 , 0),(10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(20, WIDTH-20)
    bb_rct.centery = random.randint(20, HEIGHT-20)
    bb_imgs, bb_accs = init_bb_imgs()
    idx = 0
    bb_img = bb_imgs[idx]
    bb_rct = bb_img.get_rect(center=bb_rct.center)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
               sum_mv[0] += mv[0]
               sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = kk_imgs.get((sum_mv[0], sum_mv[1]), kk_imgs[(0, 0)])
        screen.blit(kk_img, kk_rct)
        idx = min(tmr // 500, 9)                
        bb_img = bb_imgs[idx]
        bb_rct = bb_img.get_rect(center=bb_rct.center)
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))
        avx = vx * bb_accs[idx]
        avy = vy * bb_accs[idx]
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

