# run runs a command on a remote server
# local runs a local command
# put uploads a local file to the remote server
# cd changes the directory on the server side
# get downloads a file from the remote server
# prompt prompts a user with text and returns the user input
from fabric.api import local, settings, abort
from fabric.contrib.console import confirm


def test():
    with settings(warn_only=True):
        result = local("nosetests -v", capture=True)
    if result.failed and not confirm("Test failed. Continue?"):
        abort("Aborted at user request")


def commit():
    message = input("Enter a git commit message")
    local("git add . && git commit -am '{}'".format(message))


def push():
    local("git push -u origin master")


def prepare():
    test()
    commit()
    push()
