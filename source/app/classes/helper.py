class Helper:
    def __init__(self):
        pass
    
    def random_sentence(self, filename: str):
        file = open(filename).read()
        sentences = file.split('\n')
        receive_sentence = random.choice(sentences)
        
        return sentences