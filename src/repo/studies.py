from entity.studies import Studies as StudiesEntity

class Studies:
    def __init__(self, db_name: str):
        self.db_name:str = db_name

    def save(self, studies:StudiesEntity) -> None:
        pass