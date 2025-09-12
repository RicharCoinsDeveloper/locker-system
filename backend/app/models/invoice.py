from sqlalchemy import Column, String, Numeric, DateTime, LargeBinary, ForeignKey
from . import Base

class Invoice(Base):
    __tablename__ = 'invoices'
    id = Column(String(36), primary_key=True)
    payment_id = Column(String(36), ForeignKey('payments.id'))
    cell_id = Column(String(36), ForeignKey('cells.id'))
    issued_at = Column(DateTime)
    amount = Column(Numeric(10,2))
    pdf = Column(LargeBinary)
