import cv2
import numpy as np

from PIL import ImageGrab

class ScreenCapture:

	def capture(self):

		screenshot = ImageGrab.grab()

		frame = cv2.cvtColor( np.array(screenshot), cv2.COLOR_RGB2BGR )

		return frame