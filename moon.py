import ephem
import datetime

def get_moon_phase(date=None):
    """
    This function returns the moon phase for a given date.
    If no date is provided, the current date is used.

    :param date: The date for which the moon phase is fetched.
    :type date: datetime.date, optional
    :return: The moon phase (0: New Moon, 0.5: First Quarter, 1.0: Full Moon)
    :rtype: float
    https://rhodesmill.org/pyephem/quick.html
    """
    if date is None:
        date = datetime.datetime.now()

    moon = ephem.Moon(date)
    phase = moon.moon_phase
    return phase

if __name__ == "__main__":
    date = datetime.datetime.now()
    moon_phase = get_moon_phase(date)
    print(f"Today's moon phase is: {moon_phase:.2f}")
    
    next_full_moon = ephem.next_full_moon(date)
    print(f"Next full moon is: {next_full_moon}")
    
    next_new_moon = ephem.next_new_moon(date)
    print(f"Next new moon is: {next_new_moon}")
    
    