from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, text
from database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    repo_name = Column(String(255), nullable=False)

    github_url = Column(Text)

    upload_path = Column(Text)

    status = Column(String(50), default="PENDING")

    created_at = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP")
    )