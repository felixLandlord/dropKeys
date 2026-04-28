from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from dropKeys.database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    google_sub = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255))
    picture = Column(String(512))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_login = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    secrets_owned = relationship("SecretMetadata", back_populates="owner", foreign_keys="SecretMetadata.owner_id")


class SecretMetadata(Base):
    __tablename__ = "secret_metadata"

    id = Column(Integer, primary_key=True)
    doc_id = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comp_key = Column(String(512), nullable=True) # The hash part of the URL for direct sharing
    created_at = Column(DateTime, default=datetime.now(timezone.utc))


    # Relationships
    owner = relationship("User", back_populates="secrets_owned", foreign_keys=[owner_id])
    recipients = relationship("SecretRecipient", back_populates="secret", cascade="all, delete-orphan")


class SecretRecipient(Base):
    __tablename__ = "secret_recipients"

    id = Column(Integer, primary_key=True)
    secret_id = Column(Integer, ForeignKey("secret_metadata.id"), nullable=False)
    recipient_email = Column(String(255), nullable=False)

    # Relationships
    secret = relationship("SecretMetadata", back_populates="recipients")