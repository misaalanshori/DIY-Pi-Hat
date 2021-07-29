from config import dispWidth, dispHeight

# Create a centered text based on the text pixel length
def centerText(canvas, y, text, fill, font):
    w, h = canvas.textsize(text, font)
    offset = (dispWidth - w)/2
    canvas.text((offset, y), text, fill, font)


# This is a stupid function to offset xy positions, it doesnt make sense. its a way for me to solve a problem that i just can't figure out the reason and solution for
def posOffset(x,y,ox=0,oy=0,oox=0,ooy=-3):
    return (x+oox+ox, y+ooy+oy)


# shallow copy Arrays and Dicts, kinda useless because python already has this
def shallowCopyArray(arr):
    newArr = []
    for i in arr:
        newArr.append(i)
    return newArr

def shallowCopyDict(dicti):
    newDict = {}
    for i in dicti:
        newDict[i] = dicti[i]
    return newDict

# Honestly this is my best attempt at a deepCopy function
# Its recursive and in theory works with sets, lists, and dicts
# at least it works. The python Copy Module uses pickling and just breaks everything
# So i had to make one myself
def badDeepCopy(input):
    if hasattr(input, "__iter__"):
        # print(type(input))
        temp = type(input)()

        if type(input) == set:
            adder = temp.add
        elif type(input) == list:
            adder = temp.append
        elif type(input) == str:
            return input
        for obj in input:
            if type(input) != dict:
                adder(badDeepCopy(obj))
            elif type(input) == dict:
                temp[obj] = badDeepCopy(input[obj])
                
        return temp
    else:
        return input
            

