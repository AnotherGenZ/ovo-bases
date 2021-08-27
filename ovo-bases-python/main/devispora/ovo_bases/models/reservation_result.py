from devispora.ovo_bases.models.reservations import Reservation


class ReservationResult:
    def __init__(self, succeeded_reservations: [Reservation], failed_reservations: [Reservation]):
        self.succeeded_reservations = succeeded_reservations
        self.failed_reservations = failed_reservations
