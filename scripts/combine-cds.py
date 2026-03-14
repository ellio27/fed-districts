import json
import os
import util as util

'''
The year congress starts that you are interested in. For maps used in, for example,
the 2026 election, the Congress starting year is 2027.
'''
CONGRESS_YEAR = 2027
'''
Precision is in decimal places.
The combined files can be quite large, 5-6 decimals is recommended.
'''
PRECISION = 5
'''
If so, Alaska and Hawaii will be ignored.
'''
LOWER_48_ONLY = False
'''
Whether or not to show logging.
'''
VERBOSE = True


class StateMapData:
    relPath = ""

    def __init__ (self, stateAbbr, districtCount, firstCongress):
        self.state = stateAbbr
        self.count = districtCount
        self.congress = firstCongress

    def to_string (self):
        return f"{self.state}: {self.count}x (est. {self.congress})"

class DistrictMapData:
    def __init__ (self, year, state, district):
        self.year = str(year)
        self.state = state
        self.district = f"{district:02d}"

    def get_path (self):
        return (
            StateMapData.relPath
            .replace ("[YEAR]", self.year)
            .replace ("[ST]", self.state)
            .replace ("[CD]", self.district)
        )

# requesting is the year from the user, testing is the year from the data
def is_year_valid (requestingYear, testingYear):
    return requestingYear >= testingYear


### ROUTINES

def parse_all_shapes (year, verbose = False):
    ref = util.read_json ("ref.json")
    StateMapData.relPath = ref["shapes"]["relPath"]

    stateData = {} # dictionary of string to StateMapData
    for stateAbbr, stateInfo in ref["shapes"]["states"].items():
        foundValidMap = False

        for mapData in stateInfo:
            if is_year_valid (year, mapData["firstCongress"]):
                stateData[stateAbbr] = StateMapData (stateAbbr, mapData["districts"], mapData["firstCongress"])
                foundValidMap = True
                break

        if (not foundValidMap):
            print (f"\033[33mWARN: Did not find valid map for '{stateAbbr}'\033[0m")

    if verbose:
        print (f"Loaded {len (stateData)} state maps...")

    districtData = [] # list of DistrictMapData
    for stateMap in stateData.values ():
        if stateMap.count == 1:
            # states with 1 district have their district coded as '00'
            districtData.append (
                DistrictMapData (
                    stateMap.congress,
                    stateMap.state,
                    0
                )
            )
        else:
            for idx in range (1, stateMap.count + 1):
                districtData.append (
                    DistrictMapData (
                        stateMap.congress,
                        stateMap.state,
                        idx
                    )
                )
    
    if verbose:
        print (f"Loaded {len (districtData)} districts maps...")

    return districtData

def extract_features (allDistricts, lower48 = False, verbose = False):
    combinedFeatures = []
    for district in allDistricts:
        if lower48 and district.state in ("ak", "hi"):
            continue
        path = district.get_path ()
        geojson = util.read_json (path)

        if geojson["type"] == "FeatureCollection":
            features = geojson["features"]
        else:
            features = [geojson]

        for feature in features:
            feature["properties"] = {
                "state": district.state,
                "district": district.district
            }
            combinedFeatures.append (feature)

    combined = {
        "type": "FeatureCollection",
        "features": combinedFeatures
    }

    if verbose:
        print (f"Combined all districts...")

    return combined

def compress_features (allFeatures, precision, verbose = False):
    def round_coords (coords):
        if isinstance (coords[0], list):
            return [round_coords (c) for c in coords]
        return [round (c, precision) for c in coords]

    for feature in allFeatures["features"]:
        feature["geometry"]["coordinates"] = round_coords (feature["geometry"]["coordinates"])

    if verbose:
        print (f"Compressed coords to {precision} decimals...")

    return allFeatures

def write_output_geojson (allFeatures, year, precision = None, lower48 = False, verbose = False):
    os.makedirs ("output", exist_ok = True)

    nameType = "_l48" if lower48 else ""
    namePrecision = "" if precision == None else f"_p{precision}"

    outputPath = os.path.join ("output", f"cds_{year}{nameType}{namePrecision}.geojson")

    with open (outputPath, "w") as f:
        json.dump (allFeatures, f)

    if verbose:
        print (f"Wrote to {outputPath}.")

def combine_all_districts (year, precision = None, verbose = False):
    allDistricts = parse_all_shapes (year, verbose)
    allFeatures = extract_features (allDistricts, False, verbose)
    if precision != None:
        if precision < 1 or precision > 15:
            print (f"\033[33mWARN: Precision had invalid value, skipping compression.\033[0m")
        else:
            allFeatures = compress_features (allFeatures, precision, verbose)

    write_output_geojson (allFeatures, year, precision, LOWER_48_ONLY, verbose)

def main():
    combine_all_districts (CONGRESS_YEAR, PRECISION, VERBOSE)

if __name__ == "__main__":
    main()
