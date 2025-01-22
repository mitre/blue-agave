from invoke import task

SOURCE_DIR = "source/"
BUILD_DIR = "build/"


@task
def docs_ci(c):
    cmd = "sphinx-build -M dirhtml '{SOURCE_DIR}' '{BUILD_DIR}' -W --keep-going"
    c.run(cmd.format(SOURCE_DIR=SOURCE_DIR, BUILD_DIR=BUILD_DIR))


@task
def docs_html(c):
    cmd = "sphinx-build -M html '{SOURCE_DIR}' '{BUILD_DIR}'"
    c.run(cmd.format(SOURCE_DIR=SOURCE_DIR, BUILD_DIR=BUILD_DIR))


@task
def docs_server(c):
    cmd = "sphinx-autobuild -b dirhtml -a '{SOURCE_DIR}' '{BUILD_DIR}'"
    c.run(cmd.format(SOURCE_DIR=SOURCE_DIR, BUILD_DIR=BUILD_DIR))
