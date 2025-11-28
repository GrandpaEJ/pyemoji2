"""
Advanced text classes for pyemoji2 with method chaining support.
"""


class Text:
    """Text with advanced styling support."""

    def __init__(self, text, font=None, size=24):
        if font is None:
            # Import here to avoid circular imports
            from .core import get_system_fonts

            font = get_system_fonts()[0]
        self.text = text
        self.font = font
        self.size = size
        self.color = "black"

        # Advanced properties
        self.outline_color = None
        self.outline_width = 0
        self.gradient_colors = None
        self.gradient_vertical = False
        self.shadow_offset = None
        self.shadow_color = None
        self.shadow_opacity = 0.5

    def with_color(self, color):
        """Set text color (chainable)."""
        self.color = color
        return self

    def with_outline(self, color, width=2):
        """Add outline (chainable)."""
        self.outline_color = color
        self.outline_width = width
        return self

    def with_gradient(self, color1, color2, vertical=False):
        """Add gradient (chainable)."""
        self.gradient_colors = (color1, color2)
        self.gradient_vertical = vertical
        return self

    def with_shadow(self, offset_x=2, offset_y=2, color="gray", opacity=0.5):
        """Add shadow (chainable)."""
        self.shadow_offset = (offset_x, offset_y)
        self.shadow_color = color
        self.shadow_opacity = opacity
        return self


class TextBox(Text):
    """Text with background box."""

    def __init__(self, text, font=None, size=24):
        super().__init__(text, font, size)
        self.background = None
        self.padding = 10
        self.border_color = None
        self.border_width = 0

    def with_background(self, color, padding=10):
        """Set background (chainable)."""
        self.background = color
        self.padding = padding
        return self

    def with_border(self, color, width=2):
        """Set border (chainable)."""
        self.border_color = color
        self.border_width = width
        return self
