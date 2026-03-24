# fed-districts

This is a compilation of data on congressional districts, made to be easily accessible.


# How to Use

If you just want to browse and download a few files, you do not need to read this. If you want to efficiently scrape the data, this section will be useful.

The file `ref.json` contains the required parameters to access all data in this repo. Each top level entry is a type of data (more information below). Inside that entry is an entry called `relPath`, which provides the relative path from the root of the repo. You must replace the bracketed parameters with the appropriate information by state and by district. Below is a type-by-type description of the available data and its parameters.
* *shapes*: A map of a district, usually precise to a couple meters.
    * Each state has an entry in `states`. Each state's entry is composed of a list of maps, with their first congress year, adoption date, district count, and source.
        * `firstCongress` is the year when the first Congress using this map will be convened.
    * To complete the path to the `geojson`, use the year from the `firstCongress` field.
* *pvi*: Cook PVI scores by district.
    * The publishing year of the score is needed to fill in the path.
    * Remember to check if a district has been redrawn since this data was published. You can do this by comparing the `published` date of the map in `cook/reports` with the `firstCongress` date of the map in `shapes`.
* *econ*: Various economic values (such as income) by district.
    * The data year of the score is needed to fill in the path.
    * Remember to check if a district has been redrawn since this data was collected. You can do this by comparing the `year` date of the map in `econ` with the `firstCongress` date of the map in `shapes`.
        * When using data from different years, remember to correct for inflation.
    * Information on select headers is provided below. The data is broken up into sections, as shown by the header's prefix before the underscore.
        * `cd`: The congressional district
        * `inc`: Income data
            * `_medianHHI` and  `_meanHHI`: Median and mean household income
            * `_perCapita`: Per capita income
        * `popEmp`: Employment status of the population
            * `_16plusTotalPop`: Total population 16 and up
        * `civInd`: Industry of civilian workers. The extended names of the industries are listed below.
            * Agriculture, forestry, fishing and hunting, and mining
            * Construction
            * Manufacturing
            * Wholesale trade
            * Retail trade
            * Transportation and warehousing, and utilities
            * Information
            * Finance and insurance, and real estate and rental and leasing
            * Professional, scientific, and management, and administrative and waste management services
            * Educational services, and health care and social assistance
            * Arts, entertainment, and recreation, and accommodation and food services
            * Other services, except public administration
            * Public administration
        * `civHealth`: Health insurance coverage of the noninstitutionalized population
            * `_nonInstTotalPop`: Total non-institutionalized population
            * `_covered`: Total people covered on health insurance (note this is less than the sum of private & public)
            * `_private` and `_public` and `_none`: People with private/public/no health coverage
* *results*: Election results by congressional district
    * The year of the election and the type of election (house/president) is needed to access the data.
    * The `DEM` and `REP` are the results that all Democrat and Republic candidates received, respectively. `MARGIN` is the difference between those vote shares. `REMAIN` is the remaining vote share.
        * For multiple-round elections, only the final round is used.
    * Special elections and primaries are not included.

Additional useful information:
* Districts are always referred to by two-digit codes (including leading zeroes; at large districts are `00`).
* Entries are in reverse chronological order so the most recent is at the first index.
* This repo does not include any data from before 2020. Note this is why the at-large districts are marked as being enacted on Jan 1, 2020.
* Access the raw data at `https://raw.githubusercontent.com/ellio27/fed-districts/refs/heads/main/`


# Useful Scripts

Useful scripts are in the `scripts` folder.

* `combine-cds.py` contains code for creating a combined map of all districts. Details about the parameters (defined as globals in the script) are in the script itself. The script MUST be run from the root directory of this repo (e.g. `python3 scripts/combine-cds.py`).
    * The output is placed in an `output` folder. Some pre-built data is available in `artifacts`.


# Errors

If you find any errors, please report them through the Github issues tab.


# Credits and Usage

I do not claim ownership of this data. When easily available, I used data from a government website but other sources were also used. See `ref.json` for complete information on the original sources. A summary of usage guidelines is provided below, but it is not a substitute for the full guidelines:
* _Data from state governments_: Use freely.
* _Data from Redistricting Data Hub_: Use for noncommercial, nonpartisan purposes and not for gerrymandering. Provide credit for use.