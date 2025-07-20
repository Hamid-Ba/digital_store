from store import models


class CategoryServices:
    """Category Services"""

    def __init__(self) -> None:
        cats = models.Category.objects.all()

    def get_parent_cats(self):
        return models.Category.objects.get_parents_category()
