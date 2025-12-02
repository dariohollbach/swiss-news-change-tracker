class NewsPaper:
    def __init__(self, title, id=None):
        self.title = title
        self.id = id

    def summary(self):
        return self.title[:100] + '...' if len(self.title) > 100 else self.title

    def __str__(self):
        return f"Title: '{self.title}'"
    
    def to_dict(self):
        """Convert the NewsPaper object to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title
        }