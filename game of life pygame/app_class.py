import pygame, sys
from settings import *
from buttonClass import *

class App:
    # initializing pygame, setting window, setting run to true
    def __init__(self):
        pygame.init()

        #sets window size
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        #bool for if running
        self.running = True
        # an array of numbers to be plugged into the drawgrid function
        self.grid = testBoard
        #bool for selecting squares
        self.selected = None
        #var for mouse position tracking
        self.mousePos = None
        #state variable
        self.state = "paused"
        #custom event for timer
        self.timerEvent = pygame.USEREVENT
        #arrays for storing live cells
        self.pos_arr = []
        self.timer_tick= 1000
        #array for storing all cells
        self.buffer_arr = []

    # setting conditions for running, while updating and drawing to the screen what we pass through draw
    def run(self):
        #fill the grid with white
        self.window.fill(WHITE)
        ## need to handle the timer being sued based off what state im in, outside of the while loop, need to write function
        # def timeselect(self):
        #   if whatever:
        #       pygame.time.set_timer(self.timerEvent, 100)

        pygame.time.set_timer(self.timerEvent, self.timer_tick)


        #while running
        while self.running:

            if self.state == "playing":
                self.playing_events()
                self.playing_update()


            if self.state == "paused":
                self.paused_events()
                self.paused_update()
                self.paused_draw()

            if self.state == "reset":
                self.reset_events()
                self.reset_update()
                self.reset_draw()
                self.state = "paused"



            if self.running == False:
                pygame.quit()
                sys.exit()
        #basically an event handler, constantly being checked by the run method

############PAUSED STATE###################
    def paused_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            #if the Lmouse button is pressed down on an index that isnt in the pos array
            if event.type == pygame.MOUSEBUTTONDOWN and self.mouseOnGrid() and self.pos_arr.count(self.mouseOnGrid()) < 1:
                self.selected = self.mouseOnGrid()

                if event.button == 1:
                    self.drawSelectionBlack(self.window, self.selected)
                    self.pos_arr.append(self.selected)
                    print(f"pos_arr: {self.pos_arr}")
            #if the Rmouse is pressed down on an index that is in the pos array
            if event.type == pygame.MOUSEBUTTONDOWN and self.mouseOnGrid() and self.pos_arr.count(self.mouseOnGrid()) == 1:
                self.selected = self.mouseOnGrid()

                if event.button == 3:
                    self.drawSelectionWhite(self.window, self.selected)
                    self.pos_arr.remove(self.selected)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.state = "playing"
                    print(self.state)




    def paused_update(self):
        #sets mouse Pos equal to the position of the mouse
        self.mousePos = pygame.mouse.get_pos()



    #draws to the screen and updates
    def paused_draw(self):
        self.drawGrid(self.window)
        pygame.display.update()


############PLAYING STATE################
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.state = "paused"
                    print(self.state)
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.USEREVENT:
                print("tick")
                self.gameOfLife()


    def playing_update(self):
        #sets mouse Pos equal to the position of the mouse
        self.mousePos = pygame.mouse.get_pos()


    #draws to the screen and updates
    def playing_draw(self):
        #for each button object in the button array, draw the button in the window
            #if self.selected and
        for pos in self.buffer_arr:
            self.drawSelectionBlack(self.window, pos)

        for pos in self.pos_arr:
            if self.buffer_arr.count(pos) < 1:
                self.drawSelectionWhite(self.window, pos)
        self.drawGrid(self.window)
        pygame.display.update()





    ###########RESET FUNCTIONS################
    def reset_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def reset_update(self):
        #sets mouse Pos equal to the position of the mouse
        self.mousePos = pygame.mouse.get_pos()
    #draws to the screen and updates
    def reset_draw(self):
        #for each button object in the button array, draw the button in the window

            #if self.selected and
        self.window.fill(WHITE)
        self.drawGrid(self.window)
        pygame.display.update()


############HELPER FUNCTIONS################
    def drawSelectionBlack(self, window, pos):
        #if cell is live == true

        pygame.draw.rect(window, BLACK, ((pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize)+ gridPos[1], cellSize, cellSize))
        pygame.display.update()

    def drawSelectionWhite(self , window , pos):
        pygame.draw.rect(window, WHITE, ((pos[0] * cellSize)+ gridPos[0], (pos[1] * cellSize)+ gridPos[1], cellSize, cellSize))
        pygame.display.update()

        #else pygame.draw.rect(window, WHITE, ((pos[0] * cellSize)+ gridPos[0], (pos[1]* cellSize)+gridPos[1], cellSize, cellSize))

    def drawGrid(self, window):
        #draws the outside lines on the grid
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH - 150, HEIGHT - 150), 2)
        #for loop to make 9 of each of these lines
        for x in range (25):
            #draw a black line virtically
            pygame.draw.line(window, BLACK, (gridPos[0] + (x*cellSize), gridPos[1]), (gridPos[0] + (x*cellSize), gridPos[1] + 625) )
            #draw a black line horizontally
            pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x*cellSize) ), (gridPos[0] + 625 , gridPos[1] + (x*cellSize) ) )

    def mouseOnGrid(self):
        #if the x and y cordinates of the mouse are not both inside of the grid, return false
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] <gridPos[1]:
            return False
        if self.mousePos[0] > gridPos[0] + gridSize or self.mousePos[1] > gridPos[1] + gridSize:
            return False
        #else return the index of the grid position the mouse is in
        return ((self.mousePos[0] - gridPos[0])//cellSize, (self.mousePos[1] - gridPos[1])//cellSize)



    ### set rules of life, return cell back to array, if cell does not live changes the color of the cell to white, else returns cell
    def gameOfLife(self):
        print(f"game of life running{self.pos_arr}")
        if len(self.pos_arr):
            for pos in self.pos_arr:
                self.doesCellLive(pos)
        self.playing_draw()
        self.pos_arr = self.buffer_arr
        self.buffer_arr = []
#Any live cell with two or three live neighbours survives.
#Any dead cell with three live neighbours becomes a live cell.
#All other live cells die in the next generation. Similarly, all other dead cells stay dead.
# I NEED A SEPERATE FUNCTION FOR DETERMINING IF DEAD CELLS SHOULD LIVE IT WILL CHECK EVERY CURRENT LIVE CELL AND FOR EACH ADJACENT CELL CHECK TO SEE IF IT HAS 3 LIVE CELLS ADJACENT
#NEED SEPERATE ARRAY FOR HOLDING CELLS THAT ARE GOING TO LIVE SO THAT THE POS ARRAY DOESNT GET ALTERED BEFORE THE COMPUTATION IS DONE
# I ALSO NEED A CONDITION FOR THIS FUNCTION FOR IF THE CELL IS AT THE EDGE OF THE BOARD
    def doesCellLive(self, pos):
        count = 0
        adjacent_cells = []
        #check right node
        if self.pos_arr.count( ((pos[0] + 1), pos[1]) ) == 1 :
            count += 1

        #check to see if there is a daed cell on the right
        else:
            if pos[0] < 25:
                adjacent_cells.append( ((pos[0] + 1), pos[1]) )
        #check left node
        if self.pos_arr.count( ((pos[0] - 1), pos[1]) ) == 1:
            count += 1

        #check to see if there is a daed cell on the left
        else:
            if pos[0] > 0:
                adjacent_cells.append( ((pos[0] - 1), pos[1]) )
        #check bottom node
        if self.pos_arr.count( (pos[0], (pos[1] - 1)) ) == 1:
            count += 1

        #check to see if there is a daed cell on the bottom
        else:
            if pos[1] < 25:
                adjacent_cells.append( (pos[0], (pos[1] - 1)) )
        #check top node
        if self.pos_arr.count( (pos[0], (pos[1] + 1)) ) == 1:
            count += 1

        #check to see if there is a daed cell on the top
        else:
            if pos[1] > 0:
                adjacent_cells.append((pos[0], (pos[1] + 1)))
        #check bottom left
        if self.pos_arr.count( ((pos[0] - 1), (pos[1] - 1)) ) == 1:
            count += 1

        #check to see if there is a daed cell on the bottom left
        else:
            if pos[1] < 25 and pos[0] > 0:
                adjacent_cells.append( ((pos[0] - 1), (pos[1] - 1)) )
        #check bottom right
        if self.pos_arr.count( ((pos[0] + 1), (pos[1] - 1)) ) == 1:
            count += 1

        #check to see if there is a daed cell on the bottom right
        else:
            if pos[1] < 25 and pos[0] < 25:
                adjacent_cells.append( ((pos[0] + 1), (pos[1] - 1)) )
        #check top right
        if self.pos_arr.count( ((pos[0] + 1), (pos[1] + 1)) ) == 1:
            count += 1

        #check to see if there is a daed cell on the top right
        else:
            if pos[1] > 0 and pos[0] < 25:
                adjacent_cells.append( ((pos[0] + 1), (pos[1] + 1)) )
        #check top left
        if self.pos_arr.count( ((pos[0] - 1), (pos[1] + 1)) ) == 1:
            count += 1

        #check to see if there is a daed cell on the top left
        else:
            if pos[1] > 0 and pos[0] > 0:
                adjacent_cells.append( ((pos[0] - 1), (pos[1] + 1)) )
        #check if cell is on the edge
        if pos[0] == 0 or pos[0] == 25 or pos[1] == 0 or pos[1] == 25:
            self.pos_arr.remove(pos)

        print(f"count in doesCellLive{count}")
        #see if cell does not have enough live neighbours to live
        if count < 2 or count >3:
            self.makeLiveCells(adjacent_cells)

            # if the pos passes all tests
        else:
            self.makeLiveCells(adjacent_cells)
            if self.buffer_arr.count(pos) < 1:
                self.buffer_arr.append(pos)
                print(f"buffer_arr in doesCellLive: {self.buffer_arr}")

    def makeLiveCells(self, adj_arr):

        for pos in adj_arr:
            count = 0
            #check right node
            if self.pos_arr.count( ((pos[0] + 1), pos[1]) ) == 1 :
                count += 1


            #check left node
            if self.pos_arr.count( ((pos[0] - 1), pos[1]) ) == 1:
                count += 1

            #check bottom node
            if self.pos_arr.count( (pos[0], (pos[1] - 1)) ) == 1:
                count += 1

            #check top node
            if self.pos_arr.count( (pos[0], (pos[1] + 1)) ) == 1:
                count += 1

            #check bottom left
            if self.pos_arr.count( ((pos[0] - 1), (pos[1] - 1)) ) == 1:
                count += 1

            #check bottom right
            if self.pos_arr.count( ((pos[0] + 1), (pos[1] - 1)) ) == 1:
                count += 1

            #check top right
            if self.pos_arr.count( ((pos[0] + 1), (pos[1] + 1)) ) == 1:
                count += 1

            #check top left
            if self.pos_arr.count( ((pos[0] - 1), (pos[1] + 1)) ) == 1:
                count += 1
            #if there are 3 adjacent cells then it lives
            if count == 3 and self.buffer_arr.count(pos) < 1:
                self.buffer_arr.append(pos)
                print(f"buffer_arr in makeLiveCells: {self.buffer_arr}")

    #puses or plays the game
    def pausePlay(self):
        if self.state == "playing":
            self.state == "paused"
    #resets the game
    def reset(self):
        self.state == "reset"
    #makes the game go faster
    def faster(self):
        self.timer_tick += 100
    #makes the game go slower
    def slower(self):
        self.timer_tick -= 100




    ###########TODO##########
    #write a class for cells
    #done?


    #maby write a function to change the colors first, then have a function locating the x, y coordinates of live cells, and then another function for operating on the timer ticks and killing/creating live cells
    #found to be obsolete, can be handled in the class of the cell

    #figure out timer implamentation
        #i think i got this but im not sure where to put it in my application
        #CURRENT STATUS: TIMER DOESNT PRINT UNLESS IM MOVING THE APPLICATION?? pretty sure im not understanding how the state works, or the how the timer works

    # find a way to track cells and feed either WHITE or BLACK to the color if it is alive or not
        # i think  an object for cells is the way to go here and then change white or black passed as the variable for if its live or not
        # have an array of all cell objects check the variable for color or every cell x and y value 1 cellsize away in all directions may not work for diagonal
        #CURRENT STATUS: CELLCLASS HAS BEEN CREATED BUT IM NOT SURE IF IT HAS ALL THE PARAMETERS IT NEEDS, AND I HAVE YET TO FIND A SOLUCTION TO LOCATING ADJACENT CELLS

    #write function for handling if a cell is alive or not
        # LOL WHAT AM I DOING


    #write state functions play, paused, reset, and load preset

        #currently play i think is what paused needs to operate as, and then play would start the algorythm until no more live cells, or the player stops it
        #CURRENT STATUS: HAVE A FUNCTION TO HANDLE RESET BUT IM NOT SURE IT WILL WORK AFTER THE OBJECTS ARE IMPLAMENTED, MAY NEED TO CHANGE THE LIVE VARIABLE TO FALSE FOR ALL CELLS FOR IT TO WORK PROPERLY.

    #reserch Surface objects, images
