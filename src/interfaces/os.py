import subprocess


def shutdown():
    try:
        result = subprocess.run(
            ['zsh', '-c', f'shutdown -h now >&2'],
            stdin=subprocess.DEVNULL,
            timeout=5,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stderr.strip()
    except Exception as e:
        print(f"Error executing command 'shutdown -h now': {e}")
