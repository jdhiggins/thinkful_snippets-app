import sys
import logging
import argparse
'''test of git push'''
#Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """
    Store a snippet with an associated name.
  
    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet, create new blank snippet with that name?
    Or,return error, ask user for a different snippet name?
    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    arguments = parser.parse_args(sys.argv[1:])

if __name__ == "__main__":
    main()

