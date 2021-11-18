from gameboard import *


class Piece:
    def __init__(self, color, startingTile):
        self.color = color
        self.location = startingTile
        # Movement rules is dict of lists of tuples by cardinal direction
        # Movement rules does not change
        self.movementRules = {'N': [], 'NE': [], 'E': [], 'SE': [], 'S': [], 'SW': [], 'W': [], 'NW': [], 'K': []}
        self.availableMoves = []  # List of tuples of available destinations
        self.attacking = []
        self.attackedBy = []
        self.defending = []
        self.defendedBy = []

    def addMovementRule(self, fileMove, rankMove):
        # Sort movement into cardinal direction
        if fileMove == 0 and rankMove == 0:
            return
        if fileMove != rankMove and (fileMove != 0 or rankMove != 0):
            return
        if fileMove > 0 and rankMove == 0:
            self.movementRules['N'].append((fileMove, rankMove))
        elif fileMove > 0 and rankMove > 0:
            self.movementRules['NE'].append((fileMove, rankMove))
        elif fileMove == 0 and rankMove > 0:
            self.movementRules['E'].append((fileMove, rankMove))
        elif fileMove < 0 and rankMove > 0:
            self.movementRules['SE'].append((fileMove, rankMove))
        elif fileMove < 0 and rankMove == 0:
            self.movementRules['S'].append((fileMove, rankMove))
        elif fileMove < 0 and rankMove < 0:
            self.movementRules['SW'].append((fileMove, rankMove))
        elif fileMove == 0 and rankMove < 0:
            self.movementRules['W'].append((fileMove, rankMove))
        elif fileMove > 0 and rankMove < 0:
            self.movementRules['NW'].append((fileMove, rankMove))

    @staticmethod
    def movePieceByRule(startingTile, fileMove, rankMove):
        # Move piece, check if out of bounds, returns tuple e.g. (1, 1)
        destination = [startingTile[0], startingTile[1]]

        destination[0] += fileMove
        if destination[0] < 1 or destination[0] > 8:
            return

        destination[1] += rankMove
        if destination[1] < 1 or destination[1] > 8:
            return

        return tuple(destination)

    def findAvailableMoves(self, gameBoard):
        # Check collisions that interrupt lines
        for direction in GameBoard.cardinalDirections:
            if not self.movementRules[direction]:
                pass

            nearestCollidingPiece = 8
            for movementRule in self.movementRules[direction]:
                # Generate destination and check if in bounds
                destination = [self.location[0], self.location[1]]
                destination[0] += movementRule[0]
                if destination[0] < 1 or destination[0] > 8 or destination[1] < 1 or destination[1] > 8:
                    continue

                # Skip collision check for knight
                if isinstance(self, Knight):
                    destinationPiece = gameBoard.checkForPiece(destination)
                    if destinationPiece:
                        # Update defending/attacking, add move
                        if destinationPiece.color == self.color:
                            self.defending.append(destinationPiece)
                            continue
                        else:
                            self.attacking.append(destinationPiece)
                    self.availableMoves.append(destination)
                    continue

                # Calculate distance of move by either change in file or rank
                if direction == 'N' or direction == 'S':
                    distance = abs(destination[1] - self.location[1])
                else:
                    distance = abs(destination[0] - self.location[0])

                if distance < nearestCollidingPiece:
                    destinationPiece = gameBoard.checkForPiece(destination)
                    if destinationPiece:

                        # Exception for forward move of pawn
                        if isinstance(self, Pawn) and len(direction) == 1:
                            continue

                        # Update nearest collision, update defending/attacking
                        nearestCollidingPiece = distance
                        if destinationPiece.color == self.color:
                            self.defending.append(destinationPiece)
                            continue
                        else:
                            self.attacking.append(destinationPiece)

                    # Check for en passant if pawn and no destination piece
                    elif isinstance(self, Pawn) and \
                            len(direction) == 2 and \
                            ((self.color == 'white' and destination[1] == 6) or
                             (self.color == 'black' and destination[1] == 3)):
                        if not gameBoard.checkEnPassant(self, destination):
                            continue

                    self.availableMoves.append(destination)


class Pawn(Piece):
    value = 1

    def __init__(self, color, startingTile):
        super().__init__(color, startingTile)

        if self.color == 'white':
            self.movementRules['N'] = [(0, 1), (0, 2), (1, 1), (-1, 1)]
        else:
            self.movementRules['S'] = [(0, -1), (0, -2), (1, -1), (-1, -1)]


class Bishop(Piece):
    value = 3.33

    def __init__(self, color, startingTile):
        super().__init__(color, startingTile)

        for fileMove in range(-7, 8):
            for rankMove in range(-7, 8):
                super().addMovementRule(fileMove, rankMove)
        self.movementRules['S'] = self.movementRules['N'] = self.movementRules['E'] = self.movementRules['W'] = []


class Knight(Piece):
    value = 3.05

    def __init__(self, color, startingTile):
        super().__init__(color, startingTile)

        self.movementRules['K'] = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                                   (1, 2), (1, -2), (-1, 2), (-1, -2)]


class Rook(Piece):
    value = 5.63

    def __init__(self, color, startingTile):
        super().__init__(color, startingTile)

        for fileMove in range(-7, 8):
            for rankMove in range(-7, 8):
                super().addMovementRule(fileMove, rankMove)
        self.movementRules['SW'] = self.movementRules['NW'] = self.movementRules['NE'] = self.movementRules['SE'] = []


class Queen(Piece):
    value = 9.5

    def __init__(self, color, startingTile):
        super().__init__(color, startingTile)

        # Generate all movement rules
        for fileMove in range(-7, 8):
            for rankMove in range(-7, 8):
                super().addMovementRule(fileMove, rankMove)


class King(Piece):
    value = 0

    def __init__(self, color, startingTile):
        super().__init__(color, startingTile)

        for fileMove in range(-1, 2):
            for rankMove in range(-1, 2):
                super().addMovementRule(fileMove, rankMove)
