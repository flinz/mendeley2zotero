# Mendeley2Zotero

**A mendeley to zotero metadata exporter**

Tool to transfer metadata which is not covered in the existing Mendeley export formats (biblatex, rsi) from Mendeley to Zotero.

It might not be efficiently written but it does the job. Feel free to extend to further metadata.

## Why?

During switching from Mendeley to Zotero you will be faced with diverse nontransferred metadata. The most important of these are dates you added publications to the library and the Mendeley Folder structure.

The export formats provided in Mendeley (biblatex, rsi) do not include any of these data.

> **NOTE:** This script works directly on the sqlite databases of both programs. BACKUP your sqlite files before letting this script change them.

## Usage & supported metadata

```python exporter.py -m M -z Z {added_dates, collections}```

### M
Path to mendeley sqlite file - on OSX this should reside in ```/Users/USERNAME/Library/Application Support/Mendeley Desktop```

### Z
Path to zotero sqlite file - on OSX this should reside in ```/Users/USERNAME/Library/Application Support/Zotero/Profiles/KEY.default/zotero```

### added_dates
transfer "date added" information to Zotero

Usage:
```python exporter.py -m M -z Z added_dates```

### collections
transfer Mendeley folders to Zotero collections

For now, beforehand, create by hand in Zotero the desired structure of Collections/Subcollections. Then run the below.

> **NOTE:** Nonunique names are not supported for now - i.e. all your Collections should have a distinct name.

Usage: 
```python exporter.py -m M -z Z collections```

## Dependencies

* [SQLAlchemy](http://www.sqlalchemy.org/).
* Indirectly: [SQLACodegen](https://github.com/ksindi/sqlacodegen). SQLACodegen was used to reverse engineer the database object relational model of mendeley and zotero in the db_classes_*.py files.