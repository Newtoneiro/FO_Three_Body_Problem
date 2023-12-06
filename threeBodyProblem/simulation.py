import math
import pygame

from threeBodyProblem.simulation_params import SimulationParams
from threeBodyProblem.objects.canvas import Canvas
from threeBodyProblem.constants import PYGAME_CONSTANTS, COLORS, PHYSICS_CONSTANTS


class Simulation:
    """
    Class representing the simulation instance.
    """

    # ============== INITIALIZATION =============== #

    def __init__(
        self,
        win: pygame.Surface,
        clock: pygame.time.Clock,
        simulation_params: SimulationParams,
    ) -> None:
        self._win = win
        self._clock = clock
        self._params = simulation_params

        self._init_surface()
        self._init_canvas()

    def _init_surface(self) -> None:
        """
        Initializes pygame stuff.
        """
        self._surface = pygame.Surface(
            (PYGAME_CONSTANTS.WIDTH, PYGAME_CONSTANTS.HEIGHT),
            pygame.SRCALPHA,
        )
        self._surface.set_colorkey(COLORS.BACKGROUND_COLOR)
        self._surface.set_alpha(self._params.alpha)
        self._surface = self._surface.convert_alpha()

    def _init_canvas(self) -> None:
        """
        Initializes the canvas.
        """
        self._canvas = Canvas(self._surface)
        self._init_bodies()

    def _init_bodies(self) -> None:
        """
        Initializes the bodies positions as equilateral triangle
        on the canvas.
        """
        center_x = PYGAME_CONSTANTS.WIDTH / 2
        center_y = PYGAME_CONSTANTS.HEIGHT / 2
        height = (math.sqrt(3) / 2) * self._params.body_distance

        bodies_init_pos = [
            (center_x - self._params.body_distance / 2, center_y + height / 2),
            (center_x + self._params.body_distance / 2, center_y + height / 2),
            (center_x, center_y - height / 2),
        ]

        for i, (init_pos, next_init_pos) in enumerate(
            zip(bodies_init_pos, bodies_init_pos[1:] + bodies_init_pos[:1])
        ):
            vel_vector = [
                (next_init_pos[0] - init_pos[0])
                * PHYSICS_CONSTANTS.DEFAULT_BODY_VELOCITY_FACTOR,
                (next_init_pos[1] - init_pos[1])
                * PHYSICS_CONSTANTS.DEFAULT_BODY_VELOCITY_FACTOR,
            ]
            self._canvas.add_body(
                number=i + 1,
                mass=self._params.mass,
                init_x=int(init_pos[0]),
                init_y=int(init_pos[1]),
                init_vector=vel_vector,
                is_stationary=False,
                g_constant=self._params.g_constant,
            )

    # ================= PRIVATE METHODS =================== #

    def _draw(self) -> None:
        """
        Draws all bodies on the canvas.
        """
        self._canvas.draw()
        self._win.blit(self._surface, (0, 0))

    # ================== PUBLIC METHODS ================== #

    def toggle_show_vectors(self) -> None:
        """
        Switch between displaying bodies' vectors and not doing that.
        """
        self._canvas.toggle_draw_vectors()

    def toggle_draw_trails(self) -> None:
        """
        Switch between drawing trails and not doing that.
        """
        self._canvas.toggle_draw_trails()

    def toggle_show_graph(self) -> None:
        """
        Switch between plotting the graph and not doing that.
        """
        self._canvas.toggle_plot_graph()

    def reset(self) -> None:
        """
        Reset the canvas.
        """
        self._canvas.reset()
        self._init_bodies()

    def run(self) -> None:
        """
        Runs the simulation.
        """
        self._canvas.update()
        self._draw()
