from core.base import Base
from core.openGLUtils import OpenGLUtils
class Test(Base):

    def initialize(self):
        print("Initializing program...")
        OpenGLUtils.printSystemInfo()

    def update(self):
        pass

Test().run()