from lingowords import words

def kies_woord():
    import random
    return random.choice(words)

def woord_splitter(woord):
    return list(woord)
