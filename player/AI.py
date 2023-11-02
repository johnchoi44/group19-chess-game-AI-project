from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True
        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def checkmatew(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

    
    def checkmateb(self,gametiles):
        movex = move()
        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr

    # a function that calculate the mobility for each chess piece
    def calculate_mobility(self, gametiles):
        mobility_value = 0
        movex = move()
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.alliance == 'Black':
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    if moves is not None:
                        mobility_value += len(moves)
        return mobility_value

    # function that evaluate pawn structure
    def evaluate_pawn_structure(self, gametiles):
        pawn_chains = 0
        pawn_islands = 0
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile
                if piece.tostring() == 'P':
                    try:
                        # Evaluate Black pawn chain structure with two or more diagonally linked pawns
                        if gametiles[y - 1][x - 1].pieceonTile.tostring() == 'P':
                            pawn_chains -= 1
                        if gametiles[y + 1][x + 1].pieceonTile.tostring() == 'P':
                            pawn_chains -= 1
                        if gametiles[y + 1][x - 1].pieceonTile.tostring() == 'P':
                            pawn_chains -= 1
                        if gametiles[y - 1][x + 1].pieceonTile.tostring() == 'P':
                            pawn_chains -= 1
                        # Evaluate Black pawn islands structure, where pawns are separated by one or more columns
                        # this is considered to be a weaknesses, the player with more pawn islands has the weaker structure
                        lcol1 = gametiles[y][x - 1].pieceonTile.tostring()
                        lcol2 = gametiles[y + 1][x - 1].pieceonTile.tostring()
                        lcol3 = gametiles[y + 2][x - 1].pieceonTile.tostring()
                        rcol1 = gametiles[y][x + 1].pieceonTile.tostring()
                        rcol2 = gametiles[y + 1][x + 1].pieceonTile.tostring()
                        rcol3 = gametiles[y + 2][x + 1].pieceonTile.tostring()
                        if lcol1 != 'P' and lcol2 != 'P' and lcol3 != 'P':
                            pawn_islands += 0.1
                        if rcol1 != 'P' and rcol2 != 'P' and rcol3 != 'P':
                            pawn_islands += 0.1
                    except IndexError:
                        pass
                ### did not include a evaluation of the White pawn as it might lead to a non-optimal move considering the White pawn.
                # elif piece.tostring() == 'p':
                #     try:
                #         # Evaluate White pawn chain structure with two or more diagonally linked pawns
                #         if gametiles[y - 1][x - 1].pieceonTile.tostring() == 'p':
                #             pawn_chains += 0.5
                #         if gametiles[y + 1][x + 1].pieceonTile.tostring() == 'p':
                #             pawn_chains += 0.5
                #         if gametiles[y + 1][x - 1].pieceonTile.tostring() == 'p':
                #             pawn_chains += 0.5
                #         if gametiles[y - 1][x + 1].pieceonTile.tostring() == 'p':
                #             pawn_chains += 0.5
                #         # Evaluate Black pawn islands structure, where pawns are separated by one or more columns
                #         # this is considered to be a weaknesses, the player with more pawn islands has the weaker structure
                #         lcolm = gametiles[y][x - 1].pieceonTile.tostring()
                #         lcolu = gametiles[y - 1][x - 1].pieceonTile.tostring()
                #         lcold = gametiles[y + 1][x - 1].pieceonTile.tostring()
                #         rcolm = gametiles[y][x + 1].pieceonTile.tostring()
                #         rcolu = gametiles[y - 1][x + 1].pieceonTile.tostring()
                #         rcold = gametiles[y + 1][x + 1].pieceonTile.tostring()
                #         if lcolm != 'p' and lcolu != 'p' and lcold != 'p':
                #             pawn_islands += 0.1
                #         if rcolm != 'p' and rcolu != 'p' and rcold != 'p':
                #             pawn_islands += 0.1
                #     except IndexError:
                #         pass
        pawn_structure_value = pawn_chains + pawn_islands
        return pawn_structure_value

    # evaluation function that is being used to evaluate non-terminal states that are encountered in the minimax search tree
    def calculateb(self,gametiles):
        mobility_value = 0
        pawn_structure_value = 0
        space_advantage_value = 0
        value=0
        for x in range(8):
            for y in range(8):
                    piece = gametiles[y][x].pieceonTile
                    if piece.tostring()=='P':
                        value=value-100
                    if piece.tostring()=='N':
                        value=value-300
                    if piece.tostring()=='B':
                        value=value-300
                    if piece.tostring()=='R':
                        value=value-550
                    if piece.tostring()=='Q':
                        value=value-1000
                    if piece.tostring()=='K':
                        value=value-10000
                    if piece.tostring()=='p':
                        value=value+100
                    if piece.tostring()=='n':
                        value=value+300
                    if piece.tostring()=='b':
                        value=value+300
                    if piece.tostring()=='r':
                        value=value+550
                    if piece.tostring()=='q':
                        value=value+1000
                    if piece.tostring()=='k':
                        value=value+10000

                    # space advantage - someone who controls the 4 key central squares,
                    # or has better control of the 16 central squares.
                    if piece.alliance == 'Black':
                        # Evaluate space advantage for black add 50 point for 4 key central squares
                        # and 1 point for 16 central squares
                        if (3 <= x <= 4) and (3 <= y <= 4):
                            print(piece.tostring())
                            space_advantage_value -= 100
                        elif (2 <= x <= 5) and (2 <= y <= 5):
                            space_advantage_value -= 10
                    ### not using evaluation of white piece as the model might overthink to a non-optimal move
                    # elif piece.alliance == 'White':
                    #     # Evaluate space advantage for white 
                    #     if x >= 3 and x <= 4 and y >= 3 and y <= 4:
                    #         space_advantage_value -= 30
                    #     elif x >= 2 and x <= 5 and y >= 2 and y <= 5:
                    #         space_advantage_value -= 5

        # calculate the value of mobility and pawn_structure 
        mobility_value += self.calculate_mobility(gametiles)
        # king_safety_value += self.calculate_king_safety(gametiles)
        pawn_structure_value += self.evaluate_pawn_structure(gametiles)
        # add value according to check and checkmate
        # add and subtract 100 if the king is checked, subtract or add high value to avoid and try to make checkmate
        try:
            if move().checkb(gametiles)[0]=='checked':
                value -= 100
                if len(move().movesifcheckedb(gametiles)) == 0:
                    value -= 100000
        except:
            value = value
        try:
            if move().checkw(gametiles)[0]=='checked':
                value += 100
                if len(move().movesifcheckedw(gametiles)) == 0:
                    value += 100000
        except: 
            value = value
        # add all the evaluation value caluated with appropriate weights
        value = value + 0.5 * mobility_value + space_advantage_value + pawn_structure_value
        return value

    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles