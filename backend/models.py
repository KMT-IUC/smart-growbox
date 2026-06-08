from pydantic import BaseModel


class SensorVeri(BaseModel):
    sicaklik: float
    nem: float
    co2: int
    toprak_nemi: float
    pompa_aktif: int
    fan_aktif: int


class Olcum(SensorVeri):
    id: int
    zaman: str


class Basarili(BaseModel):
    success: bool
