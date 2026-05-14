from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_safety(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        leaders = [c for c in self.crew
                   if c.rank in (Rank.COMMANDER, Rank.CAPTAIN)]
        if not leaders:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced = [c for c in self.crew if c.years_experience >= 5]
            if len(experienced) < len(self.crew) / 2:
                raise ValueError(
                    "Long missions (> 365 days) need 50% experienced crew "
                    "(5+ years)"
                )

        if not all(c.is_active for c in self.crew):
            raise ValueError("All crew members must be active")

        return self


def display_mission(mission: SpaceMission) -> None:
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value}) "
              f"- {member.specialization}")


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)

    commander = CrewMember(
        member_id="CR001",
        name="Sarah Connor",
        rank=Rank.COMMANDER,
        age=42,
        specialization="Mission Command",
        years_experience=15,
    )
    lieutenant = CrewMember(
        member_id="CR002",
        name="John Smith",
        rank=Rank.LIEUTENANT,
        age=35,
        specialization="Navigation",
        years_experience=8,
    )
    officer = CrewMember(
        member_id="CR003",
        name="Alice Johnson",
        rank=Rank.OFFICER,
        age=29,
        specialization="Engineering",
        years_experience=6,
    )

    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2024-12-01T00:00:00",
            duration_days=900,
            crew=[commander, lieutenant, officer],
            budget_millions=2500.0,
        )
        display_mission(mission)
    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("=" * 41)
    print("Expected validation error:")
    try:
        cadet1 = CrewMember(
            member_id="CR010",
            name="Bob Brown",
            rank=Rank.CADET,
            age=22,
            specialization="Pilot",
            years_experience=1,
        )
        cadet2 = CrewMember(
            member_id="CR011",
            name="Eve Wilson",
            rank=Rank.OFFICER,
            age=27,
            specialization="Comms",
            years_experience=3,
        )
        SpaceMission(
            mission_id="M2024_BAD",
            mission_name="No Leader Mission",
            destination="Moon",
            launch_date="2024-08-01T00:00:00",
            duration_days=30,
            crew=[cadet1, cadet2],
            budget_millions=100.0,
        )
    except ValidationError as e:
        for err in e.errors():
            print(err["msg"].replace("Value error, ", ""))


if __name__ == "__main__":
    main()
