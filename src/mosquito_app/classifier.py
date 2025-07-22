class AIClassifier(object):
    """
    Classifier class for handling mosquito identification tasks.
    """

    def classify(self,**params) -> str:
        return NotImplementedError("This method should be overridden by subclasses.")