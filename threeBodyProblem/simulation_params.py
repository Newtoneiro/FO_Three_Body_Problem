from dataclasses import dataclass

from threeBodyProblem.constants import PHYSICS_CONSTANTS


@dataclass
class SimulationParams:
    alpha: int = 255
    body_distance: float = PHYSICS_CONSTANTS.DEFAULT_BODY_DISTANCE
    mass: float = PHYSICS_CONSTANTS.DEFAULT_BODY_MASS
    g_constant: float = PHYSICS_CONSTANTS.GRAVITATIONAL_CONSTANT
