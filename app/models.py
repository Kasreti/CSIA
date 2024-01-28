import sqlalchemy as sa
# ORM is what translates the classes defined below into tables usable by the database.
import sqlalchemy.orm as so
from app import db, app

# Each class here represents one table in the database.
class Phonology(db.Model):
    # Generates the table name.
    __tablename__ = 'Phonology'

    # Generates the columns of the table.
    phoneme: so.Mapped[str] = so.mapped_column(sa.String(7), primary_key=True)
    # The VARCHAR(5) restrictions can be seen in sa.String(5).
    ipa: so.Mapped[str] = so.mapped_column(sa.String(5), index=True)
    exists: so.Mapped[bool] = so.mapped_column()
    consonant: so.Mapped[bool] = so.mapped_column()
    romanized: so.Mapped[str] = so.mapped_column(sa.String(5), nullable=True)
    conscript: so.Mapped[str] = so.mapped_column(sa.String(5), nullable=True)

    # Adds a way for the phoneme to be represented when printed.
    def __repr__(self):
        return 'Phoneme {}'.format(self.ipa)

    # Constructor method for the column fields.
    def __init__(self, phoneme, ipa, exists, consonant, romanized=None, conscript=None):
        self.phoneme = phoneme
        self.ipa = ipa
        self.exists = exists
        self.consonant = consonant
        self.romanized = romanized
        self.conscript = conscript

class Lexicon(db.Model):
    __tablename__ = 'Lexicon'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    word: so.Mapped[str] = so.mapped_column(sa.String(50), index=True)
    pronunciation: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    conscript: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=True)
    definition: so.Mapped[str] = so.mapped_column(sa.String(255), index=True)
    partofspeech: so.Mapped[str] = so.mapped_column(nullable=True)
    wordclass: so.Mapped[int] = so.mapped_column(sa.String(1), nullable=True)
    notes: so.Mapped[str] = so.mapped_column(nullable=True)
    etymology: so.Mapped[str] = so.mapped_column(nullable=True)
    irregular: so.Mapped[bool] = so.mapped_column()
    def __repr__(self):
        return 'Word {} with definition {}'.format(self.word, self.definition)

    def __init__(self, word, pronunciation, conscript, definition, partofspeech, wordclass, notes, etymology, irregular):
        self.word = word
        self.pronunciation = pronunciation
        self.conscript = conscript
        self.wordclass = wordclass
        self.definition = definition
        self.notes = notes
        self.etymology = etymology
        self.partofspeech = partofspeech
        self.irregular = irregular

# db.Model here is inherited from the Model defined in Flask_SQLAlchemy's library.
class Texts(db.Model):
    __tablename__ = 'Texts'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(index=True)
    status: so.Mapped[str] = so.mapped_column(index=True)
    content: so.Mapped[str] = so.mapped_column()
    translation: so.Mapped[str] = so.mapped_column(nullable=True)

    def __repr__(self):
        return 'Translatable text {} with status {}'.format(self.id, self.status)

    def __init__(self, title, status, content):
        self.title = title
        self.status = status
        self.content = content

class VerbInflections(db.Model):
    __tablename__ = 'Verb Inflections'
    aspect: so.Mapped[str] = so.mapped_column(primary_key=True)
    irregular: so.Mapped[bool] = so.mapped_column()
    gloss: so.Mapped[str] = so.mapped_column()
    fs: so.Mapped[str] = so.mapped_column()
    ss: so.Mapped[str] = so.mapped_column()
    other: so.Mapped[str] = so.mapped_column()
    def __repr__(self):
        return 'Verb conjugation for aspect {}'.format(self.aspect)

    def __init__(self, aspect, irregular, gloss, fs, ss, other):
        self.aspect = aspect
        self.irregular = irregular
        self.gloss = gloss
        self.fs = fs
        self.ss = ss
        self.other = other

class NounInflections(db.Model):
    __tablename__ = 'Noun Inflections'
    number: so.Mapped[str] = so.mapped_column(primary_key=True)
    irregular: so.Mapped[bool] = so.mapped_column()
    NOM: so.Mapped[str] = so.mapped_column()
    ACC: so.Mapped[str] = so.mapped_column()
    GEN: so.Mapped[str] = so.mapped_column()
    DAT: so.Mapped[str] = so.mapped_column()
    OBL: so.Mapped[str] = so.mapped_column()
    def __repr__(self):
        return 'Noun conjugation for number {}'.format(self.number)

    def __init__(self, number, irregular, NOM, ACC, GEN, DAT, OBL):
        self.number = number
        self.irregular = irregular
        self.NOM = NOM
        self.ACC = ACC
        self.GEN = GEN
        self.DAT = DAT
        self.OBL = OBL

with app.app_context():
    db.create_all()