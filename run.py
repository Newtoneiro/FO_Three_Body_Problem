"""Main file presenting the whole program in action."""

import math
import pygame

from threeBodyProblem.objects.canvas import Canvas
from threeBodyProblem.constants import PYGAME_CONSTANTS, \
                                       PHYSICS_CONSTANTS


class Simulation:
    """
    Class representing the whole simulation.
    """

    # ============== INITIALIZATION =============== #

    def __init__(
            self,
            bodies_distance: float = PHYSICS_CONSTANTS.DEFAULT_BODY_DISTANCE
            ) -> None:
        self._init_bodies_distance = bodies_distance
        self._init_pygame()
        self._init_enviroment()
        self._init_canvas()

    def _init_pygame(self) -> None:
        """
        Initializes pygame.
        """
        pygame.init()
        pygame.display.set_caption(PYGAME_CONSTANTS.WINDOW_TITLE)
        self._win = pygame.display.set_mode(
            (PYGAME_CONSTANTS.WIDTH, PYGAME_CONSTANTS.HEIGHT)
        )
        self._clock = pygame.time.Clock()

    def _init_enviroment(self) -> None:
        """
        Initializes the enviroment.
        """
        self._last_pos_clicked = [0, 0]
        self._run = True

    def _init_canvas(self) -> None:
        """
        Initializes the canvas.
        """
        self._canvas = Canvas(self._win)
        self._init_bodies()

    def _init_bodies(self) -> None:
        """
        Initializes the bodies positions as equilateral triangle
        on the canvas.
        """
        center_x = PYGAME_CONSTANTS.WIDTH / 2
        center_y = PYGAME_CONSTANTS.HEIGHT / 2
        height = (math.sqrt(3) / 2) * self._init_bodies_distance

        bodies_init_pos = [
            (center_x - self._init_bodies_distance / 2, center_y + height / 2),
            (center_x + self._init_bodies_distance / 2, center_y + height / 2),
            (center_x, center_y - height / 2)
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
                mass=PHYSICS_CONSTANTS.DEFAULT_BODY_MASS,
                init_x=init_pos[0],
                init_y=init_pos[1],
                init_vector=vel_vector,
                is_stationary=False,
            )

    # =============================================== #

    def _draw(self) -> None:
        """
        Draws all bodies on the canvas.
        """
        self._canvas.draw()

    def _handle_events(self) -> None:
        """
        Handles all events.
        """
        for event in pygame.event.get():
            self._event_callbacks.get(event.type, lambda _: None)(event)

    def _init_event_callbacks(self) -> None:
        """
        Initializes pygame callbacks.
        """
        self._event_callbacks = {
            pygame.QUIT: lambda event: self._handle_stop(event),
            pygame.KEYDOWN: lambda event: self._handle_key_down(event),
        }

        self._key_callbacks = {
            pygame.K_v: self._handle_show_vectors,
            pygame.K_t: self._handle_switch_draw_trails,
            pygame.K_g: self._handle_switch_plot_graph,
            pygame.K_r: self._handle_reset,
        }

    # ================== EVENT HANDLERS ================== #

    def _handle_stop(self, event: pygame.event.Event) -> None:
        """
        Stops the simulation.
        """
        self._run = False

    def _handle_key_down(self, event: pygame.event.Event) -> None:
        """
        Handles key down event.
        """
        self._key_callbacks.get(event.key, lambda: None)()

    # ================== KEY CALLBACKS ================== #

    def _handle_show_vectors(self) -> None:
        """
        Handles show vectors event.
        """
        self._canvas.toggle_vectors_display()

    def _handle_switch_draw_trails(self) -> None:
        """
        Handles switch draw trails event.
        """
        self._canvas.toggle_draw_trails()

    def _handle_switch_plot_graph(self) -> None:
        """
        Handles switch plot graph event.
        """
        self._canvas.toggle_plot_graph()

    def _handle_reset(self) -> None:
        """
        Handles reset event.
        """
        self._canvas.reset()
        self._init_bodies()

    # ================== PUBLIC METHODS ================== #

    def run(self) -> None:
        """
        Runs the simulation.
        """
        self._init_event_callbacks()
        while self._run:
            self._clock.tick(PYGAME_CONSTANTS.FPS)
            self._canvas.update()

            self._draw()
            self._handle_events()

            pygame.display.flip()


if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
