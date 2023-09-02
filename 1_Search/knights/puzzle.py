from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

knowledge0 = And(
    # we know that A is either a knight or a knave, but not both.
    And(
        Or(AKnight, AKnave),
        Not(And(AKnight, AKnave))
    ),
    # and A said that he is both a knight and a knave
    # (which can translate to if A is a knight, then its true,
    # and if A is a knave, then A is lying)

    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))

)
# * A is a knave.


#! Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # we know that A and B are either a knight or a knave, but not both.
    And(
        Or(AKnight, AKnave),
        Not(And(AKnight, AKnave))
    ),
    And
    (
        Or(BKnight, BKnave),
        Not(And(BKnight, BKnave))
    ),


    # if A is a knight, then its true,
    # if its true, then A is a knave and B is a knave which mean a is lying which is not possible meaning A is a knave
    Implication(AKnight, And(AKnave, BKnave)),
    # if A is a knave, then A is lying
    # if its false(which its is), then A is lying which is not possible meaning A is a knave and B is a knight
    Implication(AKnave, Not(And(AKnave, BKnave)))

)
# * A is a knave.
# * B is a knight.

#! Puzzle 2 #fixed
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # we know that A and B are either a knight or a knave, but not both.
    And(
        Or(AKnight, AKnave),
        Not(And(AKnight, AKnave))
    ),
    And
    (
        Or(BKnight, BKnave),
        Not(And(BKnight, BKnave))
    ),

    # A statement
    Implication(
        AKnight,  # if A is a knight, then the statement is true,
        # which means A and B are both knights or both knaves
        Or(And(AKnight, BKnight), And(AKnave, BKnave))
    ),
    Implication(
        AKnave,  # if A is a knave, then the statement is false,
        # which means A and B are different
        Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))
    ),

    # B statement
    Implication(
        BKnight,  # if B is a knight, then the statement is true,
        Or(And(AKnight, BKnave), And(AKnave, BKnight))  # A and B are different
    ),
    Implication(
        BKnave,  # if B is a knave, then the statement is false,
        # A and B are the same
        Not(Or(And(AKnight,  BKnave), And(AKnave, BKnight)))
    ),
)


# * A is a knave.
# * B is a Knight.

#! Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # we know that A and B and C are either a knight or a knave, but not both.
    And(
        Or(AKnight, AKnave),
        Not(And(AKnight, AKnave))
    ),
    And
    (
        Or(BKnight, BKnave),
        Not(And(BKnight, BKnave))
    ),
    And(
        Or(CKnight, CKnave),
        Not(And(CKnight, CKnave))
    ),

    # A statement
    # ? Already know that A is either a knight or a knave, but not both. no need to write it again


    # B statement about A
    Implication(
        # if B is a knight, then the statement is true, translating to (A said(implied) that he is a knave)
        BKnight,
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    ),
    Implication(
        # if B is a knave, then the statement is false, translating to (A didn't said(implied) that he is a knave)
        BKnave,
        Not(And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        ))
    ),

    # B statement about C
    Implication(
        # if B is a knight, then the statement is true, translating to C is a knave
        BKnight,
        CKnave
    ),
    Implication(
        # if B is a knave, then the statement is false, translating to C is not a knave
        BKnave,
        Not(CKnave)
    ),


    # C statement
    Implication(
        # if C is a knight, then the statement is true, translating to A is a knight
        CKnight,
        AKnight
    ),
    Implication(
        # if C is a knave, then the statement is false, translating to A is not a knight
        CKnave,
        Not(AKnight)
    )
)
# * A is a knight.
# * B is a knave.
# * C is a knight.


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
