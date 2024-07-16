interpSpike = "circleIn"
straightName = "meld-nullifier-spike-side"
diagonalName = "meld-nullifier-spike-diagonal"

xy = ["y", "x"]
d4c = [1, 1, -1, -1]

baseIndent = 2


straightOffset = 10.5
diagonalOffset = 7.825

spikeMove = 4
diagonalMove = 2.5
spikeDelay = 0.1
spikeDelayNext = 0.2

def indent(amount):
    for i in range(amount):
        print("\t", end="")

def printIndented(string, amount):
    for i in range(amount):
        string = "\t" + string
    print(string)

def straightPart(rotation):
    indent = baseIndent
    printIndented("{", indent)
    indent += 1
    
    printIndented("name: " + straightName, indent)


    sign = 1
    if(rotation > 1):
        sign = -1
    axis = xy[rotation % 2]
    
    printIndented(axis + ": " + str(straightOffset * sign), indent)
    printIndented("move" + axis.upper() + ": " + str(spikeMove * sign), indent)

    if(rotation != 0):
        #Always offset from the movement axis
        sclAxis = xy[(rotation + 1) % 2]
        printIndented(sclAxis + "Scl" + ": -1", indent)
        printIndented("rotation: " + str(rotation * 90), indent)
        

    #Should be 0 on the first spike
    progress(rotation * 2 * spikeDelay, indent)

    indent -= 1
    printIndented("}", indent)

def diagonalPart(rotation):
    indent = baseIndent
    printIndented("{", indent)
    indent += 1
    
    printIndented("name: " + diagonalName + str(rotation + 1), indent)


    xSign = d4c[rotation % 4]
    ySign = d4c[(rotation + 1) % 4]
    
    printIndented("x: " + str(diagonalOffset * xSign), indent)
    printIndented("y: " + str(diagonalOffset * ySign), indent)
    
    printIndented("moveX: " + str(diagonalMove * xSign), indent)
    printIndented("moveY: " + str(diagonalMove * ySign), indent)

    #Should be 0.1 on the first diagonal spike
    progress((rotation * 2 + 1) * spikeDelay, indent)

    indent -= 1
    printIndented("}", indent)

def progress(timeOffset, prevIndent):
    indent = prevIndent
    
    printIndented("progress: {", indent)
    indent += 1
    printIndented("type: warmup", indent)
    printIndented("ops: [", indent)
    indent += 1

    #Each object done manually. Proabbly a better way out there involving objects
    printIndented("{", indent)
    indent += 1

    printIndented("op: compress", indent)
    printIndented("start: " + str(timeOffset), indent)
    printIndented("end: " + str(timeOffset + spikeDelayNext), indent)
    
    indent -= 1
    printIndented("}", indent)
    printIndented("{", indent)
    indent += 1

    printIndented("op: curve", indent)
    printIndented("interp: circleIn ", indent)
    
    indent -= 1
    printIndented("}", indent)


    #End the madness
    indent -= 1
    printIndented("]", indent)
    indent -= 1
    printIndented("}", indent)
    


for i in range(4):
    straightPart(i)
    diagonalPart(i)
