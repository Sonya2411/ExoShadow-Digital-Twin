# models.py
from pydantic import BaseModel
from typing import List

class Vector3(BaseModel):
    x: float
    y: float
    z: float

class ServoStatus(BaseModel):
    angle: float
    current: float
    temperature: float
    load: float

class TelemetryFrame(BaseModel):
    timestamp: float
    servos: List[ServoStatus]  # Было servo_angles: List[float]
    heart_rate: int
    accel_data: Vector3
    gyro_data: Vector3
    battery_voltage: float

class TelemetryIssue(BaseModel):
    time_offset: float
    type: str
    severity: int
    description: str

class TelemetryUpload(BaseModel):
    session_id: str
    data: List[TelemetryFrame]