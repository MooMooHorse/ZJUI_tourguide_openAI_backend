# BUGLOG

## SEV 1

### 0001: Search Engine Failure on getting locations for Qs involved in > 1 locations

#### Description

When a user searches for a Q that is involved in more than one location, the search engine fails to return the correct locations.

#### Solution

```python
q_locations = json.loads(self.get_location(question, candidates_locations))

if type == 1 or cur_location in q_locations:
    locations = q_locations
elif type == 2:
    locations = [cur_location] + q_locations
```

### 0002: Search Engine location association return format

#### Description

Sometimes the return format of the location association module is broken. 
```
{'Locations': ['Dining Hall']}
To find out the cheapest item in a school's dining hall, you can typically look for items like snacks, small drinks, or side dishes. These items are usually priced lower than main entrees or larger meals. You can also inquire directly at the dining hall or check the menu for specific pricing information.
```

#### Solution

We added a stabliity check to ensure that the return format is correct.

We also conduct heavy prompt engineering to ensure that the location association module is not broken.


## SEV 2

## SEV 3