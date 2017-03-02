# coding: utf-8
from sqlalchemy import Boolean, Column, Date, ForeignKey, Index, Integer, Numeric, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME

Base = declarative_base()
metadata = Base.metadata

# custom date_time format for zotero, prevents HH:MM:SS.SSSS entries - these messed up the
# zotero syncing (see https://forums.zotero.org/discussion/41017)

sqlite_date = DATETIME(
    storage_format="%(year)04d-%(month)02d-%(day)02d %(hour)02d:%(minute)02d:%(second)02d",
    regexp=r"(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)(?:.(\d+))?"
)

class Annotation(Base):
    __tablename__ = 'annotations'

    annotationID = Column(Integer, primary_key=True)
    itemID = Column(ForeignKey('itemAttachments.itemID'), index=True)
    parent = Column(Text)
    textNode = Column(Integer)
    offset = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    cols = Column(Integer)
    rows = Column(Integer)
    text = Column(Text)
    collapsed = Column(Boolean)
    dateModified = Column(Date)

    itemAttachment = relationship(u'Itemattachment')


class Basefieldmapping(Base):
    __tablename__ = 'baseFieldMappings'

    itemTypeID = Column(ForeignKey('itemTypes.itemTypeID'), primary_key=True, nullable=False)
    baseFieldID = Column(ForeignKey('fields.fieldID'), primary_key=True, nullable=False, index=True)
    fieldID = Column(ForeignKey('fields.fieldID'), primary_key=True, nullable=False, index=True)

    field = relationship(u'Field', primaryjoin='Basefieldmapping.baseFieldID == Field.fieldID')
    field1 = relationship(u'Field', primaryjoin='Basefieldmapping.fieldID == Field.fieldID')
    itemType = relationship(u'Itemtype')


class Basefieldmappingscombined(Base):
    __tablename__ = 'baseFieldMappingsCombined'

    itemTypeID = Column(Integer, primary_key=True, nullable=False)
    baseFieldID = Column(Integer, primary_key=True, nullable=False, index=True)
    fieldID = Column(Integer, primary_key=True, nullable=False, index=True)


class Charset(Base):
    __tablename__ = 'charsets'

    charsetID = Column(Integer, primary_key=True)
    charset = Column(Text, index=True)


class Collectionitem(Base):
    __tablename__ = 'collectionItems'

    collectionID = Column(ForeignKey('collections.collectionID'), primary_key=True, nullable=False)
    itemID = Column(ForeignKey('items.itemID'), primary_key=True, nullable=False, index=True)
    orderIndex = Column(Integer, server_default=u'0')

    collection = relationship(u'Collection')
    item = relationship(u'Item')


class Collection(Base):
    __tablename__ = 'collections'

    collectionID = Column(Integer, primary_key=True)
    collectionName = Column(Text, nullable=False)
    parentCollectionID = Column(ForeignKey('collections.collectionID'), server_default=u'NULL')
    dateAdded = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    dateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    clientDateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    libraryID = Column(Integer)
    key = Column(Text, nullable=False)

    parent = relationship(u'Collection', remote_side=[collectionID])


class Creatordatum(Base):
    __tablename__ = 'creatorData'
    __table_args__ = (
        Index('creatorData_name', 'lastName', 'firstName'),
    )

    creatorDataID = Column(Integer, primary_key=True)
    firstName = Column(Text)
    lastName = Column(Text)
    shortName = Column(Text)
    fieldMode = Column(Integer)
    birthYear = Column(Integer)


class Creatortype(Base):
    __tablename__ = 'creatorTypes'

    creatorTypeID = Column(Integer, primary_key=True)
    creatorType = Column(Text)


class Creator(Base):
    __tablename__ = 'creators'

    creatorID = Column(Integer, primary_key=True)
    creatorDataID = Column(ForeignKey('creatorData.creatorDataID'), nullable=False, index=True)
    dateAdded = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    dateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    clientDateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    libraryID = Column(Integer)
    key = Column(Text, nullable=False)

    creatorDatum = relationship(u'Creatordatum')


class Custombasefieldmapping(Base):
    __tablename__ = 'customBaseFieldMappings'

    customItemTypeID = Column(ForeignKey('customItemTypes.customItemTypeID'), primary_key=True, nullable=False)
    baseFieldID = Column(ForeignKey('fields.fieldID'), primary_key=True, nullable=False, index=True)
    customFieldID = Column(ForeignKey('customFields.customFieldID'), primary_key=True, nullable=False, index=True)

    field = relationship(u'Field')
    customField = relationship(u'Customfield')
    customItemType = relationship(u'Customitemtype')


class Customfield(Base):
    __tablename__ = 'customFields'

    customFieldID = Column(Integer, primary_key=True)
    fieldName = Column(Text)
    label = Column(Text)


class Customitemtypefield(Base):
    __tablename__ = 'customItemTypeFields'

    customItemTypeID = Column(ForeignKey('customItemTypes.customItemTypeID'), primary_key=True, nullable=False)
    fieldID = Column(ForeignKey('fields.fieldID'), index=True)
    customFieldID = Column(ForeignKey('customFields.customFieldID'), index=True)
    hide = Column(Integer, nullable=False)
    orderIndex = Column(Integer, primary_key=True, nullable=False)

    customField = relationship(u'Customfield')
    customItemType = relationship(u'Customitemtype')
    field = relationship(u'Field')


class Customitemtype(Base):
    __tablename__ = 'customItemTypes'

    customItemTypeID = Column(Integer, primary_key=True)
    typeName = Column(Text)
    label = Column(Text)
    display = Column(Integer, server_default=u'1')
    icon = Column(Text)


class Deleteditem(Base):
    __tablename__ = 'deletedItems'

    itemID = Column(Integer, primary_key=True)
    dateDeleted = Column(NullType, nullable=False, index=True, server_default=u'CURRENT_TIMESTAMP')


class Fieldformat(Base):
    __tablename__ = 'fieldFormats'

    fieldFormatID = Column(Integer, primary_key=True)
    regex = Column(Text)
    isInteger = Column(Integer)


class Field(Base):
    __tablename__ = 'fields'

    fieldID = Column(Integer, primary_key=True)
    fieldName = Column(Text)
    fieldFormatID = Column(ForeignKey('fieldFormats.fieldFormatID'))

    fieldFormat = relationship(u'Fieldformat')


class Fieldscombined(Base):
    __tablename__ = 'fieldsCombined'

    fieldID = Column(Integer, primary_key=True)
    fieldName = Column(Text, nullable=False)
    label = Column(Text)
    fieldFormatID = Column(Integer)
    custom = Column(Integer, nullable=False)


class Filetypemimetype(Base):
    __tablename__ = 'fileTypeMimeTypes'

    fileTypeID = Column(ForeignKey('fileTypes.fileTypeID'), primary_key=True, nullable=False)
    mimeType = Column(Text, primary_key=True, nullable=False, index=True)

    fileType = relationship(u'Filetype')


class Filetype(Base):
    __tablename__ = 'fileTypes'

    fileTypeID = Column(Integer, primary_key=True)
    fileType = Column(Text, index=True)


t_fulltextItemWords = Table(
    'fulltextItemWords', metadata,
    Column('wordID', ForeignKey('fulltextWords.wordID'), primary_key=True, nullable=False),
    Column('itemID', ForeignKey('items.itemID'), primary_key=True, nullable=False, index=True)
)


class Fulltextword(Base):
    __tablename__ = 'fulltextWords'

    wordID = Column(Integer, primary_key=True)
    word = Column(Text)


class Groupitem(Base):
    __tablename__ = 'groupItems'

    itemID = Column(Integer, primary_key=True)
    createdByUserID = Column(ForeignKey('users.userID'), nullable=False)
    lastModifiedByUserID = Column(ForeignKey('users.userID'), nullable=False)

    user = relationship(u'User', primaryjoin='Groupitem.createdByUserID == User.userID')
    user1 = relationship(u'User', primaryjoin='Groupitem.lastModifiedByUserID == User.userID')


class Group(Base):
    __tablename__ = 'groups'

    groupID = Column(Integer, primary_key=True)
    libraryID = Column(ForeignKey('libraries.libraryID'), nullable=False)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    editable = Column(Integer, nullable=False)
    filesEditable = Column(Integer, nullable=False)

    library = relationship(u'Library')


class Highlight(Base):
    __tablename__ = 'highlights'

    highlightID = Column(Integer, primary_key=True)
    itemID = Column(ForeignKey('itemAttachments.itemID'), index=True)
    startParent = Column(Text)
    startTextNode = Column(Integer)
    startOffset = Column(Integer)
    endParent = Column(Text)
    endTextNode = Column(Integer)
    endOffset = Column(Integer)
    dateModified = Column(Date)

    itemAttachment = relationship(u'Itemattachment')


class Itemcreator(Base):
    __tablename__ = 'itemCreators'

    itemID = Column(ForeignKey('items.itemID'), primary_key=True, nullable=False)
    creatorID = Column(ForeignKey('creators.creatorID'), primary_key=True, nullable=False)
    creatorTypeID = Column(ForeignKey('creatorTypes.creatorTypeID'), primary_key=True, nullable=False, server_default=u'1')
    orderIndex = Column(Integer, primary_key=True, nullable=False, server_default=u'0')

    creator = relationship(u'Creator')
    creatorType = relationship(u'Creatortype')
    item = relationship(u'Item')


class Itemdatum(Base):
    __tablename__ = 'itemData'

    itemID = Column(ForeignKey('items.itemID'), primary_key=True, nullable=False)
    fieldID = Column(ForeignKey('fields.fieldID'), primary_key=True, nullable=False, index=True)
    valueID = Column(ForeignKey('itemDataValues.valueID'))

    field = relationship(u'Field')
    item = relationship(u'Item')
    itemDataValue = relationship(u'Itemdatavalue')


class Itemdatavalue(Base):
    __tablename__ = 'itemDataValues'

    valueID = Column(Integer, primary_key=True)
    value = Column(NullType)


t_itemSeeAlso = Table(
    'itemSeeAlso', metadata,
    Column('itemID', ForeignKey('items.itemID'), primary_key=True, nullable=False),
    Column('linkedItemID', ForeignKey('items.itemID'), primary_key=True, nullable=False, index=True)
)


t_itemTags = Table(
    'itemTags', metadata,
    Column('itemID', ForeignKey('items.itemID'), primary_key=True, nullable=False),
    Column('tagID', ForeignKey('tags.tagID'), primary_key=True, nullable=False, index=True)
)


class Itemtypecreatortype(Base):
    __tablename__ = 'itemTypeCreatorTypes'

    itemTypeID = Column(ForeignKey('itemTypes.itemTypeID'), primary_key=True, nullable=False)
    creatorTypeID = Column(ForeignKey('creatorTypes.creatorTypeID'), primary_key=True, nullable=False, index=True)
    primaryField = Column(Integer)

    creatorType = relationship(u'Creatortype')
    itemType = relationship(u'Itemtype')


class Itemtypefield(Base):
    __tablename__ = 'itemTypeFields'

    itemTypeID = Column(ForeignKey('itemTypes.itemTypeID'), primary_key=True, nullable=False)
    fieldID = Column(ForeignKey('fields.fieldID'), index=True)
    hide = Column(Integer)
    orderIndex = Column(Integer, primary_key=True, nullable=False)

    field = relationship(u'Field')
    itemType = relationship(u'Itemtype')


class Itemtypefieldscombined(Base):
    __tablename__ = 'itemTypeFieldsCombined'

    itemTypeID = Column(Integer, primary_key=True, nullable=False)
    fieldID = Column(Integer, nullable=False, index=True)
    hide = Column(Integer)
    orderIndex = Column(Integer, primary_key=True, nullable=False)


class Itemtype(Base):
    __tablename__ = 'itemTypes'

    itemTypeID = Column(Integer, primary_key=True)
    typeName = Column(Text)
    templateItemTypeID = Column(Integer)
    display = Column(Integer, server_default=u'1')


class Itemtypescombined(Base):
    __tablename__ = 'itemTypesCombined'

    itemTypeID = Column(Integer, primary_key=True)
    typeName = Column(Text, nullable=False)
    display = Column(Integer, nullable=False, server_default=u'1')
    custom = Column(Integer, nullable=False)


class Item(Base):
    __tablename__ = 'items'

    itemID = Column(Integer, primary_key=True)
    itemTypeID = Column(Integer, nullable=False)
    dateAdded = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    dateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    clientDateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    libraryID = Column(ForeignKey('libraries.libraryID'))
    key = Column(Text, nullable=False)

    library = relationship(u'Library')
    fulltextWords = relationship(u'Fulltextword', secondary='fulltextItemWords')
    tags = relationship(u'Tag', secondary='itemTags')
    parents = relationship(
        u'Item',
        secondary='itemSeeAlso',
        primaryjoin=u'Item.itemID == itemSeeAlso.c.itemID',
        secondaryjoin=u'Item.itemID == itemSeeAlso.c.linkedItemID'
    )


class Fulltextitem(Item):
    __tablename__ = 'fulltextItems'

    itemID = Column(ForeignKey('items.itemID'), primary_key=True)
    version = Column(Integer, index=True)
    indexedPages = Column(Integer)
    totalPages = Column(Integer)
    indexedChars = Column(Integer)
    totalChars = Column(Integer)
    synced = Column(Integer, server_default=u'0')


class Itemattachment(Item):
    __tablename__ = 'itemAttachments'

    itemID = Column(primary_key=True)#ForeignKey('items.itemID'), primary_key=True)
    sourceItemID = Column(ForeignKey('items.itemID'), index=True)
    linkMode = Column(Integer)
    mimeType = Column(Text, index=True)
    charsetID = Column(Integer)
    path = Column(Text)
    originalPath = Column(Text)
    syncState = Column(Integer, index=True, server_default=u'0')
    storageModTime = Column(Integer)
    storageHash = Column(Text)

    item = relationship(u'Item', primaryjoin='Itemattachment.sourceItemID == Item.itemID')


class Itemnote(Item):
    __tablename__ = 'itemNotes'

    itemID = Column(primary_key=True)#ForeignKey('items.itemID'), primary_key=True)
    sourceItemID = Column(ForeignKey('items.itemID'), index=True)
    note = Column(Text)
    title = Column(Text)

    item = relationship(u'Item', primaryjoin='Itemnote.sourceItemID == Item.itemID')


class Library(Base):
    __tablename__ = 'libraries'

    libraryID = Column(Integer, primary_key=True)
    libraryType = Column(Text, nullable=False)


class Proxy(Base):
    __tablename__ = 'proxies'

    proxyID = Column(Integer, primary_key=True)
    multiHost = Column(Integer)
    autoAssociate = Column(Integer)
    scheme = Column(Text)


class Proxyhost(Base):
    __tablename__ = 'proxyHosts'

    hostID = Column(Integer, primary_key=True)
    proxyID = Column(ForeignKey('proxies.proxyID'), index=True)
    hostname = Column(Text)

    proxy = relationship(u'Proxy')


class Relation(Base):
    __tablename__ = 'relations'

    libraryID = Column(Integer, nullable=False)
    subject = Column(Text, primary_key=True, nullable=False)
    predicate = Column(Text, primary_key=True, nullable=False)
    object = Column(Text, primary_key=True, nullable=False, index=True)
    clientDateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')


class Savedsearchcondition(Base):
    __tablename__ = 'savedSearchConditions'

    savedSearchID = Column(ForeignKey('savedSearches.savedSearchID'), primary_key=True)
    searchConditionID = Column(Integer, primary_key=True)
    condition = Column(Text)
    operator = Column(Text)
    value = Column(Text)
    required = Column(Numeric)

    savedSearch = relationship(u'Savedsearch')


class Savedsearch(Base):
    __tablename__ = 'savedSearches'

    savedSearchID = Column(Integer, primary_key=True)
    savedSearchName = Column(Text, nullable=False)
    dateAdded = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    dateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    clientDateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    libraryID = Column(Integer)
    key = Column(Text, nullable=False)


class Setting(Base):
    __tablename__ = 'settings'

    setting = Column(Text, primary_key=True, nullable=False)
    key = Column(Text, primary_key=True, nullable=False)
    value = Column(NullType)


class Storagedeletelog(Base):
    __tablename__ = 'storageDeleteLog'

    libraryID = Column(Integer, primary_key=True, nullable=False)
    key = Column(Text, primary_key=True, nullable=False)
    timestamp = Column(Integer, nullable=False, index=True)


t_syncDeleteLog = Table(
    'syncDeleteLog', metadata,
    Column('syncObjectTypeID', ForeignKey('syncObjectTypes.syncObjectTypeID'), nullable=False),
    Column('libraryID', Integer, nullable=False),
    Column('key', Text, nullable=False),
    Column('timestamp', Integer, nullable=False, index=True)
)


class Syncobjecttype(Base):
    __tablename__ = 'syncObjectTypes'

    syncObjectTypeID = Column(Integer, primary_key=True)
    name = Column(Text, index=True)


class Syncedsetting(Base):
    __tablename__ = 'syncedSettings'

    setting = Column(Text, primary_key=True, nullable=False)
    libraryID = Column(Integer, primary_key=True, nullable=False)
    value = Column(NullType, nullable=False)
    version = Column(Integer, nullable=False, server_default=u'0')
    synced = Column(Integer, nullable=False, server_default=u'0')


class Tag(Base):
    __tablename__ = 'tags'

    tagID = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    type = Column(Integer, nullable=False)
    dateAdded = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    dateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    clientDateModified = Column(sqlite_date, nullable=False, server_default=u'CURRENT_TIMESTAMP')
    libraryID = Column(Integer)
    key = Column(Text, nullable=False)


class Transactionlog(Base):
    __tablename__ = 'transactionLog'

    transactionID = Column(ForeignKey('transactions.transactionID'), primary_key=True, nullable=False)
    field = Column(Text, primary_key=True, nullable=False)
    value = Column(Numeric, primary_key=True, nullable=False)

    transaction = relationship(u'Transaction')


class Transactionset(Base):
    __tablename__ = 'transactionSets'

    transactionSetID = Column(Integer, primary_key=True)
    event = Column(Text)
    id = Column(Integer)


class Transaction(Base):
    __tablename__ = 'transactions'

    transactionID = Column(Integer, primary_key=True)
    transactionSetID = Column(Integer, index=True)
    context = Column(Text)
    action = Column(Text)


class Translatorcache(Base):
    __tablename__ = 'translatorCache'

    leafName = Column(Text, primary_key=True)
    translatorJSON = Column(Text)
    code = Column(Text)
    lastModifiedTime = Column(Integer)


class User(Base):
    __tablename__ = 'users'

    userID = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False)


class Version(Base):
    __tablename__ = 'version'

    schema = Column(Text, primary_key=True, index=True)
    version = Column(Integer, nullable=False)


class Zoterodummytable(Base):
    __tablename__ = 'zoteroDummyTable'

    id = Column(Integer, primary_key=True)
