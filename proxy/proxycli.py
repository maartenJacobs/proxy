import proxy
import click


#
# proxy start [-p|--port]
# proxy restart [-p|--port]
# proxy stop
# proxy status
#


def start(context, port: int):
    click.echo('Starting on port %d' % port)
    try:
        proxy.run(port)
    except OSError as err:
        if err.errno == 98:
            print('Address or port are already in use')
            context.exit(1)
        else:
            raise


def stop():
    return


def restart(port):
    stop()
    start()


@click.command()
@click.argument('action')
@click.option('--port', default=8000,
              help='Port on which the proxy server will run. Default 8000.')
@click.pass_context
def cli(context, action, port):
    if action == 'start':
        start(context, port)
    elif action == 'stop':
        stop()
    else:
        click.echo('unknown action %s' % action)
