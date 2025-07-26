from invoke import task


@task
def test(c):
    """Run tests"""
    c.run("pytest")


@task
def lint(c):
    """Run linting"""
    c.run("pylint src/")
    c.run("black --check src/")


@task
def coverage(c):
    c.run("coverage run --branch -m pytest; coverage html", pty=True)


@task
def autopep(c):
    c.run("autopep8 --in-place --aggressive --recursive .", pty=True)


@task
def play(c):
    """Run the play_game.py file"""
    c.run(f"python src/play_game.py")


@task
def run(c, file):
    """Run a specific Python file"""
    c.run(f"python src/{file}")
