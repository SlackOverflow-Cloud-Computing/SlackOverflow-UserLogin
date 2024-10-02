from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from datetime import datetime

"""class CourseSection(BaseModel):
    course_id: Optional[int] = None
    course_name: Optional[str] = None
    uuid: Optional[str] = None
    created_at: Optional[str] = None
    course_code: Optional[str] = None
    sis_course_id: Optional[str] = None
    course_no: Optional[str] = None
    section: Optional[str] = None
    course_year: Optional[str] = None
    semester: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "course_id": 204283,
                "course_name": "COMSW4153_001_2024_3 - Cloud Computing",
                "uuid": "3jHCxUV0ck9Z8TF1sZeI8WTx47olDGkX1YPL3USM",
                "created_at": "2024-04-05T00:58:50Z",
                "course_code": "COMSW4153_001_2024_3 - Cloud Computing",
                "sis_course_id": "COMSW4153_001_2024_3",
                "course_no": "COMSW4153",
                "section": "001",
                "course_year": "2024",
                "semester": "3"
            }
        }"""


class UserLogin(BaseModel):
    user_id: Optional[str] = None
    user_name: Optional[str] = None
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
                "user_id": "f157e3c3-657a-4132-8820-3a4a637cb281",
                "user_name": "johndoe",
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
