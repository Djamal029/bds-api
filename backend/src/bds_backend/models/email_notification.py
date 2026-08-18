"""STUB — not implemented, and out of scope for most contributors.

A queued outbound email (e.g. "your registration code", a payment
reminder) — separate from models/notification.py's in-app notification,
which is what most features should use instead. Only implement this
once actual email sending is wired up (an external provider, e.g.
SMTP or a transactional email API); until then, an in-app Notification
row is a complete substitute at no infrastructure cost.

    class EmailNotification(UUIDPrimaryKeyMixin, TimestampMixin, Base):
        __tablename__ = "email_notifications"

        recipient_email: Mapped[str] = mapped_column(String(255))
        subject: Mapped[str] = mapped_column(String(255))
        body: Mapped[str] = mapped_column(String(5000))
        status: Mapped[NotificationStatusEnum] = mapped_column(
            SAEnum(NotificationStatusEnum), default=NotificationStatusEnum.PENDING
        )
"""
