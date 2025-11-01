from dataclasses import dataclass


@dataclass
class Venue:
    address: str
    latitude: float
    longitude: float

    def __composite_values__(self):
        return self.address, self.latitude, self.longitude

    def __repr__(self):
        return f"<Venue(address={self.address}, lat={self.latitude}, lng={self.longitude})>"

    def __eq__(self, other):
        if not isinstance(other, Venue):
            return NotImplemented
        return (
            self.address == other.address
            and self.latitude == other.latitude
            and self.longitude == other.longitude
        )

