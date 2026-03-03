# fed-districts

This is a compilation of data on congressional districts, made to be easily accessible.


# How to Use

If you just want to browse and download a few files, you do not need to read this. If you want to efficiently scrape the data, this section will be useful.

The file `ref.json` contains the required parameters to access all data in this repo. Each top level entry is a type of data (more information below). Inside that entry is an entry called `absPath`, which provides a URL to access the data (there is also `relPath` for use locally). You must replace the bracketed parameters with the appropriate information by state and by district. Below is a type-by-type description of the available data and its parameters.
* *shapes*: A map of a district, usually precise to a couple meters.
    * Each state has an entry in `states`. Each state's entry is composed of a list of maps, with their first congress year, adoption date, district count, and source.
        * `firstCongress` is the year when the first Congress using this map will be convened.
    * To complete the path to the `geojson`, use the year from the `enacted` field.
* *pvi*: Cook PVI scores by district.
    * The publishing year of the score is needed to fill in the path.
    * Remember to check if a district has been redrawn since this data was published. You can do this by comparing the `published` date of the map in `pvi` with the `firstCongress` date of the map in `shapes`.
* *hhi*: Household income by district.
    * The data year of the score is needed to fill in the path.
    * The `complete` field specifies whether or not this dataset contains all districts. This is set to false when adding updates (mainly for mid-decade redistricting).
    * Remember to check if a district has been redrawn since this data was collected. You can do this by comparing the `year` date of the map in `hhi` with the `firstCongress` date of the map in `shapes`.
        * When using data from different years, remember to correct for inflation.

Additional useful information:
* Districts are always referred to by two-digit codes (including leading zeroes; at large districts are `00`).
* Entries are in reverse chronological order so the most recent is at the first index.


# Errors

If you find any errors, please report them through the github issues tab.


# Credits and Usage

I do not claim ownership of this data. When easily available, I used data from a government website but other sources were also used. See `ref.json` for complete information on the original sources. A summary of usage guidelines is provided below, but it is not a substitute for the full guidelines:
* _Data from state governments_: Use freely.
* _Data from Redistricting Data Hub_: Use for noncommercial, nonpartisan purposes and not for gerrymandering. Provide credit for use.