from abc import ABC, abstractmethod
from typing import Any

import structlog

logger = structlog.get_logger()


class AbstractNotificationSender(ABC):
    """Abstract interface to allow real SMS/Email providers integrations later."""

    @abstractmethod
    async def send_email(self, recipient_email: str, subject: str, body: str) -> None:
        pass

    @abstractmethod
    async def send_sms(self, recipient_phone: str, message: str) -> None:
        pass


class LogNotificationSender(AbstractNotificationSender):
    """Concrete mock notification sender that writes structured layouts to logs."""

    async def send_email(self, recipient_email: str, subject: str, body: str) -> None:
        logger.info(
            "MOCK EMAIL SENT",
            to=recipient_email,
            subject=subject,
            body=body,
        )

    async def send_sms(self, recipient_phone: str, message: str) -> None:
        logger.info(
            "MOCK SMS SENT",
            to=recipient_phone,
            message=message,
        )


class NotificationService:
    """Orchestrates transactional email/SMS notifications using production-ready templates."""

    def __init__(self, sender: AbstractNotificationSender | None = None) -> None:
        self.sender = sender or LogNotificationSender()
        self.hotel_name = "Grand Hospitality Resort"

    async def send_reservation_confirmation(
        self,
        guest_name: str,
        guest_email: str,
        guest_phone: str | None,
        reservation_details: dict[str, Any],
    ) -> None:
        """Sends booking confirmations containing stay details."""
        subject = f"Booking Confirmed: Your Stay at {self.hotel_name}"
        body = (
            f"Dear {guest_name},\n\n"
            f"Thank you for choosing {self.hotel_name}! We are delighted to confirm your reservation.\n\n"
            f"Reservation ID: {reservation_details['reservation_id']}\n"
            f"Room Category: {reservation_details['category_name']}\n"
            f"Check-In Date: {reservation_details['check_in_date']}\n"
            f"Check-Out Date: {reservation_details['check_out_date']}\n"
            f"Total Price: ${reservation_details['total_cost']:.2f} (including taxes)\n\n"
            f"We look forward to welcoming you soon!\n\n"
            f"Best regards,\n"
            f"The Team at {self.hotel_name}"
        )
        await self.sender.send_email(guest_email, subject, body)
        if guest_phone:
            sms = f"Hi {guest_name}, your booking at {self.hotel_name} is confirmed! Res ID: {reservation_details['reservation_id']}. Dates: {reservation_details['check_in_date']} to {reservation_details['check_out_date']}."
            await self.sender.send_sms(guest_phone, sms)

    async def send_reservation_reminder(
        self,
        guest_name: str,
        guest_email: str,
        guest_phone: str | None,
        reservation_details: dict[str, Any],
    ) -> None:
        """Sends reminder notifications 24 hours prior to check-in."""
        subject = f"Upcoming Stay Reminder: {self.hotel_name}"
        body = (
            f"Dear {guest_name},\n\n"
            f"This is a friendly reminder that your stay at {self.hotel_name} starts tomorrow!\n\n"
            f"Reservation ID: {reservation_details['reservation_id']}\n"
            f"Check-In Date: {reservation_details['check_in_date']} (from 3:00 PM)\n"
            f"Check-Out Date: {reservation_details['check_out_date']}\n"
            f"Assigned Room: {reservation_details.get('room_number') or 'Assigned at Check-In'}\n\n"
            f"Safe travels, and see you soon!\n\n"
            f"Best regards,\n"
            f"The Team at {self.hotel_name}"
        )
        await self.sender.send_email(guest_email, subject, body)
        if guest_phone:
            sms = f"Hi {guest_name}, we look forward to seeing you tomorrow at {self.hotel_name}! Check-in starts at 3 PM. Res ID: {reservation_details['reservation_id']}."
            await self.sender.send_sms(guest_phone, sms)

    async def send_reservation_cancellation(
        self,
        guest_name: str,
        guest_email: str,
        guest_phone: str | None,
        reservation_details: dict[str, Any],
        reason: str,
    ) -> None:
        """Sends cancellation confirmations."""
        subject = (
            f"Booking Cancelled: Reservation #{reservation_details['reservation_id']}"
        )
        body = (
            f"Dear {guest_name},\n\n"
            f"As requested, your reservation at {self.hotel_name} has been cancelled.\n\n"
            f"Reservation ID: {reservation_details['reservation_id']}\n"
            f"Cancellation Reason: {reason}\n"
            f"Penalty Charged: ${reservation_details.get('penalty', 0.0):.2f}\n\n"
            f"We hope to have the opportunity to host you in the future.\n\n"
            f"Best regards,\n"
            f"The Team at {self.hotel_name}"
        )
        await self.sender.send_email(guest_email, subject, body)
        if guest_phone:
            sms = f"Hi {guest_name}, your booking Res ID: {reservation_details['reservation_id']} at {self.hotel_name} has been cancelled."
            await self.sender.send_sms(guest_phone, sms)

    async def send_reservation_modification(
        self,
        guest_name: str,
        guest_email: str,
        guest_phone: str | None,
        reservation_details: dict[str, Any],
        old_dates: str,
    ) -> None:
        """Sends modification updates."""
        subject = (
            f"Booking Modified: Reservation #{reservation_details['reservation_id']}"
        )
        body = (
            f"Dear {guest_name},\n\n"
            f"Your reservation at {self.hotel_name} has been successfully modified.\n\n"
            f"Reservation ID: {reservation_details['reservation_id']}\n"
            f"Previous Dates: {old_dates}\n"
            f"New Check-In Date: {reservation_details['check_in_date']}\n"
            f"New Check-Out Date: {reservation_details['check_out_date']}\n"
            f"New Total Cost: ${reservation_details['total_cost']:.2f}\n\n"
            f"Thank you for your business!\n\n"
            f"Best regards,\n"
            f"The Team at {self.hotel_name}"
        )
        await self.sender.send_email(guest_email, subject, body)
        if guest_phone:
            sms = f"Hi {guest_name}, your booking Res ID: {reservation_details['reservation_id']} at {self.hotel_name} was modified to {reservation_details['check_in_date']} - {reservation_details['check_out_date']}."
            await self.sender.send_sms(guest_phone, sms)

    async def send_check_in_confirmation(
        self,
        guest_name: str,
        guest_email: str,
        guest_phone: str | None,
        reservation_details: dict[str, Any],
    ) -> None:
        """Sends confirmations upon check-in."""
        subject = f"Welcome to {self.hotel_name}! You are Checked In"
        body = (
            f"Dear {guest_name},\n\n"
            f"Welcome to {self.hotel_name}! You are now checked in.\n\n"
            f"Reservation ID: {reservation_details['reservation_id']}\n"
            f"Room Number: {reservation_details['room_number']}\n"
            f"Check-Out Date: {reservation_details['check_out_date']}\n\n"
            f"If you need anything during your stay, please contact our Guest Concierge.\n\n"
            f"Enjoy your stay!\n\n"
            f"Best regards,\n"
            f"The Team at {self.hotel_name}"
        )
        await self.sender.send_email(guest_email, subject, body)
        if guest_phone:
            sms = f"Welcome {guest_name}! You are checked in to room {reservation_details['room_number']} at {self.hotel_name}."
            await self.sender.send_sms(guest_phone, sms)

    async def send_check_out_confirmation(
        self,
        guest_name: str,
        guest_email: str,
        guest_phone: str | None,
        reservation_details: dict[str, Any],
    ) -> None:
        """Sends check-out confirmation invoice."""
        subject = f"Thank you for staying at {self.hotel_name}! Check-Out Confirmed"
        body = (
            f"Dear {guest_name},\n\n"
            f"Thank you for staying at {self.hotel_name}! We hope you had an exceptional visit.\n\n"
            f"Reservation ID: {reservation_details['reservation_id']}\n"
            f"Check-Out Date: {reservation_details['check_out_date']}\n"
            f"Total Billed: ${reservation_details['total_cost']:.2f}\n\n"
            f"We hope to welcome you back soon!\n\n"
            f"Best regards,\n"
            f"The Team at {self.hotel_name}"
        )
        await self.sender.send_email(guest_email, subject, body)
        if guest_phone:
            sms = f"Hi {guest_name}, thank you for staying at {self.hotel_name}! Your check-out has been processed."
            await self.sender.send_sms(guest_phone, sms)

    async def send_ai_concierge_notification(
        self, guest_name: str, guest_email: str, guest_phone: str | None, message: str
    ) -> None:
        """Sends automated concierge notifications (booking updates or requests)."""
        subject = "HospitalityAI Concierge: Update for your stay"
        body = (
            f"Dear {guest_name},\n\n"
            f"We have an update from our AI Concierge team:\n\n"
            f"{message}\n\n"
            f"Please let us know if you have any questions.\n\n"
            f"Best regards,\n"
            f"The Team at {self.hotel_name}"
        )
        await self.sender.send_email(guest_email, subject, body)
        if guest_phone:
            await self.sender.send_sms(guest_phone, f"Concierge: {message}")


# Global notification service
notification_service = NotificationService()

__all__ = [
    "AbstractNotificationSender",
    "LogNotificationSender",
    "NotificationService",
    "notification_service",
]
