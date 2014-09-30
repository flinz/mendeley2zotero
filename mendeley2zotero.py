import db_classes_mendeley as db_m
import db_classes_zotero as db_z
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import argparse as ap

# ########## INPUT HANDLING
parser = ap.ArgumentParser()
sp = parser.add_subparsers(help="", dest='command')
sp_added = sp.add_parser('added_dates', help='Update \"Date Added\" field', description='Updates the Zotero field \"Date Added\" from Mendeley data')
sp_collections = sp.add_parser('collections', help='Update collections', description='Updates the document associations to existing collections (for now create the desired collections by hand before)')
parser.add_argument("-z", "--zotero_db", action="store", default="", help="zotero sqlite database path", required=True)
parser.add_argument("-m", "--mendeley_db", action="store", default="", help="mendeley sqlite database path", required=True)
args = parser.parse_args()

# ########## SETUP PATHS AND DICTS
dbs = { "m", "z" }
db_string = {
    "m": args.mendeley_db,
    "z": args.zotero_db
}
db_class = { 
    "m": db_m,
    "z": db_z
}

# ########## SQLALCHEMY SESSION SETUP
engine = { 
    s: create_engine('sqlite:///'+db_string[s]) for s in dbs
}
Session = { 
    s: sessionmaker(bind=engine[s]) for s in dbs
}
session = { 
    s: Session[s]() for s in dbs
}

# ########## MAIN LOOP

# get all zotero items by getting their titles (workaround for possibly incomplete reverse engineered db classes)
field_title = session["z"].query(db_class["z"].Field).filter(db_class["z"].Field.fieldName=="title").one()
type_attachment = session["z"].query(db_class["z"].Itemtype).filter(db_class["z"].Itemtype.typeName=="attachment").one()
z_titles = session["z"].query(db_class["z"].Itemdatum).filter(db_class["z"].Itemdatum.fieldID == field_title.fieldID).all()

for i,z_title_ob in enumerate(z_titles):
    
    z_item = z_title_ob.item
    
    # skip attachment items
    if z_item.itemTypeID == type_attachment.itemTypeID:
        continue

    # get mendeley equivalent by title
    z_title = z_title_ob.itemDataValue.value
    m_titles = session["m"].query(db_class["m"].Document).filter(db_class["m"].Document.title == z_title).all()
    
    if not m_titles:
        print "[%i/%i] " % (i+1,len(z_titles)),  
        print "No Mendeley equivalent for item title \"%s\" found." % z_title
        continue
    
    if args.command == "added_dates":
        # get the maximum date added (can have more than one title matching)
        d_added = max([mt.added for mt in m_titles])
        # convert to datetime
        d_added = datetime.datetime.utcfromtimestamp(d_added)
        z_item.dateAdded = d_added
        
        session["z"].add(z_item)

        # commit in batches of 10
        if i % 10 == 0 or i==len(z_titles)-1:
            try:
                session["z"].commit()
            except Error:
                print "Error during batch commit. Rolling back."
                session.rollback()
            print "[%i/%i] " % (i+1,len(z_titles)),  
            print " batch committed."

    if args.command == "collections":

        for m_object in m_titles:

            # get all associated folders for mendeley object
            folders_assoc = session["m"].query(db_class["m"].Documentfolder).filter(db_class["m"].Documentfolder.documentId == m_object.id).all()
            
            for f in folders_assoc:
                folder = session["m"].query(db_class["m"].Folder).filter(db_class["m"].Folder.id == f.folderId).one()
                # get matching zotero collections
                collections = session["z"].query(db_class["z"].Collection).filter(db_class["z"].Collection.collectionName == folder.name).all()
                
                if not collections:
                    print "[%i/%i] " % (i+1,len(z_titles)),  
                    print "No Zotero equivalent for Mendeley collection \"%s\" found." % f.name
                    continue

                # make a new collectionitem association
                # easiest: commit on add, to catch integrityerrors 
                for coll in collections:
                    tmp_collItem = db_class["z"].Collectionitem()
                    tmp_collItem.itemID = z_item.itemID
                    tmp_collItem.collectionID = coll.collectionID
                    try:
                        session["z"].add(tmp_collItem)
                        session["z"].commit()   
                    except IntegrityError:
                        session["z"].rollback()
                        print "[%i/%i] " % (i+1,len(z_titles)),  
                        print "Skipping existing association." 