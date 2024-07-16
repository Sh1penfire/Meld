baseIndent = 1


def indent(amount):
    for i in range(amount):
        print("\t", end="")

def printIndented(string, amount):
    for i in range(amount):
        string = "\t" + string
    print(string)

def weapon(){
    indent = baseIndent
    printIndented("{")
    indent += 1

    printIndented("x: 0", indent);
    printIndented("y: 0", indent);
    printIndented("mirror: false", indent);

    indent -= 1
    printIndented("{")
        
}


for i in range(100){
    weapon()
}
