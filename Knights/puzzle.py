from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

gameKnowledge = And(
    Implication(AKnight, Not(AKnave)),
    Implication(BKnight, Not(BKnave)),
    Implication(CKnight, Not(CKnave)),
    Implication(AKnave, Not(AKnight)),
    Implication(BKnave, Not(BKnight)),
    Implication(CKnave, Not(CKnight)),
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Splits it, if AKnight is false and AKnave is true, then it is AKnave as KB is also true.
    # If AKnight is true and AKnave is false, KB is false.
    Implication(AKnight, And(AKnight, AKnave)),

    # Only allows for ONLY one to be chosen (true), not one or both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # If AKnight is true, the second part MUST be true or else they are an AKnave.
    Implication(AKnight, And(AKnave, BKnave)),

    # Since B did not state anything, it is the same as not denying the claim A said (Code written in 2 different ways to represent).
    Implication(BKnight, And(Not(Not(AKnave)), Not(Not(BKnave)))),
    Implication(BKnight, And(AKnave, BKnave)),

    # Only allows for ONLY one to be chosen (true), not one or both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # If A is a knight, A and B both must be knights, otherwise, A is a knave.
    Implication(AKnight, And(AKnight, BKnight)),

    # If B is a knight, B must be the knight and A must be the knave.
    Implication(BKnight, And(AKnave, BKnight)),

    # This confirms that BKnight is false if BKnave is true.
    Implication(BKnave, BKnight),

    # Only allows for ONLY one to be chosen (true), not one or both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # If A is a knight, then B must be lying and C is telling the truth, and if A is a Knave, then the others would also be knaves.
    Implication(AKnight, And(BKnave, CKnight)),
    Implication(AKnave, And(BKnave, CKnave)),

    # If B is a knight, then A and C would be knaves, if B was a knave, then A and C would have to be knights (agrees with other statements).
    Implication(BKnight, And(AKnave, CKnave)),
    Implication(BKnave, And(AKnight, CKnight)),

    # C tells the truth if A is a knight.
    Implication(CKnight, AKnight),

    # Only allows for ONLY one to be chosen (true), not one or both.
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave)))
)


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
