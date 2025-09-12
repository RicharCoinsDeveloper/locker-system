from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from . import Base

class QRCode(Base):
    __tablename__ = 'qrcodes'
    id = Column(String(36), primary_key=True)
    reservation_id = Column(String(36), ForeignKey('reservations.id'))
    code = Column(Text)
    generated_at = Column(DateTime)
    expires_at = Column(DateTime)
    status = Column(String(20))
