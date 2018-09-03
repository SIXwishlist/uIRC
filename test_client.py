import client
import sys
import itertools

_TARGET = "#no_one_here"
_SERVER = "chat.freenode.net"
_PORT = 6667
_NICK = "uIRC_client"

def on_connect(connection, event):
    if client.is_channel(_TARGET):
        connection.join(_TARGET)
        print("Joined server %s on channel %s" % (_SERVER, _TARGET))
        return
    main_loop(connection)

def on_join(connection, event):
    main_loop(connection)

def on_disconnect(connection, event):
    raise SystemExit()

def get_lines():
    while True:
        yield sys.stdin.readline().strip()

def main_loop(connection):
    for line in itertools.takewhile(bool, get_lines()):
        print(line)
        connection.privmsg(_TARGET, line)
    connection.quit("Using uIRC/test_client.py")

def run():
    reactor = client.Reactor()

    try:
        conn = reactor.server().connect(_SERVER, _PORT, _NICK)
    except client.ServerConnectionError:
        print("Unable to connect!")
        print(sys.exc_info()[1])
        raise SystemExit(1)
    
    conn.add_global_handler("welcome", on_connect)
    conn.add_global_handler("join", on_join)
    conn.add_global_handler("disconnect", on_disconnect)

    reactor.process_forever()

if __name__ == "__main__":
    run()