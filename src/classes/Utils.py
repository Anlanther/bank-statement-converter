

class Utils:
    @staticmethod
    def is_float(str_float):
        try:
            float(str_float)
            if str_float[-3] == ".":
                return True
            else:
                return False
        except ValueError:
            return False