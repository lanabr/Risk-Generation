from abc import ABC


class Action(ABC):
    pass

    def __eq__(self, o):
        if isinstance(self, AllocationAction):
            if isinstance(o, AllocationAction):
                if self.territoryidToConquer == o.territoryidToConquer and self.playerID == o.playerID:
                    return True
            return False

        if isinstance(self, AddUnitsInExchangeCardsAction):
            if isinstance(o, AddUnitsInExchangeCardsAction):
                if self.cardsToExchange[0] == o.cardsToExchange[0] and self.cardsToExchange[1] == o.cardsToExchange[1] and self.cardsToExchange[2] == o.cardsToExchange[2]:
                    return True
            return False

        if isinstance(self, AddUnitsInConflictAction):
            if isinstance(o, AddUnitsInConflictAction):
                if self.territoryidToAdd == o.territoryidToAdd:
                    return True
            return False

        if isinstance(self, AttackWithUnitsInConflictAction):
            if isinstance(o, AttackWithUnitsInConflictAction):
                if self.territoryidAttacking == o.territoryidAttacking and self.territoryidDefending == o.territoryidDefending:
                    return True
            return False

        if isinstance(self, MoveUnitsInConflictAction):
            if isinstance(o, MoveUnitsInConflictAction):
                if self.territoryidFrom == o.territoryidFrom and self.territoryidTo == o.territoryidTo:
                    return True
            return False

    def __hash__(self):
        if isinstance(self, AllocationAction):
            return hash((self.territoryidToConquer, 0))

        if isinstance(self, AddUnitsInExchangeCardsAction):
            return hash((self.cardsToExchange, 1))

        if isinstance(self, AddUnitsInConflictAction):
            return hash((self.territoryidToAdd, 2))

        if isinstance(self, AttackWithUnitsInConflictAction):
            return hash((self.territoryidAttacking, self.territoryidDefending, 3))

        if isinstance(self, MoveUnitsInConflictAction):
            return hash((self.territoryidFrom, self.territoryidTo, 4))

        if isinstance(self, PassTurn):
            return hash(0)


class AllocationAction(Action):
    def __init__(self, territoryidToConquer, playerID):
        self.territoryidToConquer = territoryidToConquer
        self.playerID = playerID


class AddUnitsInExchangeCardsAction(Action):
    def __init__(self, cardsToExchange):
        self.cardsToExchange = cardsToExchange


class AddUnitsInConflictAction(Action):
    def __init__(self, territoryidToAdd):
        self.territoryidToAdd = territoryidToAdd


class AttackWithUnitsInConflictAction(Action):
    def __init__(self, territoryidAttacking, territoryidDefending):
        self.territoryidAttacking = territoryidAttacking
        self.territoryidDefending = territoryidDefending


class MoveUnitsInConflictAction(Action):
    def __init__(self, territoryidFrom, territoryidTo):
        self.territoryidFrom = territoryidFrom
        self.territoryidTo = territoryidTo


class PassTurn(Action):
    def __init__(self):
        pass
