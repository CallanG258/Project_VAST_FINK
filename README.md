## Project_VAST_FINK

Hi!

This is the Repository for the Winter Research Project that I'm did with Anais Moller and Dougal Dobie. We where comparing the Radio and Optical data from crossmatched VAST and FINK sources to see if we can find some new and interesting physics from transient sources, such as AGN, Supernovae, etc.

In this repository, you'll find some Jupyter Notebooks that show different stages in coding for the analyisis for these crossmatched sources. I've tried to keep it as clean as possible and try not to add too many notebooks!

---

Contents:

Projecttools.py - Module containing commonly used code for this project. The developlent and editing of these functions were explored in other notebooks. See the file itself for more comments.


FINK_Query.ipynb - Used to query the FINK datbase and extract the optical data for sources. Required for any notebook handling optical analysis. The batches produced from this notebook are saved in FINK_Source_Data.


FINK_&_VAST_Crossmatched_Sources_Statistics_2020.ipynb - Notebook that handles loading in the crossmatch catalogue for 2020, organising each source into a series of families, and then applying some summary statistics. Radio count histograms can be produced from this notebook.


VAST_Source_Query_&_Analysis.ipynb - Loads in VAST Radio data for sources and appllies an ETA - V analysis to filter for highly variable, statistically significant sources. Also discusses duplicated sources in the catalogue.


FINK_Lightcurve_Plotting.ipynb - Code necessary to plot optical lightcurves and cutouts for a given sources. includes upper magnitude limits and bad quality cuts.


VAST_Lightcurve_Plotting.ipynb - Code necessary to plot radio lightcurves and cutouts for a given source. includes cutouts from multiple epochs at 887MHz


Combined_Lightcurve_Plotting.ipynb - This outlines how the optical and radio lightcurves can be plotted together on a common time axis, for visual inspection of time overlap and correlations between optical and radio trends. Also includes functions to plot their cutouts simultaneously.

Time_Correlation_Filter_Function - Notebook used to develop and demonstrate a written function that checks the crossmatch catalogue for sources that have good lightcurve overlap. 