"""
SQLAlchemy models reflecting the UATAI Automation Hospital SQL Server database schema.

Table names and column names match the production database exactly.
"""

from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


# ═══════════════════════════════════════════════════════════════════════════════
# LOOKUP / REFERENCE TABLES
# ═══════════════════════════════════════════════════════════════════════════════


class CurtType(Base):
    __tablename__ = "Curt_Type"

    Curt_TypeID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class CurtPatterns(Base):
    __tablename__ = "Curt_Patterns"

    PatternID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    ImageURL: Mapped[str | None] = mapped_column(Text, nullable=True)


class CurtWidth(Base):
    __tablename__ = "Curt_Width"

    WidthID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class CurtHeight(Base):
    __tablename__ = "Curt_Height"

    HeightID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class CurtGrommets(Base):
    __tablename__ = "Curt_Grommets"

    GoormateID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class CurtStyle(Base):
    __tablename__ = "Curt_Style"

    Curt_StyleID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class CurtColor(Base):
    __tablename__ = "Curt_Color"

    ColorID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class CurtStatus(Base):
    __tablename__ = "Curt_Status"

    StatusID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class UnitLookup(Base):
    __tablename__ = "Units"

    UnitId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class LocationLookup(Base):
    __tablename__ = "Location"

    LocationId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class TrackType(Base):
    __tablename__ = "TrackType"

    TrackTypeId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class TrackLocation(Base):
    __tablename__ = "TrackLocation"

    TrackLocationId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str | None] = mapped_column(String(100))
    SortIndex: Mapped[int] = mapped_column(Integer)
    Enabled: Mapped[bool] = mapped_column(Boolean)


class MeshColor(Base):
    __tablename__ = "Mesh_Color"

    ColorId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class MeshSize(Base):
    __tablename__ = "Mesh_Size"

    MeshSizeId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class MeshType(Base):
    __tablename__ = "Mesh_Type"

    MeshTypeId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class HospRegion(Base):
    __tablename__ = "Hosp_Regions"

    RegionId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class InstallerTypeLookup(Base):
    __tablename__ = "Installertype"

    InstallerTypeID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class MaintenanceType(Base):
    __tablename__ = "MaintenanceType"

    MaintenanceTypeId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(String(50))
    Description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    SortIndex: Mapped[int] = mapped_column(Integer, default=0)
    IsActive: Mapped[bool] = mapped_column(Boolean, default=True)


class ScheduleTerm(Base):
    __tablename__ = "ScheduleTerm"

    ScheduleTermId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(String(50))
    FrequencyMonths: Mapped[int] = mapped_column(Integer)
    FrequencyDays: Mapped[int | None] = mapped_column(Integer, nullable=True)
    SortIndex: Mapped[int] = mapped_column(Integer, default=0)
    IsActive: Mapped[bool] = mapped_column(Boolean, default=True)


class PricingType(Base):
    __tablename__ = "PricingType"

    PricingTypeID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(String(100))
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    IsWashingPrice: Mapped[bool] = mapped_column(Boolean, default=False)


class BagLocationType(Base):
    __tablename__ = "BagLocationType"

    LocationTypeID: Mapped[int] = mapped_column(Integer, primary_key=True)
    LocationTypeName: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class WeekDays(Base):
    __tablename__ = "WeekDays"

    DayId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str] = mapped_column(String(20))
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class DropDownComments(Base):
    __tablename__ = "DropDownComments"

    CommentsId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    Status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class LocationStatus(Base):
    __tablename__ = "LocationStatus"

    LocationStatusID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    LocationStatus_: Mapped[str | None] = mapped_column("LocationStatus", String(50), nullable=True)
    UpdatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[int] = mapped_column(Integer)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)


class AppVersion(Base):
    __tablename__ = "AppVersion"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    VersionNo: Mapped[str] = mapped_column(String(10))
    IsActive: Mapped[bool] = mapped_column(Boolean)


class CountryImages(Base):
    __tablename__ = "CountryImages"

    CountryName: Mapped[str | None] = mapped_column(String(50), primary_key=True)
    CountryImage: Mapped[str | None] = mapped_column(String(50), nullable=True)


class TblCountry(Base):
    __tablename__ = "tblcountry"

    Code: Mapped[int | None] = mapped_column(Integer, primary_key=True)
    CountryDescription: Mapped[str | None] = mapped_column(String(50), nullable=True)
    enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    sortindex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    CountryCode: Mapped[str | None] = mapped_column(String(50), nullable=True)


class TblStateCountry(Base):
    __tablename__ = "tblStateCountry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CountryCode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    StateName: Mapped[str | None] = mapped_column(String(100), nullable=True)
    enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    sortindex: Mapped[int | None] = mapped_column(Integer, nullable=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CORE ENTITY TABLES
# ═══════════════════════════════════════════════════════════════════════════════


class Hospital(Base):
    __tablename__ = "Hospital"

    HID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    City: Mapped[str | None] = mapped_column(String(50), nullable=True)
    StateId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Zip: Mapped[str | None] = mapped_column(String(12), nullable=True)
    CountryCode: Mapped[str | None] = mapped_column(String(3), nullable=True)
    Phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    Extension: Mapped[str | None] = mapped_column(String(4), nullable=True)
    Fax: Mapped[str | None] = mapped_column(String(12), nullable=True)
    Email: Mapped[str | None] = mapped_column(String(50), nullable=True)
    EVS_Name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    EVS_Phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    EVS_Extension: Mapped[str | None] = mapped_column(String(4), nullable=True)
    EVS_Email: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    Comments: Mapped[str | None] = mapped_column(String(200), nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    AccountNumber: Mapped[int | None] = mapped_column(Integer, nullable=True)
    VisitDay: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Maintenance: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contactPer_Name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    contactPer_Phone: Mapped[str | None] = mapped_column(String(15), nullable=True)
    contactPer_Extension: Mapped[str | None] = mapped_column(String(4), nullable=True)
    contactPer_Email: Mapped[str | None] = mapped_column(String(50), nullable=True)
    EVS_Cell: Mapped[str | None] = mapped_column(String(12), nullable=True)
    contactPer_Cell: Mapped[str | None] = mapped_column(String(12), nullable=True)
    Latitude: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Longitude: Mapped[str | None] = mapped_column(String(50), nullable=True)
    PrimaryTitle: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SecondaryTitle: Mapped[str | None] = mapped_column(String(50), nullable=True)
    RegionId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    IsManufecturingService: Mapped[bool] = mapped_column(Boolean, default=False)
    isTempStorage: Mapped[bool] = mapped_column(Boolean, default=False)
    IsHospitalOwnedCurtains: Mapped[bool] = mapped_column(Boolean, default=False)
    HasAIAutomationHospitalSpares: Mapped[bool] = mapped_column(Boolean, default=False)
    HasDisposable: Mapped[bool] = mapped_column(Boolean, default=False)

    buildings: Mapped[list["HospBuilding"]] = relationship(back_populates="hospital")
    curtains: Mapped[list["HospCurtain"]] = relationship(back_populates="hospital")


class HospBuilding(Base):
    __tablename__ = "Hosp_Building"

    BID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HID: Mapped[int | None] = mapped_column(ForeignKey("Hospital.HID"), nullable=True)
    Hosp_BuildingID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    TotalFloor: Mapped[int | None] = mapped_column(Integer, nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Comment: Mapped[str | None] = mapped_column(String(200), nullable=True)
    IsLocked: Mapped[bool] = mapped_column(Boolean, default=False)
    ResetDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    hospital: Mapped["Hospital"] = relationship(back_populates="buildings")
    units: Mapped[list["HospUnit"]] = relationship(back_populates="building")


class HospUnit(Base):
    __tablename__ = "Hosp_Unit"

    HUID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    BID: Mapped[int | None] = mapped_column(ForeignKey("Hosp_Building.BID"), nullable=True)
    UnitID: Mapped[int | None] = mapped_column(ForeignKey("Units.UnitId"), nullable=True)
    Hosp_UnitID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Floor: Mapped[int | None] = mapped_column(Integer, nullable=True)
    LocationId: Mapped[int | None] = mapped_column(ForeignKey("Location.LocationId"), nullable=True)
    CellingHeight: Mapped[str | None] = mapped_column(String(15), nullable=True)
    SparesRequired: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    Style: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Spares: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Pattern: Mapped[str | None] = mapped_column(String(50), nullable=True)
    PatternImgURL: Mapped[str | None] = mapped_column(String(100), nullable=True)
    Schudule: Mapped[int | None] = mapped_column(Integer, nullable=True)
    SchuduleRequested: Mapped[str | None] = mapped_column(String(200), nullable=True)
    TimeOfWork: Mapped[int | None] = mapped_column(Integer, nullable=True)
    TimeOfWorkRequested: Mapped[str | None] = mapped_column(String(200), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Comments: Mapped[str | None] = mapped_column(String(200), nullable=True)
    PatternId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    IsLocked: Mapped[bool] = mapped_column(Boolean, default=False)
    ResetDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    building: Mapped["HospBuilding"] = relationship(back_populates="units")
    unit_ref: Mapped["UnitLookup | None"] = relationship(foreign_keys=[UnitID])
    location_ref: Mapped["LocationLookup | None"] = relationship(foreign_keys=[LocationId])
    rooms: Mapped[list["HospBuildingRoom"]] = relationship(back_populates="unit")
    tracks: Mapped[list["HospTrack"]] = relationship(
        back_populates="unit", foreign_keys="HospTrack.HUID"
    )

    @property
    def unit_name(self) -> str:
        if self.unit_ref and self.unit_ref.Name:
            return self.unit_ref.Name
        return f"Unit {self.HUID}"


class HospBuildingRoom(Base):
    __tablename__ = "Hosp_Building_Rooms"

    RoomID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HUID: Mapped[int | None] = mapped_column(ForeignKey("Hosp_Unit.HUID"), nullable=True)
    RoomNumber: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Comment: Mapped[str | None] = mapped_column(String(200), nullable=True)
    IsLocked: Mapped[bool] = mapped_column(Boolean, default=False)
    ResetDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    unit: Mapped["HospUnit"] = relationship(back_populates="rooms")
    tracks: Mapped[list["HospTrack"]] = relationship(back_populates="room")


class HospTrack(Base):
    __tablename__ = "Hosp_Track"

    HospTrackId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HUID: Mapped[int | None] = mapped_column(ForeignKey("Hosp_Unit.HUID"), nullable=True)
    Hosp_TrackID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    TrackTypeID: Mapped[int | None] = mapped_column(ForeignKey("TrackType.TrackTypeId"), nullable=True)
    RoomId: Mapped[int | None] = mapped_column(ForeignKey("Hosp_Building_Rooms.RoomID"), nullable=True)
    Location: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Height: Mapped[str | None] = mapped_column(String(10), nullable=True)
    Length: Mapped[str | None] = mapped_column(String(10), nullable=True)
    TrackBarCode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    CurtainStyle: Mapped[int | None] = mapped_column(Integer, nullable=True)
    NumberOfCurtain: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Curt_TypeId: Mapped[int | None] = mapped_column(ForeignKey("Curt_Type.Curt_TypeID"), nullable=True)
    SortIndex: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Comment: Mapped[str | None] = mapped_column(String(200), nullable=True)
    Track_status: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Status_Date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Due_Date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    NumberOfSpares: Mapped[int | None] = mapped_column(Integer, nullable=True)
    NumberOfDisposables: Mapped[int | None] = mapped_column(Integer, default=0)
    IsLocked: Mapped[bool] = mapped_column(Boolean, default=False)
    ResetDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    NumberOfSnapMesh: Mapped[int | None] = mapped_column(Integer, default=0)

    unit: Mapped["HospUnit"] = relationship(back_populates="tracks", foreign_keys=[HUID])
    room: Mapped["HospBuildingRoom | None"] = relationship(back_populates="tracks")
    track_type_ref: Mapped["TrackType | None"] = relationship(foreign_keys=[TrackTypeID])
    curtain_type_ref: Mapped["CurtType | None"] = relationship(foreign_keys=[Curt_TypeId])

    @property
    def length_value(self) -> float | None:
        if self.Length:
            try:
                return float(self.Length.replace('"', "").replace("'", "").strip())
            except (ValueError, AttributeError):
                return None
        return None

    @property
    def height_value(self) -> float | None:
        if self.Height:
            try:
                return float(self.Height.replace('"', "").replace("'", "").strip())
            except (ValueError, AttributeError):
                return None
        return None


class HospCurtain(Base):
    __tablename__ = "Hosp_Curtains"

    CID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HID: Mapped[int] = mapped_column(ForeignKey("Hospital.HID"))
    Hosp_CurtID: Mapped[int] = mapped_column(Integer)
    CurtBarCode: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)
    PatternID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Curt_TypeID: Mapped[int | None] = mapped_column(ForeignKey("Curt_Type.Curt_TypeID"), nullable=True)
    TypeCount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    GrommetID: Mapped[int | None] = mapped_column(ForeignKey("Curt_Grommets.GoormateID"), nullable=True)
    WidthId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    HeightId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Mesh: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    MeshSizeID: Mapped[int | None] = mapped_column(ForeignKey("Mesh_Size.MeshSizeId"), nullable=True)
    MeshTypeID: Mapped[int | None] = mapped_column(ForeignKey("Mesh_Type.MeshTypeId"), nullable=True)
    MeshColorID: Mapped[int | None] = mapped_column(ForeignKey("Mesh_Color.ColorId"), nullable=True)
    Weight: Mapped[float | None] = mapped_column(Float, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    Comment: Mapped[str | None] = mapped_column(String(200), nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    BuildingId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    UnitStyle: Mapped[int | None] = mapped_column(Integer, nullable=True)
    NoofPannels: Mapped[int | None] = mapped_column(Integer, default=0)
    SnapMesh: Mapped[int] = mapped_column(Integer, default=0)
    SONumber: Mapped[str | None] = mapped_column(String(50), nullable=True)
    LotNumber: Mapped[str | None] = mapped_column(String(50), nullable=True)
    IsManufecturing: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    hospital: Mapped["Hospital"] = relationship(back_populates="curtains")
    curtain_type_ref: Mapped["CurtType | None"] = relationship(foreign_keys=[Curt_TypeID])
    grommet_ref: Mapped["CurtGrommets | None"] = relationship(foreign_keys=[GrommetID])
    mesh_size_ref: Mapped["MeshSize | None"] = relationship(foreign_keys=[MeshSizeID])
    mesh_type_ref: Mapped["MeshType | None"] = relationship(foreign_keys=[MeshTypeID])
    mesh_color_ref: Mapped["MeshColor | None"] = relationship(foreign_keys=[MeshColorID])

    @property
    def barcode_str(self) -> str:
        return str(self.CurtBarCode) if self.CurtBarCode is not None else ""


class CurPatternImage(Base):
    __tablename__ = "Cur_PatternImage"

    ColorImageID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    PatternID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ColorID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ImageUrl: Mapped[str | None] = mapped_column(Text, nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class CurtainUnit(Base):
    __tablename__ = "Curtain_Units"

    CurtainUnitId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    CID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    HUID: Mapped[int | None] = mapped_column(Integer, nullable=True)


class HospPatternLibrary(Base):
    __tablename__ = "Hosp_PatternLibrary"

    HPID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HospitalID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    PatternID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Comment: Mapped[str | None] = mapped_column(String(200), nullable=True)


class UnitSettings(Base):
    __tablename__ = "UnitSettings"

    UnitSettingsId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HUID: Mapped[int] = mapped_column(ForeignKey("Hosp_Unit.HUID"), unique=True)
    HospitalId: Mapped[int] = mapped_column(ForeignKey("Hospital.HID"))
    IsHospitalOwnedCurtains: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    HasAIAutomationHospitalSpares: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    HasDisposable: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    CreatedBy: Mapped[str] = mapped_column(String(50))
    CreatedOn: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedOn: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class DisposableCurtainGrouped(Base):
    __tablename__ = "DisposableCurtainGrouped"

    GroupId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    First: Mapped[str] = mapped_column(String(50))
    Last: Mapped[str] = mapped_column(String(50))
    PatternID: Mapped[int] = mapped_column(Integer)
    WidthId: Mapped[int] = mapped_column(Integer)
    HeightId: Mapped[int] = mapped_column(Integer)
    HName: Mapped[str | None] = mapped_column(String(100), nullable=True)
    CurtTypeId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    CurtStatusId: Mapped[int] = mapped_column(Integer)
    HID: Mapped[int] = mapped_column(Integer)
    Count: Mapped[int] = mapped_column(Integer)
    LastRefreshed: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE / OPERATIONAL TABLES
# ═══════════════════════════════════════════════════════════════════════════════


class TrackCurtainService(Base):
    __tablename__ = "Track_Curtain_Services"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    CurBarCode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    TrackBarCode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    CurStatusID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CleanedAndR_Date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CleanedAndR_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Deleiverd_by: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Deleiverd_Date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Installed_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Installed_Date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SoiledScanedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    SoiledScanedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ScheduledDeliveryDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ServiceType: Mapped[str | None] = mapped_column(String(20), nullable=True)
    IsRewash: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    RewashDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    IsRemesh: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    RemeshDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Rewash_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    remesh_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    oldRewash: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class Visit(Base):
    __tablename__ = "Visit"

    VisitId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    VisitDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    NoOfCurtains: Mapped[int | None] = mapped_column(Integer, nullable=True)
    serviceType: Mapped[str | None] = mapped_column(String(30), nullable=True)
    VisitedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Comment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    VisitStatus: Mapped[int | None] = mapped_column(Integer, nullable=True)
    InstallerComment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ClientName: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ClientTitle: Mapped[str | None] = mapped_column(String(50), nullable=True)
    IsApprovalRequired: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    ClientSignature: Mapped[str | None] = mapped_column(Text, nullable=True)
    IsEdit: Mapped[bool] = mapped_column(Boolean, default=False)
    ClientIdPhoto: Mapped[str | None] = mapped_column(Text, nullable=True)
    StartTime: Mapped[str | None] = mapped_column(String(20), nullable=True)
    EndTime: Mapped[str | None] = mapped_column(String(20), nullable=True)
    VisitNotes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    NoOfBags: Mapped[int | None] = mapped_column(Integer, nullable=True)
    VisitType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    IsTempSotrage: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    details: Mapped[list["VisitDetail"]] = relationship(back_populates="visit")
    bags: Mapped[list["VisitBag"]] = relationship(back_populates="visit")


class VisitDetail(Base):
    __tablename__ = "VisitDetail"

    VisitId: Mapped[int] = mapped_column(ForeignKey("Visit.VisitId"), primary_key=True)
    CurtBarCode: Mapped[int] = mapped_column(Integer, primary_key=True)
    TrackBarCode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    DeliveryDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    BagID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    BagBarcode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Width: Mapped[int | None] = mapped_column(Integer, nullable=True)

    visit: Mapped["Visit"] = relationship(back_populates="details")


# ── Bag Tables ────────────────────────────────────────────────────────────────


class Bag(Base):
    __tablename__ = "Bag"

    BagID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    BagBarcode: Mapped[str] = mapped_column(String(50), unique=True)
    HID: Mapped[int] = mapped_column(Integer)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ClosedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Status: Mapped[int] = mapped_column(Integer, default=0)
    Hosp_BagId: Mapped[int] = mapped_column(BigInteger)
    UpdatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)


class CurtainBag(Base):
    __tablename__ = "CurtainBag"

    CurtainBagID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    CID: Mapped[int] = mapped_column(Integer)
    CurtBarCode: Mapped[int] = mapped_column(Integer)
    BagID: Mapped[int] = mapped_column(Integer)
    AddedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    AddedBy: Mapped[str] = mapped_column(String(50))
    UpdatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CurtainStatus: Mapped[int | None] = mapped_column(Integer, nullable=True)


class VisitBag(Base):
    __tablename__ = "VisitBag"

    VisitBagID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    VisitID: Mapped[int | None] = mapped_column(ForeignKey("Visit.VisitId"), nullable=True)
    BagID: Mapped[int] = mapped_column(Integer)
    NoofCurtain: Mapped[int] = mapped_column(Integer)
    HID: Mapped[int] = mapped_column(Integer)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)

    visit: Mapped["Visit | None"] = relationship(back_populates="bags")


class VisitBagScan(Base):
    __tablename__ = "VisitBagScan"

    ScanID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    VisitID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    BagID: Mapped[int] = mapped_column(Integer)
    ObjectId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ScanDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ScannedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    HID: Mapped[int] = mapped_column(Integer)
    ObjectLocation: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ObjectLocationBarcode: Mapped[str] = mapped_column(String(50))
    FromLocation: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ToLocation: Mapped[int | None] = mapped_column(Integer, nullable=True)


class VisitBagLocation(Base):
    __tablename__ = "VisitBagLocation"

    VisitBagLocationId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    VisitId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    TempStorageId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ParentTempStorageId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    DropDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    DropbyUserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class BagReassignmentHistory(Base):
    __tablename__ = "BagReassignmentHistory"

    BagReassignmentId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    BagId: Mapped[int] = mapped_column(Integer)
    OldVisitId: Mapped[int] = mapped_column(Integer)
    NewVisitId: Mapped[int] = mapped_column(Integer)
    ReassignedByUserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ReassignedDateTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Comments: Mapped[str | None] = mapped_column(Text, nullable=True)


# ═══════════════════════════════════════════════════════════════════════════════
# USER / ROLE TABLES
# ═══════════════════════════════════════════════════════════════════════════════


class AIAutomationHospitalUser(Base):
    __tablename__ = "AI_AUTOMATION_HOSPITAL_USERS"

    USER_ID: Mapped[str] = mapped_column(String(50), primary_key=True, unique=True)
    FIRST_NAME: Mapped[str | None] = mapped_column(String(20), nullable=True)
    LAST_NAME: Mapped[str | None] = mapped_column(String(20), nullable=True)
    Email: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Phonenumber: Mapped[str | None] = mapped_column(String(15), nullable=True)
    PhoneExtension: Mapped[str | None] = mapped_column(String(5), nullable=True)
    ENABLED: Mapped[bool | None] = mapped_column(Boolean, default=True)
    DATE_UPDATED: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UPDATED_USER_ID: Mapped[str | None] = mapped_column(String(50), nullable=True)
    date_created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UserType: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ResetPass: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    InstallerType: Mapped[int | None] = mapped_column(Integer, nullable=True)
    MobilePass: Mapped[str | None] = mapped_column(String(50), nullable=True)


class AIAutomationHospitalRoleGroup(Base):
    __tablename__ = "AI_AUTOMATION_HOSPITALRoleGroups"

    RoleGroupId: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    RoleGroupName: Mapped[str | None] = mapped_column(String(256), nullable=True)


class AIAutomationHospitalRoleGroupRole(Base):
    __tablename__ = "AI_AUTOMATION_HOSPITALRoleGroupRoles"

    RoleGroupId: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("AI AUTOMATION HOSPITALRoleGroups.RoleGroupId"), primary_key=True
    )
    RoleName: Mapped[str] = mapped_column(String(256), primary_key=True)


class AIAutomationHospitalRoleGroupUser(Base):
    __tablename__ = "AI_AUTOMATION_HOSPITALRoleGroupUsers"

    RoleGroupId: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("AI AUTOMATION HOSPITALRoleGroups.RoleGroupId"), primary_key=True
    )
    USER_ID: Mapped[str] = mapped_column(
        String(50), ForeignKey("AI AUTOMATION HOSPITAL_USERS.USER_ID"), primary_key=True
    )


class UserBelongsToHospital(Base):
    __tablename__ = "UserBelongsToHospital"

    RowID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    USER_ID: Mapped[str | None] = mapped_column(String(50), nullable=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)


class UserBelongsToRegion(Base):
    __tablename__ = "UserBelongsToRegion"

    HospRegionId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    USER_ID: Mapped[str | None] = mapped_column(String(50), nullable=True)
    RegionId: Mapped[int | None] = mapped_column(Integer, nullable=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SCHEDULING TABLES
# ═══════════════════════════════════════════════════════════════════════════════


class HospitalSchedule(Base):
    __tablename__ = "HospitalSchedule"

    HospitalScheduleId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HospitalId: Mapped[int] = mapped_column(Integer)
    ScheduleTermId: Mapped[int] = mapped_column(Integer)
    MaintenanceTypeId: Mapped[int] = mapped_column(Integer)
    PeriodStartDate: Mapped[datetime] = mapped_column(DateTime)
    PeriodEndDate: Mapped[datetime] = mapped_column(DateTime)
    StartMonth: Mapped[str | None] = mapped_column(String(50), nullable=True)
    EndMonth: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Status: Mapped[str] = mapped_column(String(20), default="Running")
    Notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    IsDelete: Mapped[bool] = mapped_column(Boolean, default=False)
    CreatedBy: Mapped[str] = mapped_column(String(50))
    CreatedOn: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedOn: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ClosedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ClosedOn: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    HospitalScheduleConfigurationId: Mapped[int | None] = mapped_column(Integer, nullable=True)


class HospitalScheduleConfiguration(Base):
    __tablename__ = "HospitalScheduleConfiguration"

    HospitalScheduleConfigurationId: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    HospitalId: Mapped[int] = mapped_column(Integer)
    ScheduleTermId: Mapped[int] = mapped_column(Integer)
    MaintenanceTypeId: Mapped[int] = mapped_column(Integer)
    StartMonth: Mapped[str] = mapped_column(String(50))
    Notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    IsActive: Mapped[bool] = mapped_column(Boolean, default=True)
    CreatedBy: Mapped[str] = mapped_column(String(50))
    CreatedOn: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedOn: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ReminderDaysBeforeStart: Mapped[int] = mapped_column(Integer, default=0)
    ReminderRecipients: Mapped[str | None] = mapped_column(Text, nullable=True)


class HospitalScheduleUnitSummary(Base):
    __tablename__ = "HospitalScheduleUnitSummary"

    HospitalScheduleUnitSummaryId: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    HospitalScheduleId: Mapped[int] = mapped_column(Integer)
    HUID: Mapped[int] = mapped_column(Integer)
    TotalTracks: Mapped[int] = mapped_column(Integer, default=0)
    InstalledTracks: Mapped[int] = mapped_column(Integer, default=0)
    RemainingTracks: Mapped[int] = mapped_column(Integer, default=0)
    StartDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CompleteDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    LastCalculatedOn: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    CreatedBy: Mapped[str] = mapped_column(String(50))
    CreatedOn: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedOn: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class ScheduleReminder(Base):
    __tablename__ = "ScheduleReminder"

    ScheduleReminderId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HospitalScheduleId: Mapped[int] = mapped_column(Integer)
    HospitalId: Mapped[int] = mapped_column(Integer)
    ReminderDateTime: Mapped[datetime] = mapped_column(DateTime)
    Status: Mapped[str] = mapped_column(String(20), default="Scheduled")
    SeenByUserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SeenOn: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    SnoozedUntil: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    DismissedByUserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    DismissedOn: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedVisitId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    CreatedOn: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ScheduleReminderRecipient(Base):
    __tablename__ = "ScheduleReminderRecipient"

    ScheduleReminderRecipientId: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    ScheduleReminderId: Mapped[int] = mapped_column(Integer)
    UserId: Mapped[str] = mapped_column(String(50))
    EmailSent: Mapped[bool] = mapped_column(Boolean, default=False)
    EmailSentOn: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedOn: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Scheduler(Base):
    __tablename__ = "Scheduler"

    ScheduleID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HospitalID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Maintenance: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ScheduleRecurrence: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Frequency: Mapped[int | None] = mapped_column(Integer, nullable=True)
    DaysOfWeek: Mapped[int | None] = mapped_column(Integer, nullable=True)
    WeeklyInterval: Mapped[int | None] = mapped_column(Integer, nullable=True)
    MonthlyInterval: Mapped[int | None] = mapped_column(Integer, nullable=True)
    QuarterInterval: Mapped[int | None] = mapped_column(Integer, nullable=True)
    QuartelyInterval: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Month: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Day: Mapped[int | None] = mapped_column(Integer, nullable=True)
    NumberOfOccurrences: Mapped[int | None] = mapped_column(Integer, nullable=True)
    StartDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    EndDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    IsCanceled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    NoEndDate: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    Units: Mapped[int | None] = mapped_column(Integer, default=0)


class ScheduleDateList(Base):
    __tablename__ = "ScheduleDateList"

    ScheduleDateId: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    Description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    Maintenance: Mapped[str | None] = mapped_column(String(50), nullable=True)
    HUID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    HID: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    UnitName: Mapped[str | None] = mapped_column(String(50), nullable=True)
    NextOccurrence: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    DateUpdated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    StartDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    EndDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ScheduleId: Mapped[int | None] = mapped_column(BigInteger, nullable=True)


class ExemptedDates(Base):
    __tablename__ = "Exempted_Dates"

    ExemptedId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HospitalID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Maintenance: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ScheduledDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ExemptedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Created: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Updated_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class HospitalDeliverySchedule(Base):
    __tablename__ = "Hospital_Delivery_Shedule"

    SID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HCNO: Mapped[int] = mapped_column(BigInteger)
    SheduledDay: Mapped[str] = mapped_column(String(10))
    DeliveryDate: Mapped[datetime] = mapped_column(DateTime)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    DateUpdated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


# ═══════════════════════════════════════════════════════════════════════════════
# INVOICE / PRICING TABLES
# ═══════════════════════════════════════════════════════════════════════════════


class Invoice(Base):
    __tablename__ = "Invoice"

    InvoiceNo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    InvoiceDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    MngDocURL: Mapped[str | None] = mapped_column(Text, nullable=True)
    DelAppDocURL: Mapped[str | None] = mapped_column(Text, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ServiceCEOInvoice: Mapped[str | None] = mapped_column(Text, nullable=True)
    Amount: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    SCEOInvoiceNo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    SCEOInvoiceLink: Mapped[str | None] = mapped_column(String(1000), nullable=True)


class InvoiceDetail(Base):
    __tablename__ = "InvoiceDetails"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    CurBarCode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ScanedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CurtainStatus: Mapped[int | None] = mapped_column(Integer, nullable=True)
    InvoiceNo: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Price: Mapped[float | None] = mapped_column(Float, nullable=True)
    ScanedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    visitId: Mapped[int | None] = mapped_column(Integer, nullable=True)


class HospPricing(Base):
    __tablename__ = "Hosp_Pricing"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HID: Mapped[int] = mapped_column(Integer)
    ServiceType: Mapped[int] = mapped_column(Integer)
    Installation: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    FM_Snap: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    FM_Standard: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    FM_Psyc: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    FM_OnTheRightTrack: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    PN_Snap: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    PN_Standard: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    PN_Psyc: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    PN_OnTheRightTrack: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    Contract: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    DateCreated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    DateUpdated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    AIAutomationHospitalSpares: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    FM_Drape: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    PN_Drape: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    Disposable: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    AfterhourPricing: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    AfterhourPricingPanel: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)


class HospPricingNew(Base):
    __tablename__ = "Hosp_Pricing_New"

    Id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    HID: Mapped[int] = mapped_column(Integer)
    ServiceType: Mapped[int] = mapped_column(Integer)
    PricingTypeID: Mapped[int] = mapped_column(ForeignKey("PricingType.PricingTypeID"))
    Amount: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    DateCreated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    DateUpdated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CurtainTypeID: Mapped[int | None] = mapped_column(
        ForeignKey("Curt_Type.Curt_TypeID"), nullable=True
    )
    SizeType: Mapped[str | None] = mapped_column(String(20), nullable=True)


# ═══════════════════════════════════════════════════════════════════════════════
# OTHER OPERATIONAL TABLES
# ═══════════════════════════════════════════════════════════════════════════════


class ScannedHistory(Base):
    __tablename__ = "ScannedHistory"

    scannedHistoryId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curtBarCode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    userId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    scannedDateTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ScannedStatus: Mapped[int | None] = mapped_column(Integer, nullable=True)
    SourcedScreen: Mapped[str | None] = mapped_column(String(50), nullable=True)


class ScanComments(Base):
    __tablename__ = "ScanComments"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    CurtainBarCode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    CurtainStatus: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    Created_By: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Created_Date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Notification(Base):
    __tablename__ = "Notifications"

    NotificationId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    UserId: Mapped[str | None] = mapped_column(String(100), nullable=True)
    Message: Mapped[str] = mapped_column(String(500))
    IsRead: Mapped[bool] = mapped_column(Boolean, default=False)
    CreatedAt: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    IssueCategory: Mapped[str | None] = mapped_column(String(100), nullable=True)
    Action: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ReferenceId: Mapped[int | None] = mapped_column(Integer, nullable=True)


class TempStorageLocation(Base):
    __tablename__ = "TempStorageLocation"

    TempStorageId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    LocationName: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    LocationBarcode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    InLocationTypeID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    OutLocationTypeID: Mapped[int | None] = mapped_column(Integer, nullable=True)


class AIAutomationHospitalTempStorage(Base):
    __tablename__ = "AIAutomationHospitalTempStorage"

    AIAutomationHospitalTempStorageId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    BagID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    BagBarcode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CurtainBarcode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    TrackBarcode: Mapped[str | None] = mapped_column(String(50), nullable=True)
    VisitId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ReturnedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ReturnedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    isUsedInBag: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    UseInBagDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class TblInStorage(Base):
    __tablename__ = "TblInStorage"

    ID: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    BID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    UID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    UNo: Mapped[int | None] = mapped_column(Integer, nullable=True)
    FloorNo: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Comments: Mapped[str | None] = mapped_column(String(250), nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    InStorageBarcode: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    Created_by: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Created_Date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Update_by: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Updated_Date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class IssueTracker(Base):
    __tablename__ = "IssueTracker"

    IssueId: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    RaisedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    IssueType: Mapped[str | None] = mapped_column(String(50), nullable=True)
    IssueStatus: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Description: Mapped[str | None] = mapped_column(Text, nullable=True)
    HandleBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SolutionDescription: Mapped[str | None] = mapped_column(Text, nullable=True)
    DateCreated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    DateUpdated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    VisitId: Mapped[int | None] = mapped_column(Integer, nullable=True)


class IssueAttachment(Base):
    __tablename__ = "IssueAttachments"

    AttachementId: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    AttachmentUrl: Mapped[str | None] = mapped_column(String(200), nullable=True)
    IssueId: Mapped[int | None] = mapped_column(BigInteger, nullable=True)


class MaintainanceReport(Base):
    __tablename__ = "MaintainanceReport"

    MaintainanceReportId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    TimeIn: Mapped[str | None] = mapped_column(String(20), nullable=True)
    TimeOut: Mapped[str | None] = mapped_column(String(20), nullable=True)
    SubmitDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Lead: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Asistant: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ProjectNumber: Mapped[str | None] = mapped_column(String(50), nullable=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    UnitsWorkPerformed: Mapped[str | None] = mapped_column(String(200), nullable=True)
    IsSpareInstalled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    WhosSpareInstalled: Mapped[str | None] = mapped_column(String(20), nullable=True)
    AreaCompleted: Mapped[str | None] = mapped_column(String(200), nullable=True)
    RoomsPending: Mapped[str | None] = mapped_column(String(200), nullable=True)
    CustomerComment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    NextVisit: Mapped[str | None] = mapped_column(String(500), nullable=True)
    StorageCondition: Mapped[str | None] = mapped_column(String(500), nullable=True)
    Comment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    Problems: Mapped[str | None] = mapped_column(String(300), nullable=True)
    UserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    DateUpdated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    VisitId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    curtainTrackCondition: Mapped[str | None] = mapped_column(String(50), nullable=True)
    addTrackAccessories: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    pickupFromSoiled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    IsSubmitIssue: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    returnAnyCurtain: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class RemeshOrder(Base):
    __tablename__ = "Remesh_Order"

    OrderID: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    HID: Mapped[int] = mapped_column(Integer)
    OrderBy: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ProposalNo: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ProjectNo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    InvoiceNo: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Amount: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    InvoiceAmount: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    Tags: Mapped[str | None] = mapped_column(String(200), nullable=True)
    ServiceType: Mapped[str | None] = mapped_column(String(30), nullable=True)
    DateOrdered: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    DatePromised: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str] = mapped_column(String(50))
    CreatedDate: Mapped[datetime] = mapped_column(DateTime)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Comment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    IsVisitCreated: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    IsStepOneDone: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    IsStepTwoDone: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    IsStepThreeDone: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class RemeshOrderDetail(Base):
    __tablename__ = "Remesh_Order_Details"

    ID: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    OrderID: Mapped[int] = mapped_column(Integer)
    HID: Mapped[int] = mapped_column(Integer)
    CID: Mapped[int] = mapped_column(Integer)
    CurBarCode: Mapped[int] = mapped_column(Integer)
    Comment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    LinearFeet: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    Amount: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    RemeshCost: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    LaundryCost: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    CreatedBy: Mapped[str] = mapped_column(String(50))
    CreatedDate: Mapped[datetime] = mapped_column(DateTime)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Truck(Base):
    __tablename__ = "Truck"

    TruckID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    TruckBarcode: Mapped[str] = mapped_column(String(50), unique=True)
    TruckNumber: Mapped[str] = mapped_column(String(50))
    DriverName: Mapped[str | None] = mapped_column(String(100), nullable=True)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str] = mapped_column(String(50))
    DateUpdated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class WrongAttempt(Base):
    __tablename__ = "WrongAttempt"

    WrongAttemptId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    VisitId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    CurtBarcode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    TrackBarcode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    UserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    HospitalId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    AttamptDateTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class DuplicateInstalledRecord(Base):
    __tablename__ = "duplicateInstalledRecords"

    DuplicateInstalledRecords: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    VisitId: Mapped[int] = mapped_column(Integer)
    CurtBarCode: Mapped[int] = mapped_column(Integer)
    TrackBarCode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    InstalledDateTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Installer: Mapped[str | None] = mapped_column(String(50), nullable=True)


class InstallerCommission(Base):
    __tablename__ = "InstallerCommission"

    InstallerID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    InstallerTypeID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    WidthIDLL: Mapped[int | None] = mapped_column(Integer, nullable=True)
    WidthIDUL: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Curt_TypeID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    CommissionAmount: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    DateCreated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    DateUpdated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Enabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class InstallerCommissions(Base):
    __tablename__ = "InstallerCommissions"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    PricingFor: Mapped[int | None] = mapped_column(Integer, nullable=True)
    FM_Snap: Mapped[float | None] = mapped_column(Float, nullable=True)
    FM_Standard: Mapped[float | None] = mapped_column(Float, nullable=True)
    FM_Psyc: Mapped[float | None] = mapped_column(Float, nullable=True)
    FM_OnTheRightTrack: Mapped[float | None] = mapped_column(Float, nullable=True)
    Pn_Snap: Mapped[float | None] = mapped_column(Float, nullable=True)
    Pn_Standard: Mapped[float | None] = mapped_column(Float, nullable=True)
    Pn_Psyc: Mapped[float | None] = mapped_column(Float, nullable=True)
    Pn_OnTheRightTrack: Mapped[float | None] = mapped_column(Float, nullable=True)
    CreatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    HID: Mapped[int | None] = mapped_column(Integer, nullable=True)


class InstCommTransaction(Base):
    __tablename__ = "InstCommTransaction"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    Hid: Mapped[int | None] = mapped_column(Integer, nullable=True)
    CurtBarCode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    UserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Price: Mapped[float | None] = mapped_column(Float, nullable=True)
    CreatedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class PaybyTrackCommission(Base):
    __tablename__ = "PaybyTrackCommission"

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    SparePrice: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    TrackPrice: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    UnitPrice: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    StoragePrice: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    AddDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdateDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    AddedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    StoragePriceByStop: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    CurtainScanPrice: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)
    ScanPriceAbove500: Mapped[float | None] = mapped_column(Numeric(19, 4), nullable=True)


class LastLogin(Base):
    __tablename__ = "LastLogin"

    LastLoginId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    UserId: Mapped[str] = mapped_column(String(50))
    LoginDateTime: Mapped[datetime] = mapped_column(DateTime)
    DeviceName: Mapped[str | None] = mapped_column(String(200), nullable=True)


class LastSyncInfo(Base):
    __tablename__ = "LastSyncInfo"

    LastSyncInfoId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    UserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    LastSyncDateTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    lastLogin: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class LocationDetailRecord(Base):
    __tablename__ = "LocationDetail"

    LocId: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    LocLatitude: Mapped[str | None] = mapped_column(String(50), nullable=True)
    LocLongitude: Mapped[str | None] = mapped_column(String(50), nullable=True)
    CreatedDateTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UserId: Mapped[str | None] = mapped_column(String(50), nullable=True)


class PendingEmail(Base):
    __tablename__ = "PendingEmails"

    IssueId: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    EmailTo: Mapped[str] = mapped_column(String(255))
    Subject: Mapped[str | None] = mapped_column(String(500), nullable=True)
    Body: Mapped[str | None] = mapped_column(Text, nullable=True)
    HasAttachments: Mapped[bool | None] = mapped_column(Boolean, default=False)
    EmailSent: Mapped[bool | None] = mapped_column(Boolean, default=False)
    CreatedAt: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class PerformAction(Base):
    __tablename__ = "PerformAction"

    PerformActionID: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    VisitID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    DeletedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    DeletedBy: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ActionJson: Mapped[str | None] = mapped_column(Text, nullable=True)
    UserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    isOperationCompleted: Mapped[bool | None] = mapped_column(Boolean, default=False)
    CompletedDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class VisitDropByUser(Base):
    __tablename__ = "VisitDropByUser"

    VisitDropById: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    DropById: Mapped[str | None] = mapped_column(String(50), nullable=True)
    VisitId: Mapped[int | None] = mapped_column(Integer, nullable=True)


class VisitVisitedBy(Base):
    __tablename__ = "VisitVisitedBy"

    VisitVisitedById: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    VisitedById: Mapped[str | None] = mapped_column(String(50), nullable=True)
    VisitId: Mapped[int | None] = mapped_column(Integer, nullable=True)


class VisitInstallationImage(Base):
    __tablename__ = "VisitInstallationImage"

    VisitInstallationImageId: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    ImageUrl: Mapped[str | None] = mapped_column(String(200), nullable=True)
    VisitId: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    ImageType: Mapped[str | None] = mapped_column(String(50), nullable=True)
    UserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    createdDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class VisitMergeHistory(Base):
    __tablename__ = "VisitMergeHistory"

    VisitMergeId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    MergedVisitId: Mapped[int] = mapped_column(Integer)
    TargetVisitId: Mapped[int] = mapped_column(Integer)
    MergedByUserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    MergedDateTime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Comments: Mapped[str | None] = mapped_column(Text, nullable=True)


class VisitPicture(Base):
    __tablename__ = "VisitPictures"

    pictureId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    visitId: Mapped[int] = mapped_column(Integer)
    picture: Mapped[str] = mapped_column(Text)
    comment: Mapped[str | None] = mapped_column(String(250), nullable=True)
    dateCreated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    createdBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    pictureName: Mapped[str | None] = mapped_column(String(50), nullable=True)


class VisitStorageInstallation(Base):
    __tablename__ = "VisitStorageInstallation"

    StorageInstallationId: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    VisitId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    Image: Mapped[str | None] = mapped_column(Text, nullable=True)
    FileName: Mapped[str | None] = mapped_column(String(50), nullable=True)
    Dateupdated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UserId: Mapped[str | None] = mapped_column(String(50), nullable=True)
    IsBeforeAfterPicture: Mapped[str | None] = mapped_column(String(50), nullable=True)


class VisitTempStorage(Base):
    __tablename__ = "VisitTempStorage"

    VisitLocationId: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    VisitId: Mapped[int] = mapped_column(Integer)
    PickupDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    TempStorageId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    DropBagBy: Mapped[str | None] = mapped_column(String(50), nullable=True)


class VisitDetailDeleted(Base):
    __tablename__ = "VisitDetailDeleted"

    VisitId: Mapped[int] = mapped_column(Integer, primary_key=True)
    CurtBarCode: Mapped[int | None] = mapped_column(Integer, primary_key=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class VisitDetailRemoved(Base):
    __tablename__ = "VisitDetailRemoved"

    VisitId: Mapped[int] = mapped_column(Integer, primary_key=True)
    CurtBarCode: Mapped[int] = mapped_column(Integer, primary_key=True)
    TrackBarCode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    DeliveryDate: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    Date_Updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    UpdatedBy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    BagID: Mapped[int | None] = mapped_column(Integer, nullable=True)
    BagBarcode: Mapped[str | None] = mapped_column(String(50), nullable=True)
