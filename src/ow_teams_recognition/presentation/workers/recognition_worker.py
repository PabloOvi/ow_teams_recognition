from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from ...application.recognition_service import (
	RecognitionService
)


class RecognitionWorker(QObject):

	finished = pyqtSignal(object)
	error = pyqtSignal(str)

	def __init__( self, recognition_service: RecognitionService ):

		super().__init__()

		self.recognition_service = ( recognition_service )


	@pyqtSlot()
	def run(self):

		try:

			match = ( self.recognition_service.recognize_match() )

			self.finished.emit( match )

		except Exception as exception:

			self.error.emit( str(exception) )