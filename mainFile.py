from cmu_112_graphics import *
import math
import random

class Snake(object):
    def __init__(self):
        self.length = 0
        self.color = "blue"
        self.headAngle = 0
        self.headX = 200
        self.headY = 200
        self.speed = 30
        self.angleOffset = 315
        self.health = 30
        self.size = 16
        self.segments = 1

    def drawSnakeHead(self, app, canvas):
            cx = self.headX
            cy = self.headY
            # head base
            offAngle = 20
            cos1 = math.cos((self.headAngle+self.angleOffset+offAngle)*math.pi/180)*self.size
            cos2 = math.cos((self.headAngle+self.angleOffset-offAngle)*math.pi/180)*self.size
            sin1 = math.sin((self.headAngle+self.angleOffset+offAngle)*math.pi/180)*self.size
            sin2 = math.sin((self.headAngle+self.angleOffset-offAngle)*math.pi/180)*self.size
            canvas.create_polygon(cx+cos2,cy-sin2,
                                    cx+cos1,cy-sin1,

                                    cx-sin2,cy-cos2,
                                    cx-sin1,cy-cos1,

                                    cx-cos2,cy+sin2,
                                    cx-cos1,cy+sin1,

                                    cx+sin2,cy+cos2,
                                    cx+sin1,cy+cos1, fill="brown"
                                    )
            # mouth base
            h = self.size*math.sin(70*math.pi/180)/math.sin(90*math.pi/180)
            inSize = self.size*math.sin(25*math.pi/180)/math.sin(135*math.pi/180)
            mcos1 = cos2
            msin1 = sin2
            mCosMid = math.cos((self.headAngle+self.angleOffset)*math.pi/180)*h
            mSinMid = math.sin((self.headAngle+self.angleOffset)*math.pi/180)*h
            mCosIn = math.cos((self.headAngle+self.angleOffset)*math.pi/180)*inSize
            mSinIn = math.sin((self.headAngle+self.angleOffset)*math.pi/180)*inSize
            canvas.create_polygon(
                                    cx+mCosIn,cy-mSinIn,
                                    cx+mCosMid,cy-mSinMid,
                                    cx+cos1,cy-sin1,
                                    
                                    cx-sin2,cy-cos2,
                                    cx-mSinMid,cy-mCosMid,
                                    cx-mSinIn,cy-mCosIn
                                    )
            # teeth
            teethAngle = (self.headAngle+self.angleOffset)
            canvas.create_line(cx+mCosIn,cy-mSinIn,
                                cx+math.cos((teethAngle+25)*math.pi/180)*self.size*0.7,cy-math.sin((teethAngle+25)*math.pi/180)*self.size*0.7,
                                fill="khaki", width = 5)

            canvas.create_line(cx-mSinIn,cy-mCosIn,
                                cx-math.sin((teethAngle-25)*math.pi/180)*self.size*0.7,cy-math.cos((teethAngle-25)*math.pi/180)*self.size*0.7,
                                fill="khaki", width = 5)
        
    def drawSnakeBody(self, app, canvas):
        # counter = 0
        bodyColor = ["indian red","brown"]
        for elem in app.snakePositions:
            # if counter % int(self.size+1) == 0:
            offAngle = 20
            cos1 = math.cos((elem[2]+offAngle)*math.pi/180)*self.size
            cos2 = math.cos((elem[2]-offAngle)*math.pi/180)*self.size
            sin1 = math.sin((elem[2]+offAngle)*math.pi/180)*self.size
            sin2 = math.sin((elem[2]-offAngle)*math.pi/180)*self.size
            cx = elem[0]
            cy = elem[1]
            canvas.create_polygon(cx+cos2,cy-sin2,
                                    cx+cos1,cy-sin1,

                                    cx-sin2,cy-cos2,
                                    cx-sin1,cy-cos1,

                                    cx-cos2,cy+sin2,
                                    cx-cos1,cy+sin1,

                                    cx+sin2,cy+cos2,
                                    cx+sin1,cy+cos1, fill=bodyColor[0]
                                    )
            bodyColor.reverse()
            # counter += 1

def gameDimensions():
    rows = 100
    cols = 150
    cellSize = 8
    margin = 0
    return (rows, cols, cellSize, margin)

def appStarted(app):
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.grid = [([None]*app.cols) for row in range(app.rows)]
    app.isWaitingForFirstKey = True 
    app.foodList = []
    app.timerDelay = 250
    app.count = 0
    app.isGameOver = False
    app.tookTooLong = False
    app.snake = Snake()
    app.angularAcc = 150*math.pi/180
    app.snakePositions = [(200,200,315)]
    app.person = app.scaleImage(app.loadImage('person.png'), 1/9)
    app.cow = app.scaleImage(app.loadImage('cow.png'), 1/8)
    app.monster = app.scaleImage(app.loadImage('monster.png'), 1/7)
    app.car = app.scaleImage(app.loadImage('car.png'), 1/6)
    app.skyscraper = app.scaleImage(app.loadImage('skyscraper.png'), 3/8)
    app.building = app.scaleImage(app.loadImage('building.png'), 2/8)
    app.background = app.loadImage('background.png')

def getCell(app, x, y):
    gridWidth  = app.width
    gridHeight = app.height
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    row = int((y) / cellHeight)
    col = int((x) / cellWidth)

    return (row, col)

def timerFired(app):
    if app.isGameOver == True:
        return
    if app.isWaitingForFirstKey == False:
        app.count+=1
        try:
            if app.count%8 == 0:
                app.foodList+=[Person(app.rows, app.cols, app.grid)]
            if app.count%30 == 0:
                app.foodList+=[Cow(app.rows, app.cols, app.grid)]
            if app.count%22 == 0:
                app.foodList+=[Car(app.rows, app.cols, app.grid)]
            if app.count%57 == 0:
                app.foodList+=[Monster(app.rows, app.cols, app.grid)]
            if app.count%70 == 0:
                app.foodList+=[Building(app.rows, app.cols, app.grid)]
            if app.count%100 == 0:
                app.foodList+=[Skyscraper(app.rows, app.cols, app.grid)]
        except:
            app.isGameOver = True
            app.tookTooLong = True
        
        for food in app.foodList:
            getDirection(app)
            if isinstance(food, MovementFood):
                try:
                    food.r, food.c = food.movement(food.r, food.c, app.grid, 
                    food.size, app.dx, app.dy)
                except:
                    app.isGameOver = True
                    app.tookTooLong = True
        #snake functions
        for (x,y,angle) in app.snakePositions:
            row, col = getCell(app, x, y)
            app.grid[row][col] = None

        app.snakePositions.pop()
        app.snakePositions.insert(0,(app.snake.headX,app.snake.headY,app.snake.headAngle+app.snake.angleOffset))
        
        app.snake.headX += app.snake.speed*math.cos(app.snake.headAngle*math.pi/180)
        app.snake.headY -= app.snake.speed*math.sin(app.snake.headAngle*math.pi/180)
        
        snakeHeadRow, snakeHeadCol = getCell(app, app.snake.headX,app.snake.headY)

        popped = 0
        for i in range(len(app.foodList)):
            for r in range(app.foodList[i-popped].size+2):
                for c in range(app.foodList[i-popped].size+2):
                    if ((app.foodList[i-popped].r + r == snakeHeadRow) and 
                    (app.foodList[i-popped].c + c == snakeHeadCol)):
                        if app.snake.size >= app.foodList[i-popped].size*app.cellSize*0.5:
                            app.foodList.pop(i-popped)
                            popped += 1
                            app.snake.segments += 1 
                            app.snake.size *= 1.1
                            # (oldX, oldY, angle) = app.snakePositions[-1] 
                            # newX = oldX + (app.snake.segments*app.snake.size)
                            # newY = oldY + (app.snake.segments*app.snake.size)
                            # app.snakePositions.append((newX, newY, angle))

                            app.snakePositions.insert(0,(app.snake.headX,app.snake.headY,app.snake.headAngle+app.snake.angleOffset))
                            
                        else:
                            if app.snake.segments - 1 ==0:
                                app.isGameOver = True 
                            app.snake.size*=.9
                            app.snake.segments -= 1 
                            app.snakePositions.pop()
                            app.foodList.pop(i-popped)
                            popped += 1
        
        if app.snake.headX > app.width - app.snake.size:
            app.snake.headX = 0 + app.snake.size
        if app.snake.headX - app.snake.size < 0:
            app.snake.headX = app.width - app.snake.size
        if app.snake.headY > app.height - app.snake.size:
            app.snake.headY = 0 + app.snake.size
        if app.snake.headY < 0 + app.snake.size:
            app.snake.headY = app.height - app.snake.size
            
        for (x,y,angle) in app.snakePositions:
                row, col = getCell(app, x, y)
                app.grid[row][col] = 'F'

def getDirection(app):
    app.dx = random.randrange(-1,1)
    app.dy = random.randrange(-1,1)
    
def keyPressed(app, event):
    app.isWaitingForFirstKey = False 
    if event.key == "a" or event.key == "Left":
        # turn left
        app.snake.headAngle += app.angularAcc
    if event.key == "d" or event.key == "Right":
        # turn right
        app.snake.headAngle -= app.angularAcc
    if event.key == 'r':
        appStarted(app)

#inits a grid
def drawGrid(app,canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col)

#populates the grid
def drawCell(app, canvas, row, col):
    color = 'blue'
    startX = app.margin
    startY = app.margin
    canvas.create_rectangle(startX+col*app.cellSize,startY+row*app.cellSize,
                        startX+(col+1)*app.cellSize,startY+(row+1)*app.cellSize,
                        fill = color, outline = color, width = 3)

def drawFood(app, canvas, FoodList):
    for food in FoodList:
        if isinstance(food,Person):
            # canvas.create_oval(food.c*app.cellSize, food.r*app.cellSize,
            #                     (food.c+food.size)*app.cellSize,
            #                     (food.r+food.size)*app.cellSize, fill="yellow")
            canvas.create_image((food.c*app.cellSize+(food.c+food.size)*app.cellSize)/2,
                                (food.r*app.cellSize+(food.r+food.size)*app.cellSize)/2, image=ImageTk.PhotoImage(app.person))
        
        elif isinstance(food, Cow):
            # canvas.create_oval(food.c*app.cellSize, food.r*app.cellSize,
            #                     (food.c+food.size)*app.cellSize,
            #                     (food.r+food.size)*app.cellSize, fill="white")
            canvas.create_image((food.c*app.cellSize+(food.c+food.size)*app.cellSize)/2,
                                (food.r*app.cellSize+(food.r+food.size)*app.cellSize)/2,
                                image=ImageTk.PhotoImage(app.cow))
        
        elif isinstance(food, Monster):
            # canvas.create_oval(food.c*app.cellSize, food.r*app.cellSize,
            #                     (food.c+food.size)*app.cellSize,
            #                     (food.r+food.size)*app.cellSize, fill="green")
            canvas.create_image((food.c*app.cellSize+(food.c+food.size)*app.cellSize)/2,
                                (food.r*app.cellSize+(food.r+food.size)*app.cellSize)/2,
                                image=ImageTk.PhotoImage(app.monster))
        
        elif isinstance(food, Car):
            # canvas.create_rectangle(food.c*app.cellSize, food.r*app.cellSize,
            #                     (food.c+food.size)*app.cellSize,
            #                     (food.r+food.size)*app.cellSize, fill="red")
            #canvas.create_image((food.c+food.size*0.5)*app.cellSize,
                                #(food.c+food.size)*app.cellSize,
                                #image = ImageTk.PhotoImage(self.img))
            canvas.create_image((food.c*app.cellSize+(food.c+food.size)*app.cellSize)/2,
                    (food.r*app.cellSize+(food.r+food.size)*app.cellSize)/2,
                    image=ImageTk.PhotoImage(app.car))
        
        elif isinstance(food, Building):
            # canvas.create_rectangle(food.c*app.cellSize, food.r*app.cellSize,
            #                     (food.c+food.size)*app.cellSize,
            #                     (food.r+food.size)*app.cellSize, fill="maroon")
            canvas.create_image((food.c*app.cellSize+(food.c+food.size)*app.cellSize)/2,
                    (food.r*app.cellSize+(food.r+food.size)*app.cellSize)/2,
                    image=ImageTk.PhotoImage(app.building))
        
        elif isinstance(food, Skyscraper):
            # canvas.create_rectangle(food.c*app.cellSize, food.r*app.cellSize,
            #                     (food.c+food.size)*app.cellSize,
            #                     (food.r+food.size)*app.cellSize, fill="yellow")
            canvas.create_image((food.c*app.cellSize+(food.c+food.size)*app.cellSize)/2,
                    (food.r*app.cellSize+(food.r+food.size)*app.cellSize)/2,
                    image=ImageTk.PhotoImage(app.skyscraper))

def redrawAll(app, canvas):
    drawGrid(app, canvas)
    canvas.create_image(app.width/2,
        app.height/2,
        image=ImageTk.PhotoImage(app.background))
    drawFood(app, canvas, app.foodList)
    app.snake.drawSnakeBody(app, canvas)
    app.snake.drawSnakeHead(app, canvas)   
    canvas.create_text(100, 50, text=f'Size:{int(app.snake.size)}',font='Arial 30 bold')    
    if app.isGameOver == True:
        canvas.create_rectangle(0, 0, 1200, 800, fill = 'sky blue')
        canvas.create_text(app.width/2, app.height/2, text="The Tsunami Ate You!! See Sco Support Group", font="Arial 20 bold", fill ="white")
        canvas.create_text(app.width/2, (app.height/2) + 50, text="Press 'r' to Restart!", font="Arial 20 bold", fill ="white")
    if app.isWaitingForFirstKey == True:
        canvas.create_text(600, 355, text="Press any key to start", fill="linen")
        canvas.create_text(600,275, text="Scobell Sandworm", fill="linen", font = "Arial 50 bold")
        canvas.create_text(595,325, text="Scobell Support Game", fill="linen", font = "Arial 25 bold")
        canvas.create_image(300, app.height/2, image=ImageTk.PhotoImage(app.person))
        canvas.create_text(385, app.height/2, text="Size: 8", fill="white", font="Arial 15 bold")
        canvas.create_image(300, app.height/2+50, image=ImageTk.PhotoImage(app.cow))
        canvas.create_text(385, app.height/2+50, text="Size: 16", fill="white", font="Arial 15 bold")
        canvas.create_image(300, app.height/2+100, image=ImageTk.PhotoImage(app.car))
        canvas.create_text(385, app.height/2+100, text="Size: 20", fill="white", font="Arial 15 bold")
        canvas.create_image(300, app.height/2+175, image=ImageTk.PhotoImage(app.monster))
        canvas.create_text(385, app.height/2+175, text="Size: 24", fill="white", font="Arial 15 bold")
        canvas.create_image(550, (app.height/2) + 40, image=ImageTk.PhotoImage(app.building))
        canvas.create_text(550, (app.height/2) - 2, text="Size: 76", fill="linen", font="Arial 15 bold")
        canvas.create_image(550, (app.height/2)+ 225, image=ImageTk.PhotoImage(app.skyscraper))
        canvas.create_text(550, (app.height/2)+ 225, text="Size: 92", fill="white", font="Arial 15 bold")
        
class Food(object):
    def __init__(self, rows, cols, grid):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.size = 5

class StaticFood(Food):
    def __init__(self, rows, cols, grid):
        super().__init__(rows, cols, grid)
        
    
    def placeFoodS(self, rows, cols, grid, size):
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        if self.isSpotTaken(row, col, grid, size):
            return self.placeFoodS(rows, cols, grid, size)
        return row, col

    def isSpotTaken(self, row, col, grid, size):
        for r in range(size):
            for c in range(size):
                if row + r + size > len(grid):
                    return True
                if col + c + size > len(grid[0]):
                    return True
                if grid[row+r][col+c] != None:
                    return True
        return False

class Building(StaticFood):
     def __init__(self, rows, cols, grid):
        super().__init__(rows, cols, grid)
        self.size = 19
        self.r, self.c = self.placeFoodS(self.rows, self.cols, grid, self.size)
        for r in range(self.size):
            for c in range(self.size):
                grid[self.r+r][self.c+c] = 'F'

class Skyscraper(StaticFood):
    def __init__(self, rows, cols, grid):
        super().__init__(rows, cols, grid)
        self.size = 23
        self.r, self.c = self.placeFoodS(self.rows, self.cols, grid, self.size)
        for r in range(self.size):
            for c in range(self.size):
                grid[self.r+r][self.c+c] = 'F'
                
class City(StaticFood):
    def __init__(self, rows, cols, grid):
        super().__init__(rows, cols, grid)
        self.size = 100
        self.r, self.c = self.placeFoodS(self.rows, self.cols, grid, self.size)
        for r in range(self.size):
            for c in range(self.size):
                grid[self.r+r][self.c+c] = 'F'

class World(StaticFood):
    def __init__(self, ):
        super().__init()
        self.size = 1000

class MovementFood(Food):
    def __init__(self, rows, cols, grid):
        super().__init__(rows, cols, grid)

    def placeFoodM(self, rows, cols, grid, size):
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        if self.isSpotTaken(row, col, grid, size):
            return self.placeFoodM(rows, cols, grid, size)
        return row, col

    def isSpotTaken(self, row, col, grid, size):
        for r in range(size):
            for c in range(size):
                if row + r + size > len(grid):
                    return True
                if col + c + size > len(grid[0]):
                    return True
                if grid[row+r][col+c] != None:
                    return True
        return False

    def movement(self, rows, cols, grid, size, dr, dc):
        for r in range(self.size):
            for c in range(self.size):
                grid[rows+r][cols+c] = None
        row = rows + dr
        col = cols + dc
        if self.isSpotTaken(row, col, grid, size):
            dr = random.randrange(-3,3)
            dc = random.randrange(-3,3)
            return self.movement(rows, cols, grid, size, dr, dc)
        for r in range(self.size):
            for c in range(self.size):
                grid[row+r][col+c] = 'F'      
        return row, col
 
class Person(MovementFood):
    def __init__(self, rows, cols, grid):
        super().__init__(rows, cols, grid)
        self.size = 2
        self.r,self.c = self.placeFoodM(self.rows, self.cols, grid, self.size)
        for r in range(self.size):
            for c in range(self.size):
                grid[self.r+r][self.c+c] = 'F'

class Cow(MovementFood):
    def __init__(self, rows, cols, grid):
        super().__init__(rows, cols, grid)
        self.size = 4 
        self.r,self.c = self.placeFoodM(self.rows, self.cols, grid, self.size)
        for r in range(self.size):
            for c in range(self.size):
                grid[self.r+r][self.c+c] = 'F'

class Monster(MovementFood):
    def __init__(self, rows, cols, grid):
        super().__init__(rows, cols, grid)
        self.size = 6
        self.r,self.c = self.placeFoodM(self.rows, self.cols, grid, self.size)
        for r in range(self.size):
            for c in range(self.size):
                grid[self.r+r][self.c+c] = 'F'

class Car(MovementFood):
    def __init__(self, rows, cols, grid):
        super().__init__(rows, cols, grid)
        self.size = 5
        #carImg = self.loadImage('https://toppng.com/public/uploads/preview/car-top-view-11549451806n8nntcut2p.png')
        #self.Img = self.scaleImage(self.image1, 1/5)
        self.r,self.c = self.placeFoodM(self.rows, self.cols, grid, self.size)
        for r in range(self.size):
            for c in range(self.size):
                grid[self.r+r][self.c+c] = 'F'

runApp(width=1200, height=800)
