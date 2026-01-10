
from sqlalchemy import String, Text, Column, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class MX8600(Base):
    __tablename__ = 'MX8600'

    id = Column(Integer, primary_key=True)
    error_code = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    troubleshooting = Column(Text)

    def __repr__(self) -> str:
        return f"Error(id={self.id!r}, error_code={self.error_code!r}, description={self.description!r}, troubleshooting{self.troubleshooting!r}"


class MX8600S(Base):
    __tablename__ = 'MX8600S'

    id = Column(Integer, primary_key=True)
    error_code = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    troubleshooting = Column(Text)

    def __repr__(self) -> str:
        return f"Error(id={self.id!r}, error_code={self.error_code!r}, description={self.description!r}, troubleshooting{self.troubleshooting!r}"