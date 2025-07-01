
import hjson

indent = 0
indentString = ""
current = ""

def printField(key, value):
    global current
    current += "\n" + indentString + "{0}: {1}".format(key, value)

def printValue(value):
    global current
    current += "\n" + indentString + value

def addIndent(opener):
    global indent
    global indentString
    printValue(opener)
    indent += 1
    indentString += "\t"

def incIndent():
    global indent
    global indentString
    indent += 1
    indentString += "\t"

def removeIndent(closer):
    global indent
    global indentString
    indent += 1
    indentString = indentString[:len(indentString) - 1]
    printValue(closer)

def deincIndent():
    global indent
    global indentString
    indent += 1
    indentString = indentString[:len(indentString) - 1]

def op(operation, amount):
    addIndent("{")
    printField("op", str(operation))
    printField("amount", str(amount))
    removeIndent("}")

def loop(amount):
    addIndent("{")
    printField("op", "loop")
    printField("time", str(amount))
    removeIndent("}")

def compress(start, end):
    addIndent("{")
    printField("op", "compress")
    printField("start", str(start))
    printField("end", str(end))
    removeIndent("}")
    
def curve(interp):
    addIndent("{")
    printField("op", "curve")
    printField("interp", interp)
    removeIndent("}")

def clamp():
    addIndent("{")
    printField("op", "clamp")
    removeIndent("}")


def modMethod(offset, frames):
    op("add", str(-(offset + 1/frames)))
    loop(1)
    compress(1 - (1/frames) * 3, 1)
    curve("slope")
    op("mul", 2)
    clamp()
    curve("smooth2")
    curve("smooth2")

def modMethodFade(offset, frames):
    op("add", str(-(offset + 1/frames)))
    loop(1)
    compress(1 - (1/frames) * 3, 1)
    curve("slope")
    op("mul", 1.5)
    clamp()

def curveMethod(offset, frames):
    op("add", -offset - 1/(2 * frames))
    loop(1)
    op("mul", 2/(1/frames + 2*0.02))
    curve("pow10In")
    curve("pow10In")
    curve("reverse")
    clamp()

def makePart(index, frames, x, y, color, fadeColor):

    #amount of frames to skip
    global skip

    offset = index/frames

    global current

    incIndent()
    incIndent()
    incIndent()

    addIndent("{")
    printField("type", "RegionPart")
    printField("name", "fluid-gas-" + str(index * (skip + 1)))
    printField("x", x)
    printField("y", y)
    printField("outline", "false")
    printField("color", fadeColor)
    printField("colorTo", color)

    addIndent(r"progress: {")
    printField("type", "time")
    addIndent(r"ops: [")

    #Set the animation scale
    op("mul", str(1/190))

    modMethodFade(offset, frames)

    removeIndent("]")
    removeIndent("}")
    removeIndent("}")

    deincIndent()
    deincIndent()
    deincIndent()

skip = 4

def makeParts(amount):
    #Pixel offsets from the center of the unit
    baseX = 0
    baseY = 4/8
    current = ""
    for i in range(0, amount):
        makePart(i, amount -1, baseX, baseY -8, "cb8650aa", "cb865000")
    current = ""
    for y in range(0, 2):
        for i in range(0, amount):
            makePart(i, amount -1, baseX, baseY + y * 8, "cbdbfccc", "cbdbfc00")

makeParts(int(50/(skip+1)))

directory = r"C:\Users\Sh1p\AppData\Roaming\Mindustry\mods\meld\content\blocks\scripts"

with open(directory + r"\liquidanim-output.txt", "w") as file:
    file.write(current)