class Article:
    def __init__(self, title, content, id=None):
        self.title = title
        self.content = content
        self.id = id

    def summary(self):
        return self.content[:100] + '...' if len(self.content) > 100 else self.content

    def __str__(self):
        return f"Title: '{self.title}' \nContent: '{self.content}'"
    
    def to_dict(self):
        """Convert the Article object to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }