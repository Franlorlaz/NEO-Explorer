"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, pdes, name='', diameter='', pha='N', **extra):
        """Create a new `NearEarthObject`.

        :param pdes: A string with the primary designation of the NEO.
        :param name: A string with the International Astronomical Union (IAU) name of the NEO.
        :param diameter: A string with the NEO's diameter in kilometers. Empty string if unknown.
        :param pha: If the NEO is a 'Potentially Hazardous Asteroid'. Must be 'Y' or 'N' (string).
        :param extra: Extra information about the NEO.
        """
        self.designation = str(pdes)
        self.name = str(name) or None

        if not diameter:
            diameter = 'nan'
        self.diameter = float(diameter)

        if pha == 'N':
            pha = ''
        self.hazardous = bool(pha)

        self.approaches = []
        self.extra_information = extra

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        fullname = f'{self.designation}'
        if self.name:
            fullname += f' ({self.name})'
        return fullname

    def __str__(self):
        """Return `str(self)`, a human-readable string representation of this object."""
        string = f'NEO {self.fullname!r}'

        if self.diameter == self.diameter:  # False when self.diameter = nan
            string += f' has a diameter of {self.diameter:.3f} km and'

        if self.hazardous:
            string += f' is potentially hazardous.'
        else:
            string += f' is not potentially hazardous.'

        return string

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, des, cd, dist, v_rel, **extra):
        """Create a new `CloseApproach`.

        :param des: Primary designation of the asteroid or comet.
        :param cd: Time of close-approach (formatted calendar date in 'YYYY-bb-DD hh:mm', in UTC).
        :param dist: Nominal approach distance (au).
        :param v_rel: Velocity relative to the approach body at close approach (km/s).
        :param extra: Extra information about the Close Approach.
        """
        self._designation = str(des)
        self.time = cd_to_datetime(cd)
        self.distance = float(dist)
        self.velocity = float(v_rel)
        self.neo = None
        self.extra_information = extra

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`, a human-readable string representation of this object."""
        string = f'At {self.time_str},'
        if self.neo:
            string += f' {self.neo.fullname!r} approaches Earth '
        else:
            string += f' {self._designation!r} approaches Earth '
        string += f'at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s.'
        return string

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def assign_neo(self, neos):
        """Assign the NearEarthObject.

        From input dictionary of 'neos', assign the NearEarthObject corresponding to self._designation.
        The self CloseApproach object is added to the neo.approaches collection.

        :param neos: A dictionary of NearEarthObject's with the primary designation as key.
        :return: Self CloseApproach object.
        """
        if self._designation in neos:
            self.neo = neos[self._designation]
            self.neo.approaches.append(self)
        else:
            self.neo = None
        return self

    def serialize(self, extension):
        """Serialize attributes.

        :param extension: Output structure. Must be 'csv' or 'json'.
        :return: A dictionary containing relevant attributes for CSV or JSON serialization.
        """
        fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation',
                      'name', 'diameter_km', 'potentially_hazardous')

        name = self.neo.name
        if name is None:
            name = ''
        attributes = (self.time_str, self.distance, self.velocity, self.neo.designation,
                      name, self.neo.diameter, self.neo.hazardous)

        if extension == 'csv':
            attributes = (str(attr) for attr in attributes)
            return dict(zip(fieldnames, attributes))

        if extension == 'json':
            out = dict(zip(fieldnames[:3], attributes[:3]))
            out['neo'] = dict(zip(fieldnames[3:], attributes[3:]))
            return out

        if extension not in ('csv', 'json'):
            raise ValueError(f"extension must be 'csv' or 'json' (given extension={extension!r}).")
