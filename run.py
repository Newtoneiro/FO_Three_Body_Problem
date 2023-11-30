"""Main file presenting the whole program in action."""

import math
import pygame

from threeBodyProblem.objects.canvas import Canvas
from threeBodyProblem.constants import PYGAME_CONSTANTS, COLORS, \
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
        self._init_pygame()
        self._init_enviroment()
        self._init_canvas(bodies_distance)

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
        self._selected_mass = PHYSICS_CONSTANTS.DEFAULT_BODY_MASS
        self._run = True

    def _init_canvas(self, body_distance: int) -> None:
        """
        Initializes the canvas.
        """
        self._canvas = Canvas(self._win)
        self._init_bodies(body_distance)

    def _init_bodies(self, body_distance: int) -> None:
        """
        Initializes the bodies positions as equilateral triangle
        on the canvas.
        """
        center_x = PYGAME_CONSTANTS.WIDTH / 2
        center_y = PYGAME_CONSTANTS.HEIGHT / 2
        height = (math.sqrt(3) / 2) * body_distance

        bodies_init_pos = [
            (center_x - body_distance / 2, center_y + height / 2),
            (center_x + body_distance / 2, center_y + height / 2),
            (center_x, center_y - height / 2)
            ]

        for i, init_pos in enumerate(bodies_init_pos):
            self._canvas.add_body(
                number=i + 1,
                mass=PHYSICS_CONSTANTS.DEFAULT_BODY_MASS,
                init_x=init_pos[0],
                init_y=init_pos[1],
                init_vector=[0, 0],
                is_stationary=False,
            )

    # =============================================== #

    def run(self) -> None:
        """
        Runs the simulation.
        """
        self._init_event_callbacks()
        while self._run:
            self._win.fill(COLORS.BLACK)
            self._clock.tick(PYGAME_CONSTANTS.FPS)
            self._canvas.update()

            self._draw_bodies()
            self._handle_events()

            pygame.display.flip()

    def _draw_bodies(self) -> None:
        """
        Draws all bodies on the canvas.
        """
        for body in self._canvas._bodies:
            body.draw(self._canvas._show_vectors)

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
            pygame.K_c: self._handle_clear,
            pygame.K_v: self._handle_show_vectors,
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

    def _handle_clear(self) -> None:
        """
        Handles clear event.
        """
        self._canvas.clear()

    def _handle_show_vectors(self) -> None:
        """
        Handles show vectors event.
        """
        self._canvas.toggle_vectors_display()

    def _handle_add_particles(self) -> None:
        """
        Handles add particles event.
        """
        x, y = pygame.mouse.get_pos()
        for i in range(PHYSICS_CONSTANTS.PARTICLES_PER_CLICK):
            self._canvas.add_body(
                mass=1,
                init_x=x,
                init_y=y + i,
                init_vector=[1, 1],
                is_stationary=False,
                is_particle=True,
            )

    def _handle_mass_change(self, mass: int) -> None:
        """
        Handles mass change event.
        """
        self._selected_mass = mass


if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
