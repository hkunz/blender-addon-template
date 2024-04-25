class ColorUtils:
    @staticmethod
    # FIXME: when exporting white color it turns pinkish
    def linear_to_srgb(color_value: float) -> float:
        if color_value <= 0.0031308:
            return 12.92 * color_value
        else:
            return 1.055 * color_value ** (1 / 2.4) - 0.055
