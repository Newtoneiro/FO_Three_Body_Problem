"""An abstraction of body on which the calculations are made."""


from __future__ import annotations
from collections import deque

import pygame
import math

from threeBodyProblem.constants import PYGAME_CONSTANTS, COLORS, PHYSICS_CONSTANTS


class Body:
    """
    Abstraction representing a body.
    Responsible for calculating the gravitational force exerted on it by other
    bodies, and for drawing itself.
    """

    def __init__(
        self,
        number: int,
        win: pygame.Surface,
        mass: float,
        init_x: int,
        init_y: int,
        init_vector: list[float] = [0, 0],
        is_stationary: bool = False,
        g_constant: float = PHYSICS_CONSTANTS.GRAVITATIONAL_CONSTANT,
        density: float = PHYSICS_CONSTANTS.DEFAULT_BODY_DENSITY,
    ):
        self._number = number
        self._color = getattr(COLORS, f"BODY_COLOR_{self._number}")
        self._win = win
        self._mass = mass
        self._x = init_x
        self._y = init_y
        self._vector = init_vector
        self._is_stationary = is_stationary
        self._g_constant = g_constant
        self._density = density

        self._init_last_positions()
        self._calculate_radius()

    # ============== PRIVATE METHODS ============== #

    def _init_last_positions(self) -> None:
        """
        Initialize the body's last positions list.
        """
        self._pos_history = deque(maxlen=PYGAME_CONSTANTS.BODY_TRAIL_LENGTH)

    def _calculate_radius(self) -> None:
        """
        Calculate the body's radius from it's mass and density,
        using the formula:
            V = m/d = 4/3(pi)(r^3). => r = (3 * m / 4 * pi * d) ** (1/3).

        If the body's radius exceeds the set boundaries, it get's reduced.
        """
        self._radius = (3 / 4 * math.pi) * (self._mass / self._density) ** (1 / 3)
        if self._radius > PHYSICS_CONSTANTS.MAX_BODY_RADIUS:
            self._radius = PHYSICS_CONSTANTS.MAX_BODY_RADIUS
        elif self._radius < PHYSICS_CONSTANTS.MIN_BODY_RADIUS:
            self._radius = PHYSICS_CONSTANTS.MIN_BODY_RADIUS

    def _check_and_update_boundary(
        self, axis: float, limit: float, radius: float, vector_index: int
    ) -> float:
        """
        Checks if the body is within the boundaries of the simulation space.
        If the body is outside the boundaries, it is bounced back with
        reduced velocity.

        Args:
            axis (float): The current position of the body on the given axis.
            limit (float): The maximum position of the body on the given axis.
            radius (float): The radius of the body.
            vector_index (int): The index of the vector component that
            corresponds to the given axis.

        Returns:
            int: The updated position of the body on the given axis.
        """
        if axis < radius:
            axis = 1 + radius
            self._vector[vector_index] = (
                -PHYSICS_CONSTANTS.VELOCITY_LOSS_FACTOR * self._vector[vector_index]
            )
        elif axis > limit - radius:
            axis = limit - radius
            self._vector[vector_index] = (
                -PHYSICS_CONSTANTS.VELOCITY_LOSS_FACTOR * self._vector[vector_index]
            )

        return axis

    def _update_pos_history(self) -> None:
        """
        Update the body's last positions list.
        """
        self._pos_history.append((self._x, self._y))

    def _draw_velocity_vector(self) -> None:
        """
        Draw the body's velocity vector on the canvas.
        """
        pygame.draw.line(
            surface=self._win,
            color=COLORS.VELOCITY_VECTORS_COLOR,
            start_pos=(self._x, self._y),
            end_pos=(
                self._x + PYGAME_CONSTANTS.VECTOR_LENGTH_MULTI * self._vector[0],
                self._y + PYGAME_CONSTANTS.VECTOR_LENGTH_MULTI * self._vector[1],
            ),
            width=PYGAME_CONSTANTS.VECTOR_WIDTH,
        )

    def _update_trail_variables(
        self, segment: int, opacity: float
    ) -> tuple[tuple, float]:
        """
        Return the color of the trail segment.

        Args:
            segment(int): the index of the segment
            opacity(float): the current opacity of the segment

        Returns:
            tuple: the color of the segment
            float: the opacity of the segment
        """
        dropoff_treshold = (
            len(self._pos_history) * PYGAME_CONSTANTS.BODY_TRAIL_DROPOFF_TRESHOLD
        )

        if segment < dropoff_treshold:
            ret_color = self.change_color_opacity(
                self._color, COLORS.BACKGROUND_COLOR, opacity
            )
            opacity += 1 / dropoff_treshold
        else:
            ret_color = self._color
        return ret_color, opacity

    def _draw_trails(self) -> None:
        """
        Draw the body's trails on the canvas.
        """
        opacity = 0.0  # starting from the end
        for i in range(len(self._pos_history) - 1):
            color, opacity = self._update_trail_variables(i, opacity)
            pygame.draw.line(
                surface=self._win,
                color=color,
                start_pos=self._pos_history[i],
                end_pos=self._pos_history[i + 1],
                width=PYGAME_CONSTANTS.TRAIL_WIDTH,
            )

    # ============== STATIC METHODS =============== #

    @staticmethod
    def change_color_opacity(color1: tuple, color2: tuple, opacity: float) -> tuple:
        """
        Change the opacity of color1 to opacity, and return the result.

        Args:
            color1(tuple): the color to change the opacity of
            color2(tuple): the relative color to change the opacity
                           in regards to
            opacity(float): the opacity

        Returns:
            tuple: the color with the changed opacity
        """
        return tuple(
            [opacity * c1 + (1 - opacity) * c2 for c1, c2 in zip(color1, color2)]
        )

    @staticmethod
    def cast_to_plot_coordinates(coordinates: tuple[int, int]) -> tuple[int, int]:
        """
        Cast the coordinates to the coordinates on the graph.

        Args:
            coordinates(tuple[int, int]): the coordinates to cast

        Returns:
            tuple[int, int]: the casted coordinates
        """
        return (
            coordinates[0] * PYGAME_CONSTANTS.GRAPH_WIDTH // PYGAME_CONSTANTS.WIDTH,
            coordinates[1] * PYGAME_CONSTANTS.GRAPH_HEIGHT // PYGAME_CONSTANTS.HEIGHT,
        )

    # ============== PUBLIC METHODS =============== #

    def calculate_impact_on(self, other: Body) -> None:
        """
        Calculate the gravitational force between self and other body,
        and update the vector accordingly.

        Args:
            other(body): other body, relative to which we calculate the
                         gravitational force.
        """
        if self._is_stationary or self == other:
            # Stationary bodys don't exert force on other bodys
            return

        d = math.sqrt((self._x - other._x) ** 2 + (self._y - other._y) ** 2)
        if d <= self._radius + other._radius:
            # So the forces won't get extreme, when the bodys get close
            return

        dx = self._x - other._x
        dy = self._y - other._y
        gravitational_force = (  # From the formula F = G * M * m / d^2
            self._g_constant * self._mass * other._mass
        ) / d**2
        Fx = gravitational_force * dx / d
        Fy = gravitational_force * dy / d

        # Update according to x acceleration
        self._vector[0] += -Fx / self._mass
        # Update according to y acceleration
        self._vector[1] += -Fy / self._mass

    def update(self) -> None:
        """
        Update the position of the body, and check for collisions with the
        boundaries.
        """
        self._x += self._vector[0]
        self._y += self._vector[1]

        self._update_pos_history()

        self._x = self._check_and_update_boundary(
            self._x, PYGAME_CONSTANTS.WIDTH, self._radius, 0
        )
        self._y = self._check_and_update_boundary(
            self._y, PYGAME_CONSTANTS.HEIGHT, self._radius, 1
        )

    def draw(
        self, show_velocity_vectors: bool = False, show_trails: bool = False
    ) -> None:
        """
        Draw the body on the canvas. If show_velocity_vectors is True,
        also draw the velocity vector of the body. If show_trails is True,
        also draw the trails of the body.
        """
        if show_trails:
            self._draw_trails()
        pygame.draw.circle(
            surface=self._win,
            color=self._color,
            center=(self._x, self._y),
            radius=self._radius,
        )
        if show_velocity_vectors:
            self._draw_velocity_vector()

    def plot_on_graph(self, plot_win: pygame.Surface) -> None:
        """
        Plot the body on the graph.
        """
        for i in range(len(self._pos_history) - 1):
            pygame.draw.line(
                surface=plot_win,
                color=self._color,
                start_pos=self.cast_to_plot_coordinates(self._pos_history[i]),
                end_pos=self.cast_to_plot_coordinates(self._pos_history[i + 1]),
                width=PYGAME_CONSTANTS.GRAPH_THICKNESS,
            )
