# Mendeley2Zotero

## Important note (as of 02/2019)

This tool probably will not work on any newer versions of Mendeley (>=1.19), since [they started encrypting the local database](https://github.com/rdiaz02/Adios_Mendeley/issues/4). In addition, [Zotero has since added official Mendeley import functionality](https://www.zotero.org/support/kb/mendeley_import), which I would recommend giving a shot before trying anything else.

## A mendeley to zotero metadata exporter

Tool to transfer metadata which is not covered in the existing Mendeley export formats (biblatex, rsi) from Mendeley to Zotero.

It might not be efficiently written but it does the job. Feel free to extend to further metadata.

## Why?

During switching from Mendeley to Zotero you will be faced with diverse nontransferred metadata. The most important of these are dates you added publications to the library and the Mendeley Folder structure.

The export formats provided in Mendeley (biblatex, rsi) do not include any of these data.

> **NOTE:** This script works directly on the sqlite databases of both programs. BACKUP your sqlite files before letting this script change them.

## Usage & supported metadata

```python mendeley2zotero.py -m M -z Z {added_dates, collections, repair_dates}```

### M
Path to mendeley sqlite file - on OSX this should reside in ```/Users/USERNAME/Library/Application Support/Mendeley Desktop```

### Z
Path to zotero sqlite file - on OSX this should reside in ```/Users/USERNAME/Library/Application Support/Zotero/Profiles/KEY.default/zotero```

### added_dates
transfer "date added" information to Zotero

Usage:
```python mendeley2zotero.py -m M -z Z added_dates```

### collections
transfer Mendeley folders to Zotero collections

For now, beforehand, create by hand in Zotero the desired structure of Collections/Subcollections. Then run the below.

> **NOTE:** Nonunique names are not supported for now - i.e. all your Collections should have a distinct name.

### repair_dates
<a name="repair_dates"></a>
only neccessary if you ran v.0.1 to import added dates. this forces all added_date entries to the zotero compliant datetime. This was fixed in v.0.2 and should not be neccessary. 

Usage: 
```python mendeley2zotero.py -m M -z Z repair_dates```

## Dependencies

* [SQLAlchemy](http://www.sqlalchemy.org/).
* Indirectly: [SQLACodegen](https://github.com/ksindi/sqlacodegen). SQLACodegen was used to reverse engineer the database object relational model of mendeley and zotero in the db_classes_*.py files.

# Versions

* 0.1.1: fixed a bug with the sqlite datetime format that prevented syncing with the zotero server - see the [repair dates](#repair_dates) function if you were affected.
* 0.1.0: initial version
