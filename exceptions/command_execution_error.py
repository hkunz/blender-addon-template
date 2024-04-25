class CommandExecutionError(Exception):
    def __init__(self, returncode: int, stdout: str, stderr: str) -> None:
        self.returncode: int = returncode
        self.stdout: str = stdout
        self.stderr: str = stderr
        super().__init__(f"Error: Command exited with return code {returncode}")