class Article():

    """Article object representation"""

    def __init__(self):
        self.id = -1
        self.title = 'Template Article'
        self.authors = 'Invalid'
        self.abstract = 'Invalid'
        self.fields = set()
        self.entries = [('template_link', 'template_journal')]
        self.journals = []
