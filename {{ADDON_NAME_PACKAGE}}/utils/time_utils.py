class TimeUtils:
    @staticmethod
    def format_duration(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        result = []
        if hours:
            result.append(f"{int(hours)} hours")
        if minutes:
            result.append(f"{int(minutes)} minutes")
        if seconds:
            result.append(f"{int(seconds)} seconds")

        return ' '.join(result)