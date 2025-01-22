

class Util:

    @staticmethod
    def intToRgb(id):
        return(
            (id & 0x000000FF) >>  0,
            (id & 0x0000FF00) >>  8,
            (id & 0x00FF0000) >> 16
        )

    @staticmethod
    def rgbToInt(rgb):
        r, g, b = rgb 
        return(r + g * 256 + b * 256**2)
    
    @staticmethod
    def toClipCoordinates(x, y, width, height):
        
        x1 = (2 * x) / width - 1 
        y1 = 1 - (2 * y) / height 

        return x1, y1