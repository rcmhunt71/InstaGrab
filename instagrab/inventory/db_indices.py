# TODO: Document class level
# TODO: Make this dynamic via yaml file or DB host


class DatabaseIndices:
    JETS = "Jets"
    MUSIC = "Music"
    NATURE = "Nature"
    PEOPLE = "People"
    UNKNOWN = "Unknown"
    SPECIAL = {
        JETS.lower(): JETS,
        MUSIC.lower(): MUSIC,
        NATURE.lower(): NATURE
    }
    DEFAULT = PEOPLE

    @classmethod
    def determine_index(cls, category: str) -> str:
        """
        Determine the database index to store record.

        Args:
            category: The category of image (determined from metadata)

        Return:
            Database index (str)
        """
        return cls.SPECIAL[category.lower()] if category.lower() in cls.SPECIAL.keys() else cls.PEOPLE
