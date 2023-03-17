from src.projection_entities.people.person import Person


class PolicyHolder(
    Person
):

    def __init__(
        self,
        policyholder_data_source
    ):

        self.issue_age: int =