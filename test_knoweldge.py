import itertools
import random

ai = MinesweeperAI()
ai.knowledge = [Sentence(((6,3),(6,4)),2), Sentence(((0,1),(0,2)),0)]
for sentence in ai.knowledge:
    print(sentence)

print(ai.moves_made)
print(ai.safes)
print(ai.mines)

ai.mark_mine((3,6))
ai.mark_safe((4,5))
ai.add_knowledge((3,5),2)

for sentence in ai.knowledge:
    print(sentence)
    print(len(sentence.cells))

#print(ai.safes)
#print(ai.mines)
