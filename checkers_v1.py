'''
The Game of American Checkers also called English draughts
This version allows only very simple moves.
- One move or jump per player turn.
- crowned piece can move in any direction but only one square at a time
Enjoy!

played on an 8x8 square board 
with twelve pieces on each side.
The pieces move and CAPTURE diagonally
They may only move forward until they reach the opposite end of the board
when they are CROWNEDed and may thereafter move and CAPTURE both backward and forward.
played by two opponents,  alternating moves on opposite sides of the game board
The pieces are traditionally black, red, or white
Enemy pieces are CAPTUREd by jumping over them.
darkest color moves first
first to get all the other pieces wins
'''
 
from graphics import *
 
BOXCOLOR = ["purple","pink" ]
PIECECOLOR = ["White","Red","Yellow","Black"]
ONE=0
TWO=1
CROWNED = 2
REGULAR=1
EMPTY = 0
NOPLAY = -1
NUMPIECES = 12
SQRS=8
BOX_W=50
BRD_W=BOX_W*SQRS
STATUS = 20
STATUS_MSG = ""
DIRECTION = [1,-1,0]
UP = 1
DOWN = -1
PLAYER = []
CAPTURE = []
TURN = TWO
SWAP = 1
SAME_PLACE = False
MULI_JUMP=False
FLYING=False
DEBUG2=False
DEBUG=False
GAME_OVER = False    
#-----------------------------------------------------------------

def main():
    play_checkers()
    
    
def play_checkers():    
    global TURN, GAME_OVER
    try:
        win = GraphWin("Display Window",BRD_W,BRD_W+STATUS)
        draw_board(win)
        init_PLAYERs(win)
        update_board(win)
        update_status(win)
        
        while GAME_OVER == False :
            
            if DEBUG2 : print("---PLAYER",TURN,end=": ")
            p = win.getMouse()
            col=int(p.getX()/50)
            row=int(p.getY()/50)
            if (col==7) & (row==0) : debug_show_window()
            if (col==0) & (row==7) : debug_show_capture()
            if DEBUG : print(" click at (",row,col,end=") ")
            if allowed_to_move(row,col) == True :  # PLAYERs TURN to move
                if move_checker(win, row, col) == False :
                    continue
            else:
                continue
            GAME_OVER = check_for_winner(win)
            TURN = SWAP - TURN
            update_status(win)
        print ("YOU WIN!" )
        print("click to quit")
        win.getMouse()
        win.close        
    except (IOError): 
        if DEBUG : print ("You Quit! or I died!" )
 
     
#-----------------------------------------------------------------
def update_status(win):
    global STATUS_MSG

    a = Point(0,BRD_W)
    b = Point(BRD_W,BRD_W+STATUS)
    rect = Rectangle(a,b)
    rect.setFill("White")
    rect.setOutline("White")
    rect.setWidth(1)  
    rect.draw(win)

    if GAME_OVER == False :
        STATUS_MSG= PIECECOLOR[TURN]+"'s turn."
        tiny_checker(win,BRD_W,STATUS,PIECECOLOR[TURN],STATUS)
    STATUS_MSG = STATUS_MSG+"     Score: "+PIECECOLOR[ONE]+"="+str(CAPTURE[ONE])+" "+PIECECOLOR[TWO]+"="+str(CAPTURE[TWO])
    if DEBUG2 : print (STATUS_MSG)

    p=Point(BRD_W/2,BRD_W+(STATUS/2))
    txt = Text(p,STATUS_MSG)
    txt.draw(win)
     
     
#-----------------------------------------------------------------
def check_for_winner(win):
    global STATUS_MSG
    ''' how does one win? '''
    for i in range(2) :
        if DEBUG2 : print("winner?",i,CAPTURE[i],NUMPIECES) 
        if CAPTURE[i]==NUMPIECES :
            STATUS_MSG =PIECECOLOR[i]+" Player Won!"
            return True
    return False
 
#-----------------------------------------------------------------
def move_checker(win, r, c):
    global PLAYER
    erase_checker(win,r,c) 
    ''' block to get next mouse click '''
    move_ok = False
    checker = PLAYER[TURN][r][c]
    PLAYER[TURN][r][c] = EMPTY
    if DEBUG : print("--(",TURN,") move FROM (",r,c,")",checker)  
    while (move_ok == False) :
        if DEBUG : print( "waiting for a click",end="")
        p = None
        while (p == None ) :
            ''' waiting for user to click in new place '''
            p = win.checkMouse()
        c2=int(p.getX()/50)
        r2=int(p.getY()/50)
        if DEBUG : print(" *click at (",r2,c2,end=") ")
        if (location_empty(r2,c2)==True) :
            if (direction_allowed(win,r,c,r2,c2,checker==CROWNED)==True) :
                move_ok = True
    ''' put the checker down '''
    checker = is_player_crowned(r2,c2, TURN, checker)
    draw_checker(win,r2,c2,PIECECOLOR[TURN],checker==CROWNED) 
    #  store new location of checker! 
    PLAYER[TURN][r2][c2] = checker
    if DEBUG : print("--(",TURN,") move TO (",r2,c2,")",checker,"=",PLAYER[TURN][r2][c2] )  
    if SAME_PLACE == True :
        return False
    return True
  
#-----------------------------------------------------------------
'''
    see if we can we make this move
    cant move more than 2 blocks no matter what
    can go back to same place
    can go one in any diagonal if crowned
    can go one in PLAYER direction
    can go 2 to CAPTURE in any direction if crowned
    can go 2 in PLAYER direction to CAPTURE
'''
def direction_allowed(win,r,c,r2,c2,crowned) :
    global SAME_PLACE
    d = DIRECTION[TURN]
    d1= r2 - r   # get the new direction and distance
    h1 =c2 - c
    ok = False
    SAME_PLACE = False
    if DEBUG : print ( "\tcan go d(", d, ") this is d1(", d1, ") from (", r,c, ") to (",r2,c2, end=") ") 
    if (abs(h1)>2) : # cant move horizontal more than 2
        if DEBUG : print("\tno,  too far horizontal")
    elif(abs(d1) >2)  : # cant jump diag more than 2
        if DEBUG : print("\tno,  too far vertical")
    elif ( (r==r2) & (c==c2) ) : # d1 was 0 request to put down in same place
        if DEBUG : print ( "\tyes, same place") 
        SAME_PLACE = True  #  dont let them loose a TURN they can go again
        ok = True
    elif (abs(d1)==1) & crowned :
        if DEBUG : print (" CROWNED, can go any direction")
        ok = True
        # must allow CAPTURE in any direction too!
    elif (d1 == d)  :   # going one in allowed direction
            if DEBUG : print ( "\tcan go", d1) 
            ok = True
    elif (d1 == d*2) | ((abs(d1)==2) & crowned):   
            # only can jump 2 if capturing a piece
            if DEBUG : print ( "\n\tcan only jump to CAPTURE (", d1,end=")") 
            if capture_checker(win,r,c,r2,c2) == True :
                if DEBUG : print ( "\tCAPTUREd / can go",d1) 
                ok = True
    if DEBUG : print("\tok(",ok,").")
    return ok
 
#-----------------------------------------------------------------
def is_player_crowned(r,c,turn,checker):
    limit = (SQRS-1)*(SWAP-turn)
    if DEBUG : print("Crown? p=",turn,"  at (",r,c,") crowned=",checker,end="")
    if (r==limit) : 
        checker = CROWNED
        if DEBUG : print(", yes crown it:",checker )
    else :
        if DEBUG : print(", No leave as is",checker )
    return checker
 
#-----------------------------------------------------------------
def capture_checker(win,r,c,r2,c2):
    global CAPTURE, PLAYER
    ok = False
    if DEBUG : print(" CAPTURE? ", r,c,r2,c2," PLAYER",TURN, end=":" )
    r1=r+((r2-r)/2)
    c1=c+((c2-c)/2)
    # debug_show_window()
    other=SWAP-TURN
    if DEBUG : print("\tjump over (",r1,c1,")c=",other,"(",PLAYER[other][int(r1)][int(c1)],")", end="")
    r1=int(r1)
    c1=int(c1)
    if PLAYER[other][r1][c1] > EMPTY :
        if DEBUG : print("\t\t took piece!")
        erase_checker(win,r1,c1) 
        CAPTURE[TURN] +=1
        PLAYER[other][r1][c1] = EMPTY
        ok = True
    elif DEBUG : print("\t no oponent.")
    # debug_show_window()
    return ok
 
#-----------------------------------------------------------------
def location_empty(r,c):
    if DEBUG : print( "\t? p1=",PLAYER[ONE][r][c],"p2=",PLAYER[TWO][r][c], end=" " )
    if (PLAYER[ONE][r][c] == EMPTY) & (PLAYER[TWO][r][c] == EMPTY) :
        if DEBUG : print (" empty" )
        return True
    else :
        if DEBUG : print (" not empty",)
        return False
    
#-----------------------------------------------------------------
def allowed_to_move(r,c):
    ok = False
    # it it the PLAYERs piece?
    if PLAYER[TURN][r][c] == EMPTY: # not PLAYERs piece
        ok = False
    elif PLAYER[TURN][r][c] == REGULAR :  # is PLAYERs piece
        ok = True
    elif PLAYER[TURN][r][c] == CROWNED : # CROWNED piece for this PLAYER
        ok =  True

    return ok
    

 
#-----------------------------------------------------------------
# draw all pieces on the board
def update_board(win):
    for c in range(SQRS):
        for r in range(SQRS):
            if PLAYER[ONE][r][c] > EMPTY :
                draw_checker(win,r,c,PIECECOLOR[ONE],(PLAYER[ONE][r][c]==CROWNED))
            if PLAYER[TWO][r][c] > EMPTY :
                draw_checker(win,r,c,PIECECOLOR[TWO],(PLAYER[TWO][r][c]==CROWNED))
    
               
#-----------------------------------------------------------------
'''  0 no piece, 1 has piece, 2 CROWNEDed piece
    fill 3d list with the PLAYERs positions for the game start
    12 pieces each
'''    
def init_PLAYERs(win):
    global PLAYER, CAPTURE
    ''' a board for each PLAYER '''
    PLAYER.append([])
    PLAYER.append([])
    CAPTURE.append(0)
    CAPTURE.append(0)
    for r in range(SQRS):
        PLAYER[ONE].append([])
        PLAYER[TWO].append([])
        for c in range(SQRS):
            # set all spaces to not allowed
            PLAYER[ONE][r].append(NOPLAY) 
            PLAYER[TWO][r].append(NOPLAY)            
    ''' 12 pieces each '''
    check = 1
    limit = SQRS-1
    not_blank = int(NUMPIECES/(SQRS/2))
    for i in range(SQRS):
        for j in range(SQRS):
            if (check == 1) :
                if i < not_blank :
                    PLAYER[ONE][i][j] = REGULAR
                    PLAYER[TWO][limit-i][limit-j] = REGULAR
                else :
                    PLAYER[ONE][i][j] = EMPTY
                    PLAYER[TWO][limit-i][limit-j] = EMPTY
            
            check = 1 - check
        check = 1 - check
            
    debug_show_players()
    return True

#----------------------------------------------------- DEBUG
#-----------------------------------------------------  
def debug_show_players():
    if DEBUG | DEBUG2 : print("positions\n PLAYER 1\n",PLAYER[ONE])             
    if DEBUG | DEBUG2 : print("PLAYER 2\n",PLAYER[TWO])   
    
#----------------------------------------------------- DEBUG
#-----------------------------------------------------     
def debug_show_window():  
    if DEBUG | DEBUG2 :
        win2 = GraphWin("DEBUG WINDOW",BRD_W,BRD_W)
        draw_board(win2)
        update_board(win2)
        win2.getMouse()
        win2.close
        
#----------------------------------------------------- DEBUG
#-----------------------------------------------------     
def debug_show_capture() :
        if DEBUG | DEBUG2  : print("capture PLAYER 1\n",CAPTURE[ONE]) 
        if DEBUG | DEBUG2  : print("capture PLAYER 2\n",CAPTURE[TWO])
         
#----------------------------------------------------- DRAW A BOX
def erase_checker(win,y,x):
    m = BOX_W
    x1 = BOX_W*x
    y1 = BOX_W*y
    bc=0
    a = Point(x1,y1)
    b = Point(x1+m-1,y1+m-1)
    rect = Rectangle(a,b)
    rect.setFill(BOXCOLOR[bc])
    rect.setOutline(BOXCOLOR[bc])
    rect.setWidth(1)  
    rect.draw(win)
    return True
    
#------------------------------------------------------ ONE CHECKER
def draw_checker(win,y,x,color,CROWNED=False):
    checker_base(win,y,x,color,False)
    if CROWNED : checker_base(win,y,x,color,True)

def checker_base(win,y,x,color,CROWNED=False):
    # if DEBUG : print ("dc: ",x,y,color,CROWNED,end="-> ")
    o = BOX_W/2
    x1 = BOX_W*x+o
    y1 = BOX_W*y+o
    if CROWNED == False :
        clr1=color
    else :
        clr1="yellow"
    clr2="black"
    r1=int(BOX_W*.8)/2
    r2=int(BOX_W*.6)/2
    # if DEBUG : print(x1,y1)
    c0 = Point(x1,y1)
    circ = Circle(c0,r1)
    circ.setFill(clr1)
    circ.setOutline(clr2)
    circ.setWidth(2)    
    circ.draw(win)
    circ = Circle(c0,r2)
    circ.setFill(color)
    circ.draw(win)

def tiny_checker(win,y,x,color,w):
    # if DEBUG : print ("dc: ",x,y,color,CROWNED,end="-> ")
    o = w/2
    x1 = x+o
    y1 = y+o
    clr1=color
    clr2="black"
    r1=int(w*.8)/2
    r2=int(w*.6)/2
    c0 = Point(x1,y1)
    circ = Circle(c0,r1)
    circ.setFill(clr1)
    circ.setOutline(clr2)
    circ.setWidth(2)    
    circ.draw(win)
    circ = Circle(c0,r2)
    circ.draw(win)
 
#-------------------------------------------------------- CHECKERBOARD
def draw_board(win):  
    m = BOX_W
    o = BOX_W
    bc = 0
    y=0
    while y<BRD_W :
        x=0
        while x < BRD_W :
            a = Point(x,y)
            b = Point(x+m,y+m)
            rect = Rectangle(a,b)
            rect.setFill(BOXCOLOR[bc])
            rect.setOutline(BOXCOLOR[bc])
            rect.setWidth(1)  
            rect.draw(win)
            x=x+o
            bc = 1 - bc
        y=y+m   
        bc = 1 - bc   
    return True
 
   
main()
