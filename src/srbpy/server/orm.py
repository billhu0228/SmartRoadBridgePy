from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, MetaData, Text, FLOAT, DECIMAL
from sqlalchemy.orm import relationship

Base = declarative_base()

# metadata = MetaData()
#
# BridgeTbl = Table(
#     'bridge_tbl',
#     metadata,
#     Column('name', String, primary_key=True),
# )
#
# mapper(Bridge, BridgeTbl)
#
# EITbl = Table(
#     "ei_tbl",
#     metadata,
#     Column('Name', String, primary_key=True),
#     Column('_sqx_filed', Text),
#     #Column('SQX', Text),
#     #Column('DMX', Text),
#     #Column('CG', Text),
#     #Column('HDX', Text),
# )
# mapper(Align, EITbl)
#

# class SpanTbl(Base):
#    __tablename__ = 'span_tbl'
#    Name = Column(String, primary_key=True)
#    align_name = Column(String)
#    bridge_name = Column(String)
#    Station = Column(Float)
#    Angle = Column(Float)
#
#    def __repr__(self):
#        return "<User(Name='%s', Station='%.3f', Angle='%.2f')>" % (
#            self.Name, self.Station, self.Angle)


# if __name__ == "__main__":
#     from sqlalchemy import create_engine
#
#     engine = create_engine("sqlite:///:memory:", echo=False)
#     from sqlalchemy.orm import sessionmaker
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     BridgeTbl.metadata.create_all(engine)
#     EITbl.metadata.create_all(engine)
#
#     session.add(Bridge("F1"))
#     session.commit()
#
#     session.add(Bridge("F3"))
#     session.commit()
#
#     M1K = Align(r"G:\20191213-肯尼亚高架桥施工图设计(19406)\01 前方资料\EI Data\00-MainLine\M1K-0312",name="M1K")
#     session.add(M1K)
#     session.commit()
#
#     ret = session.query(Align).all()
#
#     print(ret)
#     k = 1
#
