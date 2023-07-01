from dataclasses import dataclass
from uuid import UUID

from phonenumber_field.modelfields import PhoneNumberField


@dataclass
class CustomerProfileRequest:
    id: UUID
    firstName: str
    lastName: str
    dateOfBirth: str
    phoneNumber: PhoneNumberField
