from datetime import datetime

from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    curtain_barcode: str = Field(..., description="Barcode of the scanned curtain")
    visit_id: int | None = Field(None, description="Current visit ID if applicable")
    installer_id: int | None = Field(None, description="ID of the installer scanning")


class LocationDetail(BaseModel):
    hospital_name: str
    hospital_id: int
    building_name: str
    building_id: int
    floor: int
    unit_name: str
    unit_id: int
    room_name: str
    room_id: int
    track_barcode: str
    track_id: int


class TrackRecommendation(BaseModel):
    rank: int
    location: LocationDetail
    score: float = Field(..., description="Confidence score 0-100")
    reason: str = Field(..., description="Why this track is recommended")
    type_match: bool
    style_match: bool
    size_match: bool
    has_capacity: bool
    warnings: list[str] = Field(default_factory=list)


class SuggestLocationResponse(BaseModel):
    curtain_barcode: str
    curtain_status: str
    curtain_category: str
    hospital_name: str
    is_disposable: bool
    is_spare: bool
    recommendations: list[TrackRecommendation]
    total_candidates: int
    message: str


class TrackScanRequest(BaseModel):
    track_barcode: str = Field(..., description="Barcode of the scanned track")
    visit_id: int | None = None


class CurtainMatch(BaseModel):
    curtain_barcode: str
    curtain_id: int
    curtain_category: str
    curtain_type: str
    width: float
    height: float
    status: str
    score: float
    is_best_match: bool
    reason: str
    warnings: list[str] = Field(default_factory=list)


class MatchCurtainsResponse(BaseModel):
    track_barcode: str
    track_type: str
    track_length: float
    track_height: float
    hospital_name: str
    building_name: str
    floor: int
    room_name: str
    matches: list[CurtainMatch]
    total_candidates: int
    message: str


class RouteStopResponse(BaseModel):
    order: int
    hospital_name: str
    hospital_id: int
    building_name: str
    building_id: int
    floor: int
    unit_name: str
    room_name: str
    track_barcode: str
    track_id: int
    pending_curtains: int


class RouteSegmentResponse(BaseModel):
    hospital_name: str
    hospital_id: int
    stops: list[RouteStopResponse]
    total_tracks: int


class InstallerRouteResponse(BaseModel):
    installer_id: int
    route_date: str
    total_stops: int
    total_hospitals: int
    segments: list[RouteSegmentResponse]
    message: str


class CacheStatsResponse(BaseModel):
    total_keys: int
    backend: str = "in-memory"


class HealthResponse(BaseModel):
    status: str
    version: str
    db_ok: bool
    cache_ok: bool = True
    timestamp: datetime
