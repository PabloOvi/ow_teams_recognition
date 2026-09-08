import easyocr


class EasyOCRReader:

	def __init__(self):

		self.reader = easyocr.Reader( ["en"], gpu=False, verbose=False )


	def read(self, image) -> str:

		results = self.reader.readtext( image )

		extracted_text = "\n".join(
			text
			for (
				bbox,
				text,
				probability
			) in results
		)

		return extracted_text.strip()
