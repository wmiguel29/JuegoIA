# Author: aqeelanwar
# Created: 13 March,2020, 9:19 PM
# Email: aqeel.anwar@gatech.edu

from multiprocessing.sharedctypes import Value
from platform import node
from tkinter import *
import numpy as np

size_of_board = 600
number_of_dots = 3
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25*size_of_board/number_of_dots
edge_width = 0.1*size_of_board/number_of_dots
distance_between_dots = size_of_board / (number_of_dots)


class Dots_and_Boxes():

    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.play_again()
        self.player1_score=0
        self.player2_score=0
        self.player=True
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))
        
        self.player1_starts = True
        self.player1_turn = True
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def mainloop(self):
        self.window.mainloop()


    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position-distance_between_dots/4)//(distance_between_dots/2)
        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            type = 'row'
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def mark_box(self):
        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                if self.player1_turn:
                    color = player1_color_light
                    self.shade_box(box, color)
                    self.player1_score +=1
                else:
                    color = player2_color_light
                    self.shade_box(box, color)
                    self.player2_score +=1
                   

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if c < (number_of_dots-1) and r < (number_of_dots-1):
            self.board_status[c][r] += val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += val

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = player2_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width)
    

    def display_gameover(self):
        if self.player1_score > self.player2_score:
            text = 'Winner: Player 1 '
            color = player1_color
        elif self.player2_score > self.player1_score:
            text = 'Winner: Player 2 '
            color = player2_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(self.player1_score) + '\n'
        score_text += 'Player 2 : ' + str(self.player2_score) + '\n'
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.player1_score=0
        self.player2_score=0
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i*distance_between_dots+distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2,
                                        end_x+dot_width/2, fill=dot_color,
                                        outline=dot_color)

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold", text=text, fill=color)


    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width/2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def posibility (self):
        operators=[]
        for i in range(len(self.row_status)):
            for j in range(len(self.row_status[i])):
                arrayxd=[i,j,0]
                operators.append(arrayxd)
                
        for i in range(len(self.col_status)):
            for j in range(len(self.col_status[i])):
                arrayxd=[i,j,1]
                operators.append(arrayxd)
        return operators
    

    def click(self, event):
        if not self.reset_board:
            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
            if valid_input and not self.is_grid_occupied(logical_positon, valid_input):
                cont = len(self.already_marked_boxes)
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.mark_box()
                self.refresh_board()
                if self.is_gameover():
                    self.display_gameover()
                elif(cont==len(self.already_marked_boxes)):
                  self.player1_turn = not self.player1_turn
                  while(self.player1_turn==False):
                    if(self.is_gameover()):
                      self.player1_turn = True
                      self.display_gameover()
                    else:
                      cont = len(self.already_marked_boxes)
                      operators= self.posibility()
                      status = [self.row_status, self.col_status, self.board_status]
                      prueba= Doxes(True,value="inicio",state = status, operators=operators)              
                      treeMinMax= Tree(prueba, operators)
                      resultado= treeMinMax.alpha_beta(5)
                      self.row_status=resultado.state[0]
                      self.col_status=resultado.state[1]
                      self.board_status=resultado.state[2]
                      a,b=ia_update(resultado.state,resultado.parent.state)
                      self.make_edge(b,a)
                      self.mark_box()
                      self.refresh_board()  
                    if(cont==len(self.already_marked_boxes)):
                      self.player1_turn = True                    
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


def ia_update(state1, state2):
  for i in range(len(state1[0])):
    for j in range(len(state1[0][i])):
      if state1[0][i][j] != state2[0][i][j]:
        return [j, i], "row"
  for i in range(len(state1[1])):
    for j in range(len(state1[1][i])):
      if state1[1][i][j] != state2[1][i][j]:
        return [j, i], "col"



#INCIIO ALPHA BETHA __ COLOCAR EL STATE DE LAS 2 VARIABLES
class Node ():
  def __init__(self, state ,value,operators,operator=None, parent=None,objective=None):
    self.state = state
    self.value = value
    self.children = []
    self.parent=parent
    self.operator=operator
    self.objective=objective
    self.level=0
    self.operators=operators
    self.v=0

    
  def add_child(self, value, state, operator):
    node=type(self)(value=value, state=state, operator=operator,parent=self,operators=self.operators)
    node.level=node.parent.level+1
    self.children.append(node)
    return node
  
  def add_node_child(self, node):
    node.level=node.parent.level+1
    self.children.append(node)    
    return node

  def update_board1(self,states):
    cont = 0
    for i in range(len(states[2])):
      for j in range(len(states[2][i])):
        if states[0][i][j] != 0:
          cont+=1
        if states[0][i+1][j] != 0:
          cont+=1
        if states[1][i][j] != 0:
          cont+=1
        if states[1][i][j+1] != 0:
          cont+=1
        states[2][i][j] = cont
        cont=0
    return states[2]

  #Devuelve todos los estados según los operadores aplicados

  def   getchildrens(self): 
    resultados=[]
    row=self.state[0]
    columns= self.state[1]
    
    board=[]
    for i in range(len(row)):
      for j in range(len(row[i])):
        if row [i][j]!=1:
          original= np.copy(self.state[2])  
          nuevo=np.copy(row)
          nuevo[i][j]=1
          board=self.update_board1([nuevo,columns,original])
          resultados.append([nuevo,columns,board])
    for i in range(len(columns)):
      for j in range(len(columns[i])):
        if columns [i][j]!=1:

          original= np.copy(self.state[2])  
          nuevo=np.copy(columns)
          nuevo[i][j]=1
          board=self.update_board1([row,nuevo,original])
          resultados.append([row,nuevo,board])
     
    return resultados
    
  def getState(self, index):
    pass
  
  def heuristic(self):
    return 0
  
  def cost(self):
    return 1
  
  def f(self): 
    return self.cost()+self.heuristic()

  ### Crear método para criterio objetivo
  ### Por defecto vamos a poner que sea igual al estado objetivo, para cada caso se puede sobreescribir la función
  def isObjective(self):
    return (self.state==self.objetive.state)

class Tree ():
  def __init__(self, root ,operators):
    self.root=root
    self.operators=operators

  def alpha_beta(self, depth):
    self.root.v= self.alpha_betaR(self.root, depth, float('-inf'), float('+inf'), True)
    if not self.root.isObjective():
      values=[c.v for c in self.root.children]
      maxvalue=max(values)
      index=values.index(maxvalue)
      return self.root.children[index]
    else: return self.root
 
  
  def alpha_betaR(self, node, depth, alpha, beta, player):
    if depth == 0 or node.isObjective():
       node.v = node.heuristic()
       return node.heuristic()
    if player:
      value=float('-inf')
      children = node.getchildrens()
      for i,child in enumerate(children):
        if child is not None:
          newChild=type(self.root)(value=node.value+'-'+str(i),state=children[i],operator=i,parent=node, operators=node.operators,player=False)
          newChild=node.add_node_child(newChild)
          value = max(value,self.alpha_betaR(newChild, depth-1, alpha,beta,False))
          alpha = max(alpha,value)
          if alpha>=beta:
            break
     
    else:
      value=float('inf')
      children = node.getchildrens()
      for i,child in enumerate(children):
        if child is not None:
          newChild=type(self.root)(value=node.value+'-'+str(i),state=children[i],operator=i,parent=node, operators=node.operators,player=True)
          newChild=node.add_node_child(newChild)
          value = min(value,self.alpha_betaR(newChild, depth-1, alpha,beta,True))
          beta = min(beta,value)
          if alpha>=beta:
            break
    node.v = value
    return value
 
class Doxes(Node):
  ## Vamos a añadir el jugador, pues en dependencia del jugador se hace una cosa u otra.

  def __init__(self, player=True,**kwargs):
    super(Doxes, self).__init__(**kwargs)
    self.player=player
    if player:
      self.v=float('-inf')
    else:
      self.v=float('inf')

    
  def isObjective(self):
    matrix = np.all(self.state[2] == 4)
    return matrix

  def cost(self):
    return self.level

  def heuristic(self):
    a = self.state[0]
    b = self.state[1]
    board = self.state[2]
    cont=0
    coords = np.argwhere(board == 4)
    if coords.size>0:
      cont += coords.size*10
    coords = np.argwhere(board == 2)
    if coords.size>0:
      cont += coords.size*4
    coords = np.argwhere(board == 1)
    if coords.size>0:
      cont+= coords.size*1
    coords = np.argwhere(board == 3)
    if coords.size>0:
      cont-= coords.size*100
    return cont
game_instance = Dots_and_Boxes()
game_instance.mainloop()
