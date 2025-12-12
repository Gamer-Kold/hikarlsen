import chess

import sys
import threading
import time
import engine

ENGINE_NAME = "Hikarlsen"
ENGINE_AUTHOR = "Qamar et. al."

# a thread-safe event to signal the search thread to stop
stop_searching_event = threading.Event()
# a reference to the active search thread
search_thread = None
# a reference to the engine
engine = Engine()

# --- UCI Command Handlers (The main engine logic) ---

def handle_uci():
    print(f"id name {ENGINE_NAME}")
    print(f"id author {ENGINE_AUTHOR}")
    
    print("uciok")
    sys.stdout.flush()

def handle_position(command_parts):
    # first 6 parts are the fen position
    # we skip the redundant "moves" and then
    # send the rest of the list as a list of moves
    engine.position(command_parts[:6], command_parts[7:])
    print("info string Position set.")
    sys.stdout.flush()

def _search_worker(go_command_args):
    # for future reference when search gets implemented 
    # print(f"info depth {depth} score cp {score} nodes {nodes} time {depth*500} pv {pv}")
    print(f"bestmove {best_move_so_far}")
    sys.stdout.flush()
    print("info string Search finished.")
    sys.stdout.flush()


def handle_go(command_parts):
    global search_thread, stop_searching_event

    # if a search is already running, stop it first
    if search_thread and search_thread.is_alive():
        handle_stop()

    stop_searching_event.clear()
    search_thread = threading.Thread(target=_search_worker, args=(command_parts,))
    search_thread.start()

def handle_stop():
    print("info string Received 'stop' command.")
    sys.stdout.flush()
    # we wait for the thread to finish on it's own
    # joining would hang the main loop
    stop_searching_event.set() 

def handle_quit():
    print("info string Received 'quit' command. Shutting down.")
    sys.stdout.flush()
    if search_thread and search_thread.is_alive():
        handle_stop()
        # we're closing the entire program; wait for the search to end
        search_thread.join(timeout=1.0) 
    sys.exit(0)

def main():
    while True:
        # use readline to handle input gracefully
        command = sys.stdin.readline().strip()
        
        # if the line is empty continue
        if not command:
            continue

        # uci commands are separated spaces
        command_parts = command.split()
        cmd = command_parts[0]

        if cmd == "uci":
            handle_uci()
        elif cmd == "isready":
            print("readyok")
            sys.stdout.flush()
        elif cmd == "ucinewgame":
            pass # do nothing
        elif cmd == "position":
            handle_position(command_parts)
        elif cmd == "go":
            handle_go(command_parts)
        elif cmd == "stop":
            handle_stop()
        elif cmd == "quit":
            handle_quit()
        else:
            # unknown command, can be ignored or logged.
            # setoption is not included as we do not have any options to set.
            print(f"info string Unknown command: {command}", file=sys.stderr)
            sys.stdout.flush()

if __name__ == "__main__":
    main()
