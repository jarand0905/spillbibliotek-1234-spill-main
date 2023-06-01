#importerer biblotekene vi trenger
import pygame as pg
from pygame.locals import*
import sys



#variabler for gamestart
BLACK = (0, 0, 0)
WINDOW_WIDTH = WINDOW_HEIGHT = 500
DIMENSION =8
SQ_SIZE = WINDOW_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}



# 3 - initialiserer spillet

#farger
white = (255, 255, 255)
black = (0, 0, 0)
#loader bildene til de riktige navnene i arrayen
def loadImages():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bQ','bK']
    for piece in pieces:
        IMAGES[piece]=pg.transform.scale(pg.image.load("Sjakk/sjakk/"+ piece +".png"),(SQ_SIZE,SQ_SIZE)) 

#lager en klasse for brettet 
class GameState():
    def __init__(self):
        #bruker array til å lettere definere brettet 
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],]
        self.movefunk = {"P": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves, 
                        "B" : self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
    def makeMove(self,move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # logg til senere
        self.whiteToMove = not self.whiteToMove #bytte tur
    def getValidMoves(self):
        return  self.getAllPossibleMoves()
    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn =="w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.movefunk[piece](r,c,moves)
        return moves


    def getPawnMoves(self, r , c, moves):
        if self.whiteToMove:
            if self.board[r-1][c]=="--":
                moves.append(Move((r, c),(r-1,c),self.board))
                if r == 6 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1>=0: #ta brikker skrått til venstre
                if self.board[r-1][c-1][0]=="b": #motstanders brikke
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1<=7:
                if self.board[r-1][c+1][0]=="b":
                    moves.append(Move((r,c),(r-1,c+1),self.board))
                            
        else: 
            if self.board[r+1][c]=="--":
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1>=0: #ta brikker skrått til venstre
                if self.board[r+1][c-1][0]=="w": #motstanders brikke
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<=7:
                if self.board[r+1][c+1][0]=="w":
                    moves.append(Move((r,c),(r+1,c+1),self.board))
    
    def getRookMoves(self, r, c, moves):
        directions =((-1,0),(0,-1),(1,0),(0,1)) #opp venstre ned høyre
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] *i
                endCol = c + d[1] *i
                if 0 <= endRow < 8 and 0 <= endCol <8: #på brettet
                    endPiece = self.board[endRow][endCol]
                    if endPiece =="--": #tom rute godkjent
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getKnightMoves(self,r,c, moves):
        directions =((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)) #opp venstre ned høyre
        allyColor = "w" if self.whiteToMove else "b"
        for m in directions:
            endRow = r + m[0] 
            endCol = c + m[1] 
            if 0 <= endRow < 8 and 0 <= endCol <8: #på brettet
                endPiece = self.board[endRow][endCol]
                if endPiece[0]!= allyColor:
                    moves.append(Move((r,c),(endRow,endCol), self.board))

    def getBishopMoves(self,r,c, moves):
        directions =((-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(0,-1),(1,0),(0,1)) #opp venstre ned høyre
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] *i
                endCol = c + d[1] *i
                if 0 <= endRow < 8 and 0 <= endCol <8: #på brettet
                    endPiece = self.board[endRow][endCol]
                    if endPiece =="--": #tom rute godkjent
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
    def getKingMoves(self,r,c, moves):
        km =((-1,1),(-1,1),(1,-1),(1,1),(1,0),(-1,0),(0,1),(0,-1)) #opp venstre ned høyre
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + km[i][0] 
            endCol = c + km[i][1] 
            if 0 <= endRow < 8 and 0 <= endCol <8: #på brettet
                endPiece = self.board[endRow][endCol]
                if endPiece[0]!= allyColor:
                    moves.append(Move((r,c),(endRow,endCol), self.board))

class Move():
    # maps keys to values
    # key : value

    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}

    rowsToRanks ={v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colToFiles = { v: k for k, v in filesToCols.items()}

    def __init__(self,startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self. pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)
    def __eq__(self,other):
        if isinstance(other, Move):
            return (self.moveID == other.moveID)
        return False
    def getChessNotation(self):
        return self.getRankFiles(self.startRow,self.startCol)+ self.getRankFiles(self.endRow, self.endCol)
    def getRankFiles(self, r , c):
        return self.colToFiles[c]+self.rowsToRanks[r]
    
#lager variabel for klassen

gs=GameState()

#hovedkoden
def main():
    pg.init()
    window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pg.time.Clock()
    window.fill(pg.Color("white"))
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages() #loader alle bildene
    #så lenge spillet kjører
    running = True
    sqSelected = () #ingen valgte ruter, hvor musen klikket sist
    playerClicks = [] #holder følge med spillerens klikk
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos() #(x, y) plassering av mus
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected ==(row,col): #spiller trykket samme rute to ganger
                    sqSelected =() #deselect
                    playerClicks = [] #clear spiller trykk
                else:
                    sqSelected =(row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) ==2:
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        print("valid")
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #reset bruker trykk
                    playerClicks = []
                    

            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False
        drawGameState(window,gs) 
        clock.tick(MAX_FPS)
        pg.display.flip()
    
def drawGameState(window,gs): #tegner nåveærende stilling
    drawBoard(window) 
    drawPieces(window,gs.board)


#tegner brettet
def drawBoard(window): 
    colors =[pg.Color("white"),pg.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color =colors[((r+c)%2)]
            pg.draw.rect(window,color,pg.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
#tegner brikkene

def drawPieces(window,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #hvis ruten ikke er tom, så plasserer den en brike der
                window.blit(IMAGES[piece], pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
if __name__ == "__main__":
    main()

        

