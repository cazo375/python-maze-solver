#!/usr/bin/python
#The Maze Sovler
import random

#setup test mode
mode = input("Enter run mode. r for random or f for fixed:")
solution = input("Enter solution type. s for shortest path found or q for quickest path found:")

#fixed grid from txt file
if mode == "f":
    #read in file
    f = open("example_map.txt", 'r')

    #read grid sze
    x = f.readline()
    cut_last_char = x.split("\n")
    vertical = int(cut_last_char[0])
    print(vertical)
    x = f.readline()
    cut_last_char = x.split("\n")
    horizontal = int(cut_last_char[0])
    print(horizontal)

    #init grid
    grid = [] * vertical

    #build grid from file
    x = f.readline()
    i = 0
    while(x != ""):
        cut_last_char = x.split("\n")
        temp_list = cut_last_char[0].split(",")
        grid.append(temp_list)
        print(" ".join(grid[i]))
        x = f.readline()
        i = i + 1

    #parse grid data
    for v in range(0,vertical):
        for h in range(0, horizontal):
            if grid[v][h] == "S":
                start_pos = [v,h]
                print(start_pos)
            elif grid[v][h] == "E":
                end_pos = [v,h]
                print(end_pos)
            #elif grid[v][h] == "T1":
            #    grid[v][h] = "T"
            #    teleporters.append([v,h]) 
    #print(teleporters)
    
#randomly generated grid
elif mode == "r":
    vertical = random.randint(10, 20)
    print(vertical)
    horizontal = random.randint(10,20)
    print(horizontal)
    grid = [] * vertical
               
    
    start_pos = [random.randint(2,vertical-2), random.randint(2,horizontal-2)]
    print(start_pos)
    end_pos = [random.randint(2,vertical-2), random.randint(2,horizontal-2)]
    print(end_pos)

    walls = 0
    for l in range(0, vertical):
        line = []
        for k in range(0,horizontal):
            if l <= 0 or k <= 0 or l >= vertical-1 or k >= horizontal-1:
                line.append("X")
            elif l == start_pos[0] and k == start_pos[1]:
                line.append("S")
            elif l == end_pos[0] and k == end_pos[1]:
                line.append("E")
            else:
                #if walls <= wall_count:  
                if random.randint(0, 10) <= 1:
                    line.append("X")
                    walls = walls + 1
                else:
                    line.append(" ")
                #else:
                #    line.append(" ")
        grid.append(line)
        print(" ".join(line))
    print(walls)
    
    
else:
    print("only r and f are valid modes")

#Node class
class Node:
    def __init__(self, pos, last, weight, move):
        self.pos = pos
        self.last = last
        self.weight = weight
        self.move = move

#production functions
def isValid(py, px, w):
    if px < 0 or px >= horizontal:
        return False
    if py < 0 or py >= vertical:
        return False
    if grid[py][px] == "X":
        return False
    for c in closed_nodes:
        cy = c.pos[0]
        cx = c.pos[1]
        if cx == px and cy == py:
            if w < c.weight:
                #print("w:%d  cw:%d" , w, c.weight)
                #print("overwriten")
                del c
                return True
            return False
    return True

def expand(n):
    posy = n.pos[0]
    posx = n.pos[1]
    new_weight = n.weight + 1
    if isValid(posy - 1, posx, new_weight):
        new_node = Node([posy-1,posx], n, new_weight, "^")
        open_nodes.append(new_node)
    if isValid(posy + 1, posx, new_weight):
        new_node = Node([posy+1,posx], n, new_weight, "v")
        open_nodes.append(new_node)
    if isValid(posy, posx - 1, new_weight):
        new_node = Node([posy,posx-1], n, new_weight, "<")
        open_nodes.append(new_node)
    if isValid(posy, posx + 1, new_weight):
        new_node = Node([posy,posx+1], n, new_weight, ">")
        open_nodes.append(new_node)
    return


#update grid with solution and print
def drawPath(n):
    if n != None:
        n = n.last
        while(n.last != None):
            py = n.pos[0]
            px = n.pos[1]
            grid[py][px] = n.move 
            n = n.last
        for l in range(0, vertical):
            print(" ".join(grid[l]))
            
    return

#init search root
root = Node(start_pos, None, 0, "S")
open_nodes = []
closed_nodes = []
open_nodes.append(root)

#main search loop
print("searching")
while(True):
    if len(open_nodes) <= 0:
        print("out of open nodes.")
        if solution == "s":
            index = None;
            s_path = 99999;
            for c in closed_nodes:
                cy = c.pos[0]
                cx = c.pos[1]
                if cy == end_pos[0] and cx == end_pos[1]:
                    if c.weight < s_path:
                        s_path = c.weight
                        index = c
            if index != None:
                print("shortest solution found!")
                drawPath(index)
                print("path length:")
                print(index.weight)
            break
    
    distance = 999999;    
    for n in open_nodes:
        dist = abs(n.pos[0] - end_pos[0]) + abs(n.pos[1] - end_pos[1])
        if dist < distance:
            distance = dist
            curr_node = n
    if curr_node != None:
        open_nodes.remove(curr_node)
    else:
        curr_node = open_nodes.pop()
        
    curr_pos = curr_node.pos
    if solution == "q":
        if curr_pos[0] == end_pos[0] and curr_pos[1] == end_pos[1]:
            closed_nodes.append(curr_node)
            print("solution found!")
            drawPath(curr_node)
            print("path length:")
            print(curr_node.weight)
            break

    expand(curr_node)
    closed_nodes.append(curr_node)
    curr_node = None

