

class Util:

    @staticmethod
    def getCurrentSpeed(acceleration, startVelocity, currentTime, timeStart):
        
        delta = currentTime - timeStart 
        delta = delta / 1_000_000_000 

        return  startVelocity + acceleration * (delta)
        
        pass