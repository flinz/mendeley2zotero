# coding: utf-8
from sqlalchemy import BigInteger, Boolean, Column, DateTime, Float, ForeignKey, Integer, LargeBinary, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Canonicaldocument(Base):
    __tablename__ = 'CanonicalDocuments'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False)
    catalogUrl = Column(String)
    downloadUrl = Column(String)
    lastModified = Column(Integer, nullable=False)


t_DataCleaner = Table(
    'DataCleaner', metadata,
    Column('version', Integer, nullable=False)
)


class Documentcanonicalid(Base):
    __tablename__ = 'DocumentCanonicalIds'

    documentId = Column(Integer, primary_key=True)
    canonicalId = Column(Integer, nullable=False, index=True)
    timestamp = Column(Integer, nullable=False)


class Documentcontributor(Base):
    __tablename__ = 'DocumentContributors'

    id = Column(Integer, primary_key=True)
    documentId = Column(Integer, nullable=False, index=True)
    contribution = Column(String, nullable=False)
    firstNames = Column(String)
    lastName = Column(String, nullable=False)


class Documentdetailsbase(Base):
    __tablename__ = 'DocumentDetailsBase'

    documentId = Column(Integer, primary_key=True, nullable=False, index=True)
    fieldId = Column(Integer, primary_key=True, nullable=False)
    originalValue = Column(String)
    conflictValue = Column(String)


class Documentfield(Base):
    __tablename__ = 'DocumentFields'

    fieldId = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


t_DocumentFiles = Table(
    'DocumentFiles', metadata,
    Column('documentId', Integer, nullable=False, index=True),
    Column('hash', String, nullable=False, index=True),
    Column('remoteUrl', String, nullable=False),
    Column('unlinked', Boolean, nullable=False),
    Column('downloadRestricted', Boolean, nullable=False, server_default=u'0')
)


class Documentfolder(Base):
    __tablename__ = 'DocumentFolders'

    documentId = Column(Integer, primary_key=True, nullable=False)
    folderId = Column(Integer, primary_key=True, nullable=False)


class Documentfoldersbase(Base):
    __tablename__ = 'DocumentFoldersBase'

    documentId = Column(Integer, primary_key=True, nullable=False, index=True)
    folderId = Column(Integer, primary_key=True, nullable=False)


class Documentkeyword(Base):
    __tablename__ = 'DocumentKeywords'

    documentId = Column(Integer, primary_key=True, nullable=False)
    keyword = Column(String, primary_key=True, nullable=False)


class Documentreference(Base):
    __tablename__ = 'DocumentReferences'

    documentId = Column(Integer, primary_key=True, nullable=False, index=True)
    referencedDocumentId = Column(Integer, primary_key=True, nullable=False, index=True)


class Documenttag(Base):
    __tablename__ = 'DocumentTags'

    documentId = Column(Integer, primary_key=True, nullable=False)
    tag = Column(String, primary_key=True, nullable=False)


class Documenturl(Base):
    __tablename__ = 'DocumentUrls'

    documentId = Column(Integer, primary_key=True, nullable=False)
    position = Column(Integer, primary_key=True, nullable=False)
    url = Column(String, nullable=False)


class Documentversion(Base):
    __tablename__ = 'DocumentVersion'

    documentId = Column(Integer, primary_key=True)
    version = Column(String)


class Documentzotero(Base):
    __tablename__ = 'DocumentZotero'

    documentId = Column(Integer, primary_key=True)
    zoteroID = Column(Integer, nullable=False)
    lastSyncTime = Column(Integer, nullable=False)


class Document(Base):
    __tablename__ = 'Documents'

    id = Column(Integer, primary_key=True)
    uuid = Column(String, nullable=False)
    confirmed = Column(Integer)
    deduplicated = Column(Integer)
    deletionPending = Column(Integer)
    favourite = Column(Integer)
    read = Column(Integer)
    onlyReference = Column(Integer)
    type = Column(String)
    abstract = Column(String)
    added = Column(Integer)
    modified = Column(Integer)
    importer = Column(String)
    note = Column(String)
    privacy = Column(String)
    title = Column(String)
    advisor = Column(String)
    articleColumn = Column(String)
    applicationNumber = Column(String)
    arxivId = Column(String)
    chapter = Column(String)
    citationKey = Column(String)
    city = Column(String)
    code = Column(String)
    codeNumber = Column(String)
    codeSection = Column(String)
    codeVolume = Column(String)
    committee = Column(String)
    counsel = Column(String)
    country = Column(String)
    dateAccessed = Column(String)
    day = Column(Integer)
    department = Column(String)
    doi = Column(String)
    edition = Column(String)
    genre = Column(String)
    hideFromMendeleyWebIndex = Column(Integer)
    institution = Column(String)
    internationalAuthor = Column(String)
    internationalNumber = Column(String)
    internationalTitle = Column(String)
    internationalUserType = Column(String)
    isbn = Column(String)
    issn = Column(String)
    issue = Column(String)
    language = Column(String)
    lastUpdate = Column(String)
    legalStatus = Column(String)
    length = Column(String)
    medium = Column(String)
    month = Column(Integer)
    originalPublication = Column(String)
    owner = Column(String)
    pages = Column(String)
    pmid = Column(BigInteger)
    publication = Column(String)
    publicLawNumber = Column(String)
    publisher = Column(String)
    reprintEdition = Column(String)
    reviewedArticle = Column(String)
    revisionNumber = Column(String)
    sections = Column(String)
    seriesEditor = Column(String)
    series = Column(String)
    seriesNumber = Column(String)
    session = Column(String)
    shortTitle = Column(String)
    sourceType = Column(String)
    userType = Column(String)
    volume = Column(String)
    year = Column(Integer)


class Eventattribute(Base):
    __tablename__ = 'EventAttributes'

    eventId = Column(ForeignKey('EventLog.id'), primary_key=True)
    attribute = Column(String, primary_key=True, nullable=False)
    value = Column(String, nullable=False)

    EventLog = relationship(u'Eventlog')


class Eventlog(Base):
    __tablename__ = 'EventLog'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)
    sent = Column(Boolean, nullable=False)


class Filehighlightrect(Base):
    __tablename__ = 'FileHighlightRects'

    id = Column(Integer, primary_key=True)
    highlightId = Column(Integer, nullable=False)
    page = Column(Integer, nullable=False)
    x1 = Column(Float, nullable=False)
    y1 = Column(Float, nullable=False)
    x2 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)


class Filehighlight(Base):
    __tablename__ = 'FileHighlights'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    uuid = Column(String, nullable=False)
    documentId = Column(Integer, nullable=False, index=True)
    fileHash = Column(String, nullable=False, index=True)
    createdTime = Column(String, nullable=False)
    unlinked = Column(Boolean, nullable=False)


class Filenote(Base):
    __tablename__ = 'FileNotes'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    uuid = Column(String, nullable=False)
    documentId = Column(Integer, nullable=False, index=True)
    fileHash = Column(String, nullable=False, index=True)
    page = Column(Integer, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    note = Column(String, nullable=False)
    modifiedTime = Column(String, nullable=False)
    createdTime = Column(String, nullable=False)
    unlinked = Column(Boolean, nullable=False)


t_FileReferenceCountsView = Table(
    'FileReferenceCountsView', metadata,
    Column('hash', String),
    Column('referenceCount', NullType)
)


class Fileviewstate(Base):
    __tablename__ = 'FileViewStates'

    hash = Column(String, primary_key=True)
    positionx = Column(Float, nullable=False)
    positiony = Column(Float, nullable=False)
    pagenumber = Column(Integer, nullable=False)
    zoommode = Column(Integer, nullable=False)
    zoomfactor = Column(Float, nullable=False)
    rotation = Column(Float, nullable=False)


class File(Base):
    __tablename__ = 'Files'

    hash = Column(String, primary_key=True)
    localUrl = Column(String, nullable=False)


class Folder(Base):
    __tablename__ = 'Folders'

    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    name = Column(String, nullable=False)
    parentId = Column(Integer)
    access = Column(String, nullable=False)
    syncPolicy = Column(String, nullable=False)
    downloadFilesPolicy = Column(Integer, nullable=False)
    uploadFilesPolicy = Column(Integer, nullable=False)
    publicUrl = Column(String)
    description = Column(String)
    creatorName = Column(String)
    creatorProfileUrl = Column(String)


class Group(Base):
    __tablename__ = 'Groups'

    id = Column(Integer, primary_key=True)
    remoteId = Column(Integer)
    name = Column(String)
    groupType = Column(String, nullable=False)
    status = Column(String, nullable=False)
    access = Column(String, nullable=False)
    syncPolicy = Column(String, nullable=False)
    downloadFilesPolicy = Column(Integer, nullable=False)
    uploadFilesPolicy = Column(Integer, nullable=False)
    publicUrl = Column(String)
    isOwner = Column(Boolean, nullable=False)
    isReadOnly = Column(Boolean, nullable=False)
    isPrivate = Column(Boolean, nullable=False)
    iconName = Column(String)


class Htmllocalstorage(Base):
    __tablename__ = 'HtmlLocalStorage'

    origin = Column(String, primary_key=True, nullable=False)
    key = Column(String, primary_key=True, nullable=False)
    value = Column(String)


class Importhistory(Base):
    __tablename__ = 'ImportHistory'

    path = Column(String, primary_key=True)
    importCount = Column(Integer, nullable=False)
    ignore = Column(Boolean, nullable=False)


class Notduplicate(Base):
    __tablename__ = 'NotDuplicates'

    uuid1 = Column(String, primary_key=True, nullable=False)
    uuid2 = Column(String, primary_key=True, nullable=False)


t_OAuth1AccessTokens = Table(
    'OAuth1AccessTokens', metadata,
    Column('token', String, nullable=False),
    Column('tokenSecret', String, nullable=False)
)


class Remotedocument(Base):
    __tablename__ = 'RemoteDocuments'

    documentId = Column(Integer, primary_key=True, index=True)
    remoteId = Column(Integer, primary_key=True, index=True)
    groupId = Column(Integer, nullable=False)
    status = Column(String, nullable=False)


class Remotefilehighlight(Base):
    __tablename__ = 'RemoteFileHighlights'

    uuid = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    revision = Column(Integer, nullable=False)


class Remotefilenote(Base):
    __tablename__ = 'RemoteFileNotes'

    uuid = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    revision = Column(Integer, nullable=False)


class Remotefolder(Base):
    __tablename__ = 'RemoteFolders'

    folderId = Column(Integer, primary_key=True)
    remoteId = Column(Integer)
    parentRemoteId = Column(Integer)
    groupId = Column(Integer)
    status = Column(String, nullable=False)
    version = Column(Integer, nullable=False)


class Resource(Base):
    __tablename__ = 'Resources'

    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)
    iconData = Column(LargeBinary)


t_RunsSinceLastCleanup = Table(
    'RunsSinceLastCleanup', metadata,
    Column('time', DateTime, nullable=False)
)


class Schemaversion(Base):
    __tablename__ = 'SchemaVersion'

    key = Column(String, primary_key=True)
    value = Column(Integer, nullable=False)


class Setting(Base):
    __tablename__ = 'Settings'

    key = Column(String, primary_key=True)
    value = Column(NullType)


class Stat(Base):
    __tablename__ = 'Stats'

    Action = Column(String(50), primary_key=True)
    Counter = Column(Integer, nullable=False)


t_SynchronisationToken = Table(
    'SynchronisationToken', metadata,
    Column('token', String, nullable=False),
    Column('lastSync', DateTime, nullable=False)
)


t_ZoteroLastSync = Table(
    'ZoteroLastSync', metadata,
    Column('time', Integer, nullable=False)
)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)
