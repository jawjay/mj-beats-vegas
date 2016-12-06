import json


board = [[4, 8, 12], [5, 10, 15], [6, 12, 18]]

diagR = [(0,0),(1,1),(0,2)]
diagL = [(2,0),(1,1),(0,2)]
verts = [[ (i,j) for i in range(3)]for j in range(3)] 
rows = (zip(*verts))

possible = verts + rows + [diagL]+[diagR]

for p  in possible:
    x=1
    # print p# test_Ai = AI()
# print test_Ai.findRandomMove(test_game.board)

print rows
print verts
