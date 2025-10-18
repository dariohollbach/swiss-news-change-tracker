class Article:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def summary(self):
        return self.content[:100] + '...' if len(self.content) > 100 else self.content

    def __str__(self):
        return f"Title: '{self.title}' \nContent: '{self.content}'"