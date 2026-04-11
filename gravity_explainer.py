"""Simple script to explain gravity in plain language.

Run:
    python gravity_explainer.py
"""


def explain_gravity() -> str:
    """Return a beginner-friendly explanation of gravity."""
    return (
        "Gravity is a force of attraction between objects that have mass.\n"
        "The more mass an object has, the stronger its gravity.\n\n"
        "On Earth, gravity pulls everything toward the planet's center. "
        "That is why things fall down instead of floating away.\n\n"
        "Isaac Newton described gravity as a force, and Albert Einstein later "
        "explained it as the bending of space-time by massive objects.\n"
        "In both views, gravity keeps planets in orbit and helps hold galaxies together."
    )


if __name__ == "__main__":
    print(explain_gravity())
