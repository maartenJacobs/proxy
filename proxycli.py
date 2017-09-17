import proxy
import click


#
# proxy start [-p|--port]
# proxy restart [-p|--port]
# proxy stop
# proxy status
#


def start(port):
    proxy.run(port)


def stop():
    return


def restart(port):
    stop()
    start()


@click.command()
@click.argument('action')
@click.option('--port', default=8000,
              help='Port on which the proxy server will run. Default 8000.')
def cli(action, port):
    if action == 'start':
        start(port)
    elif action == 'stop':
        stop()
    else:
        click.echo('unknown action %s' % action)
