class Entry():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, concept, entry, date, mood_id):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.date = date
        self.mood_id = mood_id