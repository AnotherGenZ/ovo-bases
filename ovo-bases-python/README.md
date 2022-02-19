## OvO Bases
This service allows you to check the availability of bases (facilities) and reserve them as well.  
The service accepts two types of requests as `request_type`:

- availability
- reservation

Reservation will also check availability, but will complete reservations for bases that are allowed within the timeframe
and are allowed.

There are three types of groups that call the service. POG, OvO and Admin. These are accompanied by the
following `reservation_type`:

- large_event
- scrim
- training
- pog

Scrims and trainings are suitable for OvO and Admins can create large_events that can take up to three days. POG desires
specific requirements, which is the ability to request direct availability. POG requests will check for up to an hour of
availability, but it will return anything that is available the next 45 minutes. POG availability requests have to be
done in the following format:

```json
{
  "facility_ids": [
    266000,
    239000
  ],
  "reservation_type": "pog",
  "request_type": "availability",
  "group_name": "POG_BOT"
}
```

Basically you want to supply all the `facility_ids` you want to check availability on.  
The service will add timestamps internally. A traditional `reservation_type` however can be done the following way:

```json
{
  "facility_ids": [
    266000,
    239000
  ],
  "reservation_type": "training",
  "request_type": "reservation",
  "group_name": "HELP",
  "start_time": 1643760000,
  "end_time": 1643767200
}
```

Non POG-reservations currently have multiple basic restrictions:

- The `start_time` cannot be longer than an hour ago.
- The `end_time` cannot be before the `start_time`.
- Reservations cannot take longer than three days.