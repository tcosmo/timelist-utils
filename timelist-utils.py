#!python3
import sys, os
import json

from config import Config
import uuid

json_dumping_options = { 'indent': 4, 'separators': ( ',', ': ' ), 'ensure_ascii': False }

list_main_fname = "list_main.json"
with open( list_main_fname, 'r' ) as f:
    list_main_d = json.load( f )

entry_main_fname = "entry_main.json"
with open( entry_main_fname, 'r' ) as f:
    entry_main_d = json.load( f )

def new_list():
    """ Creates a new list in db:
            db/<unique_foldername>/main.json
            db/<unique_foldername>/entries
    """

    unique_foldername = str( uuid.uuid4().hex )
    path_to_list      = os.path.join( Config.TL_DB_PATH, unique_foldername )

    os.makedirs( path_to_list )
    os.makedirs( os.path.join( path_to_list, 'entries' ) )

    list_main_d_copy = list_main_d.copy()
    list_main_d_copy[ 'uuid' ] = unique_foldername

    with open( os.path.join( path_to_list, 'main.json' ), 'w' ) as f:
        json.dump( list_main_d_copy, f, **json_dumping_options )

    print( path_to_list )

available_lists = {}
def lists( verbose = True ):
    global available_lists
    available_lists = {}
    if verbose:
        print( "db path:", Config.TL_DB_PATH )
    for file in os.listdir( Config.TL_DB_PATH  ):
        if file[ 0 ] != '.' and os.path.isdir( os.path.join( Config.TL_DB_PATH, file ) ):
            with open( os.path.join( Config.TL_DB_PATH, file, 'main.json' ), 'r' ) as f:
                main_d = json.load( f )
            available_lists[ main_d[ 'uuid' ] ] = True
            if verbose:
                name = main_d[ 'name' ] if not main_d[ 'name' ] == "" else "unnamed"
                print( '\t-', name+',', main_d[ 'uuid' ] )

def new_entry( list_uuid ):
    unique_filename = str( uuid.uuid4().hex )
    path_to_entry     = os.path.join( Config.TL_DB_PATH, list_uuid, 'entries', unique_filename )

    os.makedirs( os.path.join( path_to_entry ) )
    os.makedirs( os.path.join( path_to_entry, 'images' ) )
    os.makedirs( os.path.join( path_to_entry, 'assets' ) )

    with open( os.path.join( path_to_entry, 'ref.bib' ), 'w' ) as f:
        pass

    with open( os.path.join( path_to_entry, 'content.md' ), 'w' ) as f:
        pass

    entry_main_d_copy = entry_main_d.copy()
    entry_main_d_copy[ 'uuid' ] = unique_filename

    with open( os.path.join( path_to_entry, 'main.json' ), 'w' ) as f:
        json.dump( entry_main_d_copy, f, **json_dumping_options )

    print( path_to_entry )

def usage():
    print("Usage:")
    print("./timelist-utils.py lists")
    print("./timelist-utils.py new list")
    print("./timelist-utils.py new entry <list_uuid>")

def main():
    list_args = sys.argv

    if len( list_args ) < 2:
        usage()
        exit( 1 )

    if list_args[ 1 ] == 'lists':
        lists()
        exit( 0 )
    elif list_args[ 1 ] == 'new':
        if len( list_args ) < 3:
            usage()
            exit( 1 )

        if list_args[ 2 ] == 'list':
            new_list()
            exit( 0 )
        elif list_args[ 2 ] == 'entry':
            if len( list_args ) < 4:
                usage()
                exit( 1 )

            list_id = list_args[ 3 ]
            if list_id in available_lists:
                new_entry( list_id )
                exit( 0 )
            else:
                print("No list under that uuid.")
                exit( 1 )
        else:
            usage()
            exit( 1 )
    else:
        usage()
        exit( 1 )

    print( sys.argv )

if __name__ == '__main__':
    lists( verbose = False )
    main()
#new_list()
#lists()
#new_entry( "63a333393188498fbe2f471f16660b07" )
