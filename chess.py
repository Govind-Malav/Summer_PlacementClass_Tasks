import random

Pieces=["bP","bR","bN","bB","bQ","bK","wP","wR","wN","wB","wQ","wK"]

Piece_values={'P':100,'N':300,'B':320,'R':500,'Q':900,'K':20000}

class Gamestate:
    def __init__(self):
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]

        self.white_to_move=True
        self.move_log=[]

        self.zobrist_hash=zobrist.get_initial_hash(self.board,self.white_to_move)

        self.white_king_location=(7,4)
        self.black_king_location=(0,4)

    def make_move(self,move):
        self.board[move.start_row][move.start_col]='--'
        self.board[move.end_row][move.end_col]=move.piece_moved
        self.move_log.append(move)

        move_idx=piece_to_idx(move.piece_moved)
        self.zobrist_hash ^=zobrist.table[move.start_row][move.start_col][move_idx]
        self.zobrist_hash ^=zobrist.table[move.end_row][move.end_col][move_idx]

        if move.piece_captured !="--":
            captured_idx=peice_to_idx(move.piece_captured)
            self.zobrist_hash ^=zobrist.table[move.end_row][move.end_col][captured_idx]

        if move.piece_moved=="wK":
            self.white_king_location=(move.end_row,move.end_col)
        elif move.piece_moved=="bK":
            self.black_king_location=(move.end_row,move.end_col)
        
        self.white_to_move = not self.white_to_move
        self.zobrist_hash ^=zobrist.white_to_move_key
    
    def undo_move(self):
        if len(self.move_log) !=0:
            move=self.move_log.pop()
        
            self.board[move.start_row][move.start_col]=move.piece_moved
            self.board[move.end_row][move.end_col]=move.piece_captured
            self.white_to_move = not self.white_to_move


            moved_idx=piece_to_idx(move.piece_moved)
            self.zobrist_hash ^=zobrist.table[move.start_row][move.start_col][moved_idx]
            self.zobrist_hash ^=zobrist.table[move.end_row][move.end_col][moved_idx]
            if move.piece_captured !="--":
                captured_idx=piece_to_idx(move.piece_captured)
                self.zobrist_hash ^=zobrist.table[move.end_row][move.end_col][captured_idx]
            self.zobrist_hash ^=zobrist.white_to_move_key

            if move.piece_moved=="wk":
                self.white_king_location=(move.start_row,move.start_col)
            elif move.piece_moved=="bk":
                self.black_king_location=(move.start_row,move.start_col)
    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0],self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0],self.black_king_location[1])
    def square_under_attack(self,r,c):
        self.white_to_move=not self.white_to_move
        opp_moves=self.get_all_pseudo_legal_moves()
        self.white_to_move= not self.white_to_move
        for move in opp_moves:
            if move.end_row==r and move.end_col==c:
                return True
            return False
    
    def get_valid_moves(self):
        moves=self.get_all_pseudo_legal_moves()

        for i in range(len(moves)-1,-1,-1):
            move=moves[i]
            self.make_move(move)
            self.white_to_move=not self.white_to_move
            if self.in_check():
                moves.remove(move)
            self.white_to_move= not self.white_to_move
            self.undo_moves()
        return moves
    
    def get_all_pseudo_legal_moves(self):
        moves=[]

        for r in range(8):
            for c in range(8):
                turn=self.board[r][c][0]
                if (turn=='w' and self.white_to_move) or (turn=='b' and not self.white_to_move):
                    piece=self.board[r][c][1]
                    if piece == 'P':
                        self.get_pawn_moves(r,c,moves)
                    elif piece == 'R':
                        self.get_rook_moves(r,c,moves)
                    elif piece == 'N':
                        self.get_knight_moves(r,c,moves)
                    elif piece == 'B':
                        self.get_bishop_moves(r,c,moves)
                    elif piece == 'Q':
                        self.get_queen_moves(r,c,moves)
                    elif piece == 'K':
                        self.get_king_moves(r,c,moves)
        return moves
    
    def get_pawn_moves(self,r,c,moves):
        if self.white_to_move:
            if self.board[r-1][c]=='--':
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=='--':
                    moves.append(Move((r,c),(r-2,c),self.board))
                
            if c-1>=0 and self.board[r-1][c-1][0]=='b':
                moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1<=7 and self.board[r-1][c+1][0]=='b':
                moves.append(Move((r,c),(r-1,c+1),self.board))
        else:
            if self.board[r+1][c]=='--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=='--':
                    moves.append(Move((r,c),(r+2,c),self.board))
                
            if c-1>=0 and self.board[r+1][c-1][0]=='w':
                moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1<=7 and self.board[r+1][c+1][0]=='w':
                moves.append(Move((r,c),(r+1,c+1),self.board))
            

    # def print_board(board):
    #     print("\n a b c d e f g h")
    #     for r in range(8):
    #         print(f"{8-r}",end="")
    #         for c in range(8):
    #             piece=board[r][c]
    #             print(f"[{piece if piece != '--' else ' '}]")
    #         print(f"{8-r}")
    #     print(" a b c d e f g h \n")

class Move:
    ranks_to_rows={"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rows_to_rank={v:k for k, v in ranks_to_rows.items()}

    files_to_cols={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    cols_to_files={v:k for k,v in files_to_cols.items()}

    def __init__(self,start_sq,end_sq,board):
        self.start_row,self.start_col=start_sq
        self.end_row,self.end_col=end_sq
        self.piece_moved=board[self.start_row][self.start_col]
        self.pieces_captured=board[self.end_row][self.end_col]
        self.move_id=self.start_row*1000+self.start_col*100+self.end_row*10+self.end_col
        

    def __eq__(self,other):
        if instance(other,move):
            return self.move_id == other.move_id
        return False

    def get_algebraic_notation(self):
        return self.get_rank_files(self.start_row,self.start_col)+(self.get_row,self.end_col)

    def get_rank_file(self,row,col):
        return self.cols_to_find[col]+self.rows_to_rank[row]

    
class zobrist:
    def __init__(self):
        self.table=[[[random.getrandbits(64)] for _ in range(12)] for _ in range(8)]
        self.white_to_move_key=random.getrandbits(64)

    def get_initial_hash(self,board,white_to_move):
        h=0
        for r in range(8):
            for c in range[8]:
                piece=board[r][c]
                if piece!='--':
                    piece_idx=piece_to_idx[piece]
                    h^=self.table[r][c][piece_idx]
        if white_to_move:       
            h^=self.white_to_move_key
        return h

zobrist=zobrist()

