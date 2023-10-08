import tkinter as tk
from tkinter import IntVar, StringVar, ttk
import ValidScoreStrings

#  Set Globals
windowSize = (1300, 300)
windowTitle = 'Python Bowling Scoreboard Test'
scoreCharacters = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '/', 'X' ]
scoreFixes = { 'x': 'X', '\\': '/' }

#  Calculated Globals
sidePadding = int(windowSize[0] / 100)
topRowHeight = (windowSize[1] / 10)
scoreFrameSize = (int((windowSize[0] - (sidePadding * 2)) / 13), int((windowSize[1] - (sidePadding * 2)) / 3))


#  Program class, for managing the program and the main window and loop
class Program(tk.Tk):
    def __init__(self, windowTitle, windowSize):
        #  Initial Window Setup
        super().__init__()
        self.title(windowTitle)
        self.geometry(f'{windowSize[0]}x{windowSize[1]}')
        self.minsize(windowSize[0], windowSize[1])
        self.resizable(width=False, height=False)
        self.wm_attributes('-transparentcolor','magenta')
        self.protocol("WM_DELETE_WINDOW", self.closeWindow)

        #  Primary Element: the scoreboard
        self.scoreBoard = Scoreboard(self, (0, 0), (1.0, 1.0))

        #  Main Loop
        self.mainloop()

    def closeWindow(self):
        self.destroy()


#  Scoreboard class, for creating a managed tkinter frame to hold all scoreboard elements inside
class Scoreboard(tk.Frame):
    def __init__(self, parent, pos, relSize):
        super().__init__(parent)
        self.place(x=pos[0], y=pos[1], relwidth=relSize[0], relheight=relSize[1])

        #  Create the top row, a black spot above the name and then a frame index for each score frame as well as a space above the total score
        self.createTopRow()
        
        #  Create the bowler name frame, all ten scoring frames, and a space for the total score
        self.scoreboardRow = ScoreboardRow(self)

        self.resetButton = tk.Button(self, text = 'RESET', bd='5', command=self.reset)
        self.resetButton.place(relx=0.5, rely=0.75, relwidth=0.1, anchor='center')


    def createTopRow(self):
        #  Create the 10 spots above the score board entries for the score indices
        for i in range(10):
            scoreIndexFrame = tk.Frame(self, borderwidth=2, relief='sunken')
            scoreIndexFrame.place(x=sidePadding + (scoreFrameSize[0] * 2) + (scoreFrameSize[0] * i), y=sidePadding, width=scoreFrameSize[0], height=topRowHeight)
            scoreIndexLabel = tk.Label(scoreIndexFrame, text=str(i + 1))
            scoreIndexLabel.place(relx=0.5, rely=0.5, anchor='center')

        #  Create the spot above the total score column to show "TOTAL SCORE" as a column header
        topRight = tk.Frame(self, borderwidth=2, relief='sunken')
        topRight.place(x=sidePadding + scoreFrameSize[0] * 12, y=sidePadding, width=scoreFrameSize[0], height=topRowHeight)
        scoreIndexLabel = tk.Label(topRight, text="TOTAL SCORE")
        scoreIndexLabel.place(relx=0.5, rely=0.5, anchor='center')

    def reset(self):
        self.scoreboardRow.resetAllValues()



class ScoreboardRow():
    def __init__(self, parent):
        super().__init__()
        self.createNameFrame(parent, (sidePadding, sidePadding + topRowHeight), (scoreFrameSize[0] * 2, scoreFrameSize[1]), "Drew")
        self.scoringFrames = []
        for i in range(10):
            self.scoringFrames.append(FrameScoreEntry(parent, i, (sidePadding + scoreFrameSize[0] * 2 + (i * scoreFrameSize[0]), sidePadding + topRowHeight), scoreFrameSize, (i == 9), (i == 0), self.scoreboardUpdate))
        self.totalValueStr = self.createTotalScoreFrame(parent, (sidePadding + scoreFrameSize[0] * 12, sidePadding + topRowHeight), scoreFrameSize)
        self.defineJumpElements()


    def defineJumpElements(self):
        for i in range(9):
            self.scoringFrames[i].scoreVars[0].jumpElements = (self.scoringFrames[i].scoreVars[1], self.scoringFrames[i + 1].scoreVars[0])
            self.scoringFrames[i].scoreVars[1].jumpElements = (self.scoringFrames[i + 1].scoreVars[0], self.scoringFrames[i + 1].scoreVars[0])
        self.scoringFrames[9].scoreVars[0].jumpElements = (self.scoringFrames[9].scoreVars[1], self.scoringFrames[9].scoreVars[1])
        self.scoringFrames[9].scoreVars[1].jumpElements = (self.scoringFrames[9].scoreVars[2], self.scoringFrames[9].scoreVars[2])
        self.scoringFrames[9].scoreVars[2].jumpElements = (None, None)


    def scoreboardUpdate(self):
        for e in self.scoringFrames:
            e.validateScores(False)

        #  For each frame score entry, set the updated total if a spare or a strike has valid scores to add
        lastFrameComplete = True
        for i in range(len(self.scoringFrames)):
            #  Grab the FrameScoreEntry, and ensure we enable each according to if the previous one is complete and enabled
            fse = self.scoringFrames[i]
            fse.setFrameScoreEnabled(lastFrameComplete)
            lastFrameComplete = fse.frameComplete and lastFrameComplete

            # If we're in the first nine frames, determine extra points for spares and strikes
            if (fse.frameIndex < (len(self.scoringFrames) - 1)):
                if (fse.scoreVars[1].entryStrVar.get() == '/'):
                    next = self.scoringFrames[i + 1]
                    scoreVals = next.scoreValuesList
                    fse.setTotalValue(fse.totalIntVar.get() + scoreVals[0])
                elif (fse.scoreVars[0].entryStrVar.get() == 'X'):
                    next = self.scoringFrames[i + 1]
                    scoreVals = next.scoreValuesList
                    if (len(scoreVals) < 2):
                        twoUp = self.scoringFrames[i + 2]
                        scoreVals = scoreVals + twoUp.scoreValuesList
                    fse.setTotalValue(fse.totalIntVar.get() + scoreVals[0] + scoreVals[1])

        #  Loop through again, and this time update the current score as of each frame based on previous values
        totalAsOf = 0
        for fse in self.scoringFrames:
            totalAsOf += fse.totalIntVar.get()
            fse.setTotalValue(totalAsOf)

        # Set the total end score under the TOTAL SCORE column
        self.totalValueStr.set(str(totalAsOf))


    def createNameFrame(self, parent, framePos, size, name):
        nameFrame = tk.Frame(parent, borderwidth=2, relief='sunken')
        nameFrame.place(x=framePos[0], y=framePos[1], width=size[0], height=size[1])
        nameLabel = tk.Label(nameFrame, text=name.upper(), font=("Arial", 25))
        nameLabel.place(relx=0.5, rely=0.5, anchor='center')
    

    def createTotalScoreFrame(self, parent, framePos, size):
        totalFrame = tk.Frame(parent, borderwidth=2, relief='sunken')
        totalFrame.place(x=framePos[0], y=framePos[1], width=size[0], height=size[1])
       
        totalValueStr = StringVar()
        totalLabel = tk.Label(totalFrame, text="", font=('Helvetica 22'), textvariable=totalValueStr)
        totalLabel.place(relx=0.5, rely=0.5, anchor='center')
        return totalValueStr
    
    def resetAllValues(self):
        for sfe in self.scoringFrames:
            sfe.resetValues()
        self.scoringFrames[0].validateScores(True)
        self.scoringFrames[0].scoreVars[0].entryEntry.focus()



# FrameScoreEntry (vars: frameIndex, tenth, disabled, frameComplete, scoreVars, totalStrVar, totalIntVar, entryTotalLabel, scoreValuesList)
class FrameScoreEntry(tk.Frame):
    def __init__(self, parent, frameIndex, framePos, size, tenth, enabled, updateCallback):
        super().__init__(parent, borderwidth=2, relief="sunken")
        self.place(x=framePos[0], y=framePos[1], width=size[0], height=size[1])

        #  Determine the size of the 2 (or if onthe tenth frame, 3) score entry boxes
        boxSize = (int(size[0]/2), int(size[1]/2)) if not tenth else (int(size[0]/3), int(size[1]/2))

        #  Store off the score entry frames
        self.frameIndex = frameIndex
        self.tenth = tenth
        self.enabled = enabled
        self.frameComplete = False
        self.scoreVars = []
        self.updateCallback = updateCallback

        self.scoreVars.append(ScoreEntryFrame(self, (boxSize[0] * 0, 0), frameIndex, 0, boxSize, self.tenth, enabled, self.validateScores))
        self.scoreVars.append(ScoreEntryFrame(self, (boxSize[0] * 1, 0), frameIndex, 1, boxSize, self.tenth, False, self.validateScores))
        if tenth:
            self.scoreVars.append(ScoreEntryFrame(self, (boxSize[0] * 2, 0), frameIndex, 2, boxSize, self.tenth, False, self.validateScores))

        self.totalStrVar = StringVar()
        self.totalIntVar = IntVar()
        self.entryTotalLabel = tk.Label(self, text="", font=('Helvetica 22'), textvariable=self.totalStrVar)
        self.entryTotalLabel.place(relx=0.5, rely=0.75, anchor='center')
        self.scoreValuesList = []


    def setFrameScoreEnabled(self, enabled):
        color = "red" if not enabled else "cyan"
        self.config(background=color)
        self.enabled = enabled
        if (self.enabled == True):
            self.scoreVars[0].enable()
        else:
            for e in self.scoreVars:
                e.disable()

    def enableCount(self, count):
        for e in self.scoreVars:
            e.enabled = False
            e.disable()
        for i in range(count):
            self.scoreVars[i].enable()

    def resetValues(self):
        for sef in self.scoreVars:
            sef.clearValue()
    
    def getScoreString(self):
        stringVal = ""
        for e in self.scoreVars:
            value = e.entryStrVar.get()
            stringVal += ('_' if (value == '') else value)
        return stringVal
    
    def setTotalValue(self, totalVal):
        self.totalIntVar.set(totalVal)
        self.totalStrVar.set(str(self.totalIntVar.get()))

    def validateScores(self, doUpdate):
        validAddition = False
        stringVal = self.getScoreString()
        if stringVal not in ValidScoreStrings.List:
            index = len(self.scoreVars) - 1
            while (stringVal not in ValidScoreStrings.List):
                self.scoreVars[index].clearValue()
                index = index - 1
                stringVal = self.getScoreString()
        else:
            validAddition = True

        entry = ValidScoreStrings.List[stringVal]
        self.setTotalValue(entry[0])
        self.enableCount(entry[1])
        self.frameComplete = entry[2]
        self.scoreValuesList = entry[3]
        
        if doUpdate:
            self.updateCallback()

        return validAddition



# ScoreEntryFrame (vars: frameIndex, scoreIndex, tenth, disabled, entryStrVar, entryEntry)
class ScoreEntryFrame(tk.Frame):
    def __init__(self, parent, pos, frameIndex, scoreIndex, boxSize, tenth, enabled, updateCallback):
        super().__init__(parent, borderwidth=1, relief='flat')
        self.place(x=pos[0], y=pos[1], width=boxSize[0], height=boxSize[1])
        self.frameIndex = frameIndex
        self.scoreIndex = scoreIndex
        self.tenth = tenth
        self.enabled = enabled
        self.updateCallback = updateCallback
        self.jumpElements = (None, None)

        self.entryStrVar = StringVar()
        self.entryStrVar.trace("w", lambda name, index, mode, var=self.entryStrVar: self.validateScoreEntry())

        self.entryEntry = tk.Entry(self, justify=tk.CENTER, font=('Helvetica 22'), textvariable=self.entryStrVar)
        self.entryEntry.place(relx=0.5, rely=0.5, width=int(boxSize[0] * 0.8), height=int(boxSize[1] * 0.8), anchor='center')

        if not self.enabled:
            self.entryEntry.config(state="disabled")

    
    def clearValue(self):
        self.entryStrVar.set('')

    def disable(self):
        self.enabled = False
        self.entryEntry.config(state="disabled")

    def enable(self):
        self.enabled = True
        self.entryEntry.config(state="normal")


    def validateScoreEntry(self):
        content = self.entryStrVar.get()
        if (len(content) > 1):
            self.entryStrVar.set(content[0:1])
            content = self.entryStrVar.get()

        if (content in scoreFixes):
            self.entryStrVar.set(scoreFixes[content])
            content = self.entryStrVar.get()

        if (content not in scoreCharacters):
            self.clearValue()
            content = self.entryStrVar.get()

        #  If the content we set to was valid, jump if able
        if self.updateCallback(True):
            if (content != 'X' and self.jumpElements[0] != None):
                self.jumpElements[0].entryEntry.focus()
            elif (self.jumpElements[1] != None):
                self.jumpElements[1].entryEntry.focus()



Program(windowTitle, windowSize)