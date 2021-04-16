# Stand Out Suggestions


## String representation of ```NearEarthObject```

When a ```NearEarthObject``` is printed (called as str), a string is returned indicating 
the NEO fullname and if is or not potentially hazardous. The diameter is only indicated 
when it's known.


## Modifying Tests to solve errors

For task 2a, function ```load_neos``` (in file ```extract.py```) must return a collection 
of ```NearEarthObject```s. It's usefull to return a dictionary with the primary designation 
as key and the NEO object as value. Tests proposed to debug the code raise some errors 
if the function return a dictionary, so changes in tests must be done.

```tests/test_extract.py```
```python
class TestLoadNEOs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.neos = load_neos(TEST_NEO_FILE).values()  # Add '.values()' to allow 'load_neos' return a dictionary.
        cls.neos_by_designation = {neo.designation: neo for neo in cls.neos}
    ...
```

```tests/test_database.py```
```python
class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.neos = load_neos(TEST_NEO_FILE)
        cls.approaches = load_approaches(TEST_CAD_FILE)
        cls.db = NEODatabase(cls.neos, cls.approaches)
        cls.neos = cls.neos.values()  # Add this line to allow 'load_neos' return a dictionary and pass the tests.
    ...
```

```tests/test_write.py```
```python
...

def build_results(n):
    neos = load_neos(TEST_NEO_FILE)  # removed tuple conversion, neos is a dictionary.
    approaches = tuple(load_approaches(TEST_CAD_FILE))

    # Only needed to link together these objects.
    NEODatabase(neos, approaches)

    return approaches[:n]

...
```
The final code in ```extract.py``` for ```load_neos``` return a list to avoid test errors, 
but code to return a dictionary has been commented. Return a dictionary is better than 
return a list and then build the dictionary in ```database.py```.


## Extra information for ```CloseApproach``` objects

A new attribute, ```extra_information```, has been added to ```NearEarthObjects``` 
and ```CloseApproach``` classes in ```models.py``` file. This attribute contains a 
dictionary with extra information about the NEO or the Close Approach and can be usefull 
to give more functionalities to the project.


## New method for ```CloseApproach``` objects

In order to optimize the connection between ```NearEarthObjects``` and ```CloseApproach```es 
when creating the ```NEODatabase``` in task 2b, a new method has been added 
to ```CloseApproach``` class in ```models.py``` file.

```python
class CloseApproach:
    ...
    
    def assign_neo(self, neos):
        if self._designation in neos:
            self.neo = neos[self._designation]
            self.neo.approaches.append(self)
        else:
            self.neo = None
        return self
    
    ...
```

The input parameter ```neos``` is a dictionary with NEO objects as values and the primary 
designation as key.
