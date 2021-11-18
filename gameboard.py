from pieces import *
import copy


class GameBoard:
    files = ranks = (1, 2, 3, 4, 5, 6, 7, 8)
    fileDict = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
    cardinalDirections = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    def __init__(self):
        self.moveList = []  # List of tuples of format (piece, origin tile, destination tile, captured piece)
        self.activePieces = []
        self.capturedPieces = []

        # Create tiles in board as dict with entries (file, rank) : Piece
        self.tileIndex = {}
        for file in self.files:
            for rank in self.ranks:
                self.tileIndex[(file, rank)] = None

        # Create starting pieces
        for file in range(1, 9):
            self.activePieces.append(Pawn('white', (file, 2)))
            self.activePieces.append(Pawn('black', (file, 7)))
        self.activePieces.append(King('white', (5, 1)))
        self.activePieces.append(King('black', (5, 8)))
        self.activePieces.append(Queen('white', (4, 1)))
        self.activePieces.append(Queen('black', (4, 8)))
        self.activePieces.append(Bishop('white', (3, 1)))
        self.activePieces.append(Bishop('white', (6, 1)))
        self.activePieces.append(Bishop('black', (3, 8)))
        self.activePieces.append(Bishop('black', (6, 8)))
        self.activePieces.append(Knight('white', (2, 1)))
        self.activePieces.append(Knight('white', (7, 1)))
        self.activePieces.append(Knight('black', (2, 8)))
        self.activePieces.append(Knight('black', (7, 8)))
        self.activePieces.append(Rook('white', (1, 1)))
        self.activePieces.append(Rook('white', (8, 1)))
        self.activePieces.append(Rook('black', (1, 8)))
        self.activePieces.append(Rook('black', (8, 8)))
        for piece in self.activePieces:
            self.tileIndex[piece.location] = piece

    def checkForPiece(self, tile):
        # Returns either Piece instance or None
        return self.tileIndex[tile]

    def updateDefendedAttacked(self):
        # Check each piece for attacking and defending, update corresponding pieces attacked/defended lists
        for piece in self.activePieces:
            for attackedPiece in piece.attacking:
                attackedPiece.attackedBy.append(piece)
            for defendedPiece in piece.defending:
                defendedPiece.defendedBy.append(piece)

    def checkEnPassant(self, destination):
        enPassant = True
        lastMove = self.moveList[-1]
        if not isinstance(lastMove[0], Pawn):
            enPassant = False
        if not destination[1] == ((lastMove[1][1] + lastMove[2][1]) / 2):
            enPassant = False
        if not destination[0] == lastMove[1][0] == lastMove[2][0]:
            enPassant = False
        return enPassant

    def checkCastle(self, king, destinationTile):
        for move in self.moveList:
            if move[0] is king:
                print('King has moved previously')
                return False

        # White, king-side
        if destinationTile == (7, 1):
            if not isinstance(self.tileIndex[(8, 1)], Rook):
                print('Rook not in appropriate position')
                return False
            for move in self.moveList:
                if move[0] is self.tileIndex[(8, 1)]:
                    print('Rook has moved previously')
                    return False
            if self.tileIndex[(6, 1)] or self.tileIndex[(7, 1)]:
                print('Castle path occupied')
                return False
            vulnerableTiles = [(5, 1), (6, 1), (7, 1)]
            for piece in self.activePieces:
                for move in piece.availableMoves:
                    if move in vulnerableTiles:
                        print('Movement not safe.')
                        return False

        # White, queen-side
        if destinationTile == (3, 1):
            if not isinstance(self.tileIndex[(1, 1)], Rook):
                print('Rook not in appropriate position')
                return False
            for move in self.moveList:
                if move[0] is self.tileIndex[(1, 1)]:
                    print('Rook has moved previously')
                    return False
            if self.tileIndex[(2, 1)] or self.tileIndex[(3, 1)] or self.tileIndex[(4, 1)]:
                print('Castle path occupied')
                return False
            vulnerableTiles = [(3, 1), (4, 1), (5, 1)]
            for piece in self.activePieces:
                for move in piece.availableMoves:
                    if move in vulnerableTiles:
                        print('Movement not safe.')
                        return False

        # Black, king-side
        if destinationTile == (7, 8):
            if not isinstance(self.tileIndex[(8, 8)], Rook):
                print('Rook not in appropriate position')
                return False
            for move in self.moveList:
                if move[0] is self.tileIndex[(8, 8)]:
                    print('Rook has moved previously')
                    return False
            if self.tileIndex[(6, 8)] or self.tileIndex[(7, 8)]:
                print('Castle path occupied')
                return False
            vulnerableTiles = [(5, 8), (6, 8), (7, 8)]
            for piece in self.activePieces:
                for move in piece.availableMoves:
                    if move in vulnerableTiles:
                        print('Movement not safe.')
                        return False

        # Black, queen-side
        if destinationTile == (3, 8):
            if not isinstance(self.tileIndex[(1, 8)], Rook):
                print('Rook not in appropriate position')
                return False
            for move in self.moveList:
                if move[0] is self.tileIndex[(1, 8)]:
                    print('Rook has moved previously')
                    return False
            if self.tileIndex[(2, 8)] or self.tileIndex[(3, 8)] or self.tileIndex[(4, 8)]:
                print('Castle path occupied')
                return False
            vulnerableTiles = [(3, 8), (4, 8), (5, 8)]
            for piece in self.activePieces:
                for move in piece.availableMoves:
                    if move in vulnerableTiles:
                        print('Movement not safe.')
                        return False
        return True

    def mergeVirtualBoard(self, virtualBoard):
        # Accepts virtual board, replaces attributes of game board with those of virtual
        self.moveList = virtualBoard.moveList
        self.activePieces = virtualBoard.activePieces
        self.capturedPieces = virtualBoard.capturedPieces
        self.tileIndex = virtualBoard.tileIndex

    @staticmethod
    def checkIllegalCheck(virtualBoard, originTile, destinationTile, piece):
        virtualPiece = copy.deepcopy(piece)
        # Check for capture, log capture
        if virtualBoard.tileIndex[destinationTile]:
            virtualBoard.capturedPieces.append(virtualBoard.tileIndex[destinationTile])
            virtualBoard.activePieces.remove(virtualBoard.tileIndex[destinationTile])

        # Move piece and update index and move list
        virtualBoard.moveList.append(
            (virtualPiece, originTile, destinationTile, virtualBoard.tileIndex[destinationTile]))
        virtualPiece.location = destinationTile
        virtualBoard.tileIndex[destinationTile] = virtualPiece
        virtualBoard.tileIndex[originTile] = None

        # Check for checks
        for activePiece in virtualBoard.activePieces:
            activePiece.findAvailableMoves(virtualBoard)
        virtualBoard.updateDefendedAttacked()
        for activePiece in virtualBoard.activePieces:
            if isinstance(activePiece, King) and activePiece.color == virtualPiece.color:
                if activePiece.attackedBy:
                    print('Illegal move due to check')
                    return None
        return virtualBoard

    def movePiece(self, originTile, destinationTile):
        # Takes two tuples in format (file, rank)
        piece = self.tileIndex[originTile]

        # Check for castling
        if isinstance(piece, King) and abs(originTile[0] - destinationTile[0]) == 2:
            if self.checkCastle(piece, destinationTile):

                # Move king, update index
                piece.location = destinationTile
                self.tileIndex[originTile] = None
                self.tileIndex[destinationTile] = piece

                # Move rook, update index
                if destinationTile == (7, 1):
                    rook = self.tileIndex[(8, 1)]
                    rook.location = (6, 1)
                    self.tileIndex[(8, 1)] = None
                    self.tileIndex[(6, 1)] = rook
                    return
                elif destinationTile == (3, 1):
                    rook = self.tileIndex[(1, 1)]
                    rook.location = (4, 1)
                    self.tileIndex[(1, 1)] = None
                    self.tileIndex[(4, 1)] = rook
                    return
                elif destinationTile == (7, 8):
                    rook = self.tileIndex[(8, 8)]
                    rook.location = (6, 8)
                    self.tileIndex[(8, 8)] = None
                    self.tileIndex[(6, 8)] = rook
                    return
                elif destinationTile == (3, 8):
                    rook = self.tileIndex[(1, 8)]
                    rook.location = (4, 8)
                    self.tileIndex[(1, 8)] = None
                    self.tileIndex[(4, 8)] = rook
                    return
                else:
                    print('Invalid king move')
                    return

        assert destinationTile in piece.availableMoves  # Check move is in available moves

        # Create virtual board, check for illegal move, merge if accepted
        virtualBoard = copy.deepcopy(self)
        newBoard = self.checkIllegalCheck(virtualBoard, originTile, destinationTile, piece)
        if newBoard:
            self.mergeVirtualBoard(newBoard)
