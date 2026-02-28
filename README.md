# fed-districts

This is a compilation of data on congressional districts, made to be easily accessible.


# How to Use

If you just want to browse and download a few files, you do not need to read this. If you want to efficiently scrape the data, this section will be useful.

The file `ref.json` contains the required parameters to access all data in this repo. Each top level entry is a type of data (more information below). Inside that entry is an entry called `path`, which provides a URL to access the data. You must replace the bracketed parameters with the appropriate information by state and by district. Note that districts are always refered as two-number codes (include leading zeroes, at-large districts are `00`). Below is type-by-type description of the available data and its parameters.
* *shapes*: A map of a district, usually precise to a couple meters.
    * The approval year of the map (not the election year) is needed to fill in the path. All years with data for that state are listed in the state-specific entry's list, `years`. The years are in descending order, so the first entry is the most recent.
    * The source of the data for a given year is the same-index entry in the `sources` list.


# Credits and Usage

I do not claim ownership of this data. When easily available, I used data from a government website but other sources were also used. See `ref.json` for complete information on the original sources. A summary of usage guidelines is provided below, but it is not a substitute for the full guidelines:
* Data from state governments: Use freely.
* Data from Redistricting Data Hub: Use for noncommercial, nonpartisan purposes and not for gerrymandering. Provide credit for use.