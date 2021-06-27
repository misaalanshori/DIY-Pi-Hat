from config import dispWidth, dispHeight

def centerText(canvas, y, text, fill, font):
	w, h = canvas.textsize(text, font)
	offset = (dispWidth - w)/2
	canvas.text((offset, y), text, fill, font)

def posOffset(x,y,ox=0,oy=0,oox=0,ooy=-3):
	return (x+oox+ox, y+ooy+oy)
