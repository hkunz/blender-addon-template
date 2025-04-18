class NumberUtils:

    @staticmethod
    def is_almost_equal(float1, float2, tolerance=0.0001):
        return abs(float1 - float2) < tolerance

    @staticmethod
    def format_decimal_2(float):
        return '{:.2f}'.format(float)