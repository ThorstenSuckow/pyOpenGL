

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
    
    @staticmethod
    def center(list):
        minx = 1
        miny = 1
        maxy = -1
        maxx = -1
        for i in range(0, len(list)):
            minx = min(minx, list[i][0])
            maxx = max(maxx, list[i][0])
            miny = min(miny, list[i][1])
            maxy = max(maxy, list[i][1])
            
        return minx + (maxx - minx) / 2, miny + (maxy - miny) / 2    