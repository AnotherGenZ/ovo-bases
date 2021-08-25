from devispora.ovo_bases.models.reservations import Reservation


class AvailabilityResult:

    def __init__(self, possible_reservations: [Reservation], denied_reservations: [Reservation]):
        self.possible_reservations = possible_reservations
        self.denied_reservations = denied_reservations
