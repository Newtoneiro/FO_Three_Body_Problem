"""
Constants defined for other files.
"""


class PYGAME_CONSTANTS:
    """
    Constants for pygame config.
    """

    WIDTH: int = 1000
    HEIGHT: int = 1000
    FPS: int = 120
    WINDOW_TITLE: str = "v-vectors"

    VECTOR_WIDTH: int = 2
    VECTOR_LENGTH_MULTI: int = 10


class COLORS:
    """
    Colors for pygame.
    """

    BLACK: tuple = 20, 52, 62
    WHITE: tuple = 249, 247, 243
    RED: tuple = 239, 71, 111
    YELLOW: tuple = 255, 209, 102
    GREEN: tuple = 6, 214, 160

    BACKGROUND_COLOR: tuple = BLACK
    VELOCITY_VECTORS_COLOR: tuple = WHITE
    BODY_COLOR_1: tuple = RED
    BODY_COLOR_2: tuple = YELLOW
    BODY_COLOR_3: tuple = GREEN


class PHYSICS_CONSTANTS:
    """
    Constants for physics.
    """

    # Constants for physics
    GRAVITATIONAL_CONSTANT: float = 0.1

    # Body constants
    MAX_BODY_RADIUS: int = 100
    MIN_BODY_RADIUS: int = 2
    DEFAULT_BODY_DENSITY: float = 1
    DEFAULT_BODY_MASS: int = 1000
    DEFAULT_BODY_DISTANCE: float = PYGAME_CONSTANTS.WIDTH / 5

    # Vector constants
    VELOCITY_LOSS_FACTOR: float = 0.9
    SPAWN_VECTOR_DIVIDER: int = 50
