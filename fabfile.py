import sys

from fabric.colors import red, green
from fabric.decorators import task
from fabric.operations import local


def title(s):
    print(green(s, bold=True))
    sys.stdout.flush()

def info(s):
    print(green(s, bold=False))
    sys.stdout.flush()


def error(s):
    print(red(s, bold=True))
    sys.stdout.flush()


def warning(s):
    print(red(s, bold=False))
    sys.stdout.flush()


@task
def clean():
    title("Cleaning Environments..")
    local("docker-compose down")
    local("docker-compose rm -f")
    clean_dangling()
    title("Clean complete")


@task
def test():
    title("Running tests..")
    local("docker-compose exec website snakeeyes test")
    title("Done.")


@task
def build():
    title("Building artifacts for release..")
    local("docker-compose build")
    title("Build complete.")

@task
def deploy():
    title("Deploying application..")
    local("docker-compose up -d")
    title("Done.")


@task
def import_data():
    title("Adding initializing DB with data..")
    local("docker-compose exec api python cli.py import_data")
    title("Done.")

@task
def init_redis():
    title("Initializing redis..")
    local("docker-compose exec api python cli.py init_redis")
    title("Done.")

@task
def analyse_watchlist():
    title("Adding initializing DB with data..")
    local("docker-compose exec api python cli.py watchlist")
    title("Done.")

@task
def analyse_portfolio():
    title("Adding initializing DB with data..")
    local("docker-compose exec api python cli.py portfolio")
    title("Done.")

@task
def clean_deploy():
    title("Cleaning and deploying application..")
    clean()
    build()
    deploy()
    title("Done.")


def clean_dangling():
    try:
        local('docker rmi $(docker images --filter "dangling=true" -q --no-trunc)')
    except:
        'Error while cleaning dangling images'


def get_container_id(service="website"):
    c = local('docker-compose ps -q {}'.format(service), capture=True)
    ret = ''
    if c.stdout:
        ret = c.stdout.strip()
        print("{} ID: {}".format(service, ret))
    else:
        warning("No service {} found.".format(service))
    return ret
