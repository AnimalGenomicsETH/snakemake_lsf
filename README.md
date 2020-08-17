## Custom snakemake config

Some basic config stuff for easier snakemake calling on Leonhard

## Install
To install, first clone the repo into the ~/.config/snakemake directory
```
git clone https://github.com/ASLeonard/snakemake_lsf.git
```

then run snakemake as 
```
snakemake --profile "snakemake_lsf"

## Differences

- walltime
  - minute/hour format 
- disk_scratch
  - $TMPDIR
- log structure
