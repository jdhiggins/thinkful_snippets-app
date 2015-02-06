import psycopg2
import sys
from sys import exit
import logging
import argparse

#Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")


def put(name, snippet, hide):
    """
    Store a snippet with an associated name.
  
    Returns the name and the snippet
    """
#    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    logging.info("Storing snippet {!r}: {!r}. Hide: {}.".format(name, snippet, hide))
    with connection, connection.cursor() as cursor:
        try:
            command = "insert into snippets values (%s, %s, %s)"
            cursor.execute(command, (name, snippet, hide))
        except psycopg2.IntegrityError as e:
            command = "update snippets set message=%s where keyword=%s.  Hidden state=%s"
            cursor.execute(command, (snippet, name, hide))
    logging.debug("Snippet stored successfully.")
    return name, snippet, hide

def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet, create new blank snippet with that name?
    Or,return error, ask user for a different snippet name?
    Returns the snippet.
    """
#    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    logging.info("Retrieving snippet message from {!r}".format(name))
#    cursor = connection.cursor()
#    command = "select keyword, message from snippets where keyword='{}'".format(name)
#    cursor.execute(command, name)
#    result = cursor.fetchone()
#    connection.commit()
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        result = cursor.fetchone()
    if not result:
        #No snippet was found with that name.
        print "No keyword '{}' found.".format(name)
        print "Would you like to add '{}' as a keyword?".format(name)
        answer = raw_input("Y/N?  ")
        if answer.lower() == 'y':
            msg = raw_input("Type a message to associate to the keyword {} (Enter for blank.)".format(name))
            put(name, msg)
# add No case
    else:
        return result[0]

def catalog():    
    with connection, connection.cursor() as cursor:
        #use order by keyword to return in alphabetical order
        cursor.execute("select keyword from snippets where not hidden order by keyword")
        result = cursor.fetchall()
    return result

def search(search_word):    
    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets where not hidden where message like '%{}%'".format(search_word,))
        result = cursor.fetchall()
    return result
    
    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    put_parser.add_argument("--hide", action='store_true', help='hidden flag')
#    put_parser.add_argument("--unhide", action='store_false', help='unhide flag')
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    # Subparser for the catalog command
    logging.debug("Constructing the catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Get a keyword list")
     
    # Subparser for the search command
    logging.debug("Constructing the search subparser")
    search_parser = subparsers.add_parser("search", help="Search message for words")
    search_parser.add_argument("search_word", help="The word to be searched")
        

    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    print arguments
    
    if command == "put":
        name, snippet, hide = put(**arguments)
        print ("Stored {!r} as {!r}".format(snippet, name))
        print ("Hidden state: {}".format(hide))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        keywords = catalog()
        # right now keywords is a list of tuples (singletons)
#        keywords = ", ".join([x[0] for x in keywords])
#        print "Keywords: " + keywords
        for x in keywords:
            print x[0] + ",",
    elif command == "search":
        search_results = search(**arguments)
        for result in search_results:
            print "Keyword: {}   Message: {}".format(result[0], result[1])
        
if __name__ == "__main__":
    main()
