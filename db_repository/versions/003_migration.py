from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
eve = Table('eve', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('level', String(length=140)),
    Column('type', String(length=140)),
    Column('name', String(length=140)),
    Column('time', String(length=140)),
    Column('timestamp', DateTime),
    Column('sheet_id', Integer),
)

sheet = Table('sheet', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('level', Integer),
    Column('name', String(length=140)),
    Column('timestamp', DateTime),
)

vul = Table('vul', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('level', String(length=140)),
    Column('type', String(length=140)),
    Column('name', String(length=140)),
    Column('time', String(length=140)),
    Column('timestamp', DateTime),
    Column('sheet_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['eve'].create()
    post_meta.tables['sheet'].create()
    post_meta.tables['vul'].columns['sheet_id'].create()
    post_meta.tables['vul'].columns['time'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['eve'].drop()
    post_meta.tables['sheet'].drop()
    post_meta.tables['vul'].columns['sheet_id'].drop()
    post_meta.tables['vul'].columns['time'].drop()
