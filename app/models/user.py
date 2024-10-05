from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None  # Date format as string
    password: Optional[str] = None
    # phone_number: Optional[str] = None
    # last_login: Optional[str] = None  # Date format as string
    # session_token: Optional[str] = None
    # ip_address: Optional[str] = None
    # device_info: Optional[str] = None
    # updated_at: Optional[str] = None  # Date format as string

    class Config:
        json_schema_extra = {
            "example": {
                "id": "f157e3c3-657a-4132-8820-3a4a637cb281",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "123456789Abc.",
                "created_at": "2024-01-15T12:00:00Z",
                # "phone_number": "+1234567890",
                # "last_login": "2024-09-30T10:00:00Z",
                # "session_token": "abc123xyzToken",
                # "ip_address": "192.168.1.1",
                # "device_info": "Chrome on Windows 10",
                # "updated_at": "2024-09-30T11:00:00Z"
            }
        }
