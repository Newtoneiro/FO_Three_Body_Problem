"""An abstraction of canvas, on which the bodies interact with eachother."""

import pygame

from threeBodyProblem.objects.body import Body
from threeBodyProblem.constants import COLORS


class Canvas:
    """
    Abstraction representing the sky, on which the bodies interact.
    Responsible for updating the bodies' positions and displaying other
    features.
    """

    def __init__(self, win: pygame.Surface):
        self._win = win
        self._bodies = []
        self._show_vectors = False
        self._show_trails = True

    def toggle_vectors_display(self) -> None:
        """
        Switch between displaying bodies' vectors and not doing that.
        """
        self._show_vectors = not self._show_vectors

    def toggle_draw_trails(self) -> None:
        """
        Switch between drawing trails and not doing that.
        """
        self._show_trails = not self._show_trails

    def draw(self) -> None:
        """
        Draw the canvas.
        """
        self._win.fill(COLORS.BLACK)

        for body in self._bodies:
            body.draw(self._show_vectors, self._show_trails)

    def add_body(
        self,
        number: int,
        mass: float,
        init_x: int,
        init_y: int,
        init_vector: list[float],
        is_stationary: bool = False,
    ) -> None:
        """
        Initialize and add a body to the canvas.

        Args:
            win(pygame.Surface): the window on which the body is drawn
            mass(float): the mass of the body
            init_x(int): the initial x coordinate of the body
            init_y(int): the initial y coordinate of the body
            init_vector(list[float]): the initial velocity vector of the body
            is_stationary(bool): whether the body is stationary or not
        """
        self._bodies.append(
            Body(
                number, self._win, mass, init_x, init_y, init_vector,
                is_stationary
                )
        )

    def update(self) -> None:
        """
        Update the positions of the bodies and draw them.
        """
        for body1 in self._bodies:
            for body2 in self._bodies:
                if body1 == body2:
                    continue
                body1.calculate_impact_on(body2)

            body1.update()
