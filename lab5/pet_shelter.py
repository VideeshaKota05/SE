
"""Manage an animal shelter's pet registration and adoption records."""

import secrets
import sqlite3


ADOPTION_CODE_MIN = 1000
ADOPTION_CODE_RANGE = 9000


class PetShelter:
    """Manage pet registration and adoption records."""

    def __init__(self):
        """Initialize the in-memory pet database."""
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute(
            """
            CREATE TABLE pets (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                species TEXT NOT NULL,
                age INTEGER NOT NULL,
                adopted INTEGER NOT NULL DEFAULT 0
            )
            """
        )

    def register_pet(
        self,
        name: str,
        species: str,
        age: int,
        tags: list[str] | None = None,
    ) -> list[str]:
        """Register a pet and return its tags."""
        if tags is None:
            tags = []

        self.connection.execute(
            """
            INSERT INTO pets (name, species, age, adopted)
            VALUES (?, ?, ?, 0)
            """,
            (name, species, age),
        )

        tags.append(species)
        return tags

    def adopt(self, pet_id: int) -> None:
        """Mark a pet as adopted."""
        self.connection.execute(
            "UPDATE pets SET adopted = 1 WHERE id = ?",
            (pet_id,),
        )

    def adoption_code(self) -> str:
        """Generate a secure four-digit adoption code."""
        code = secrets.randbelow(ADOPTION_CODE_RANGE)
        return f"PET-{code + ADOPTION_CODE_MIN}"

    def oldest_available(self) -> str | None:
        """Return the name of the oldest available pet."""
        row = self.connection.execute(
            """
            SELECT name
            FROM pets
            WHERE adopted = 0
            ORDER BY age DESC
            LIMIT 1
            """
        ).fetchone()

        if row is None:
            return None

        return row[0]

    def clear_unadopted(self) -> None:
        """Delete all pets that have not been adopted."""
        self.connection.execute(
            "DELETE FROM pets WHERE adopted = 0"
        )

    def shelter_status(self) -> str:
        """Return the current shelter status."""
        row = self.connection.execute(
            "SELECT COUNT(*) FROM pets WHERE adopted = 1"
        ).fetchone()

        if row[0] > 0:
            return "active"

        return "quiet"

    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()


def main() -> None:
    """Run the animal shelter demonstration."""
    shelter = PetShelter()

    try:
        shelter.register_pet("Bruno", "dog", 7)
        shelter.register_pet("Mitzi", "cat", 3)
        shelter.register_pet("Kiwi", "parrot", 12)

        shelter.adopt(1)

        print(
            shelter.oldest_available(),
            shelter.adoption_code(),
            shelter.shelter_status(),
        )

        shelter.clear_unadopted()

    finally:
        shelter.close()


if __name__ == "__main__":
    main()
