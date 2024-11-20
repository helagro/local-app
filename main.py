import subprocess


def is_away():
    result = subprocess.run(
        ["zsh", "-i", "-c", "source ~/.zshrc && tl is/away | st cnt"],
        capture_output=True,
        text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return Code:", result.returncode)


def a(content: str):
    result = subprocess.run(["zsh", "-c", f"source ~/.zshrc && a {content}"],
                            capture_output=True,
                            text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return Code:", result.returncode)


def get_routine():
    pass


# a("Hello, World!")
# away()
