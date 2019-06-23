import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, func, Date, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base

from membership.models import Member

Base = declarative_base()


class MessageTemplate(enum.Enum):
    LABACCESS_REMINDER = 'labaccess_reminder'
    LOGIN_LINK = 'login_link'
    NEW_MEMBER = 'new_member'
    RECEIPT = 'receipt'
    ADD_LABACCESS_TIME = 'add_labaccess_time'
    ADD_MEMBERSHIP_TIME = 'add_membership_time'


class Message(Base):
    
    QUEUED = 'queued'
    SENT = 'sent'
    FAILED = 'failed'
    
    __tablename__ = 'message'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    subject = Column(Text, nullable=False)
    body = Column(Text)
    member_id = Column(Integer, ForeignKey(Member.member_id))
    recipient = Column(String(255))
    date_sent = Column(Date)
    status = Column(Enum(QUEUED, SENT, FAILED), nullable=False)
    template = Column(String(120), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f'Message(recipient_id={self.id}, subject={self.subject}, member_id={self.member_id})'
