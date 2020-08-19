# Custom snakemake config

Some basic config stuff for easier snakemake calling on Leonhard

## Install
To install, make a directory in the home config folder
```
mkdir -p ~/.config/snakemake
```
and then clone the repo into that directory
```
cd ~/.config/snakemake && git clone https://github.com/ASLeonard/snakemake_lsf.git
```

## Usage
In theory, can then just run snakemake as 
```
snakemake --profile "snakemake_lsf"
```
There may be some changes necessary if you require conda etc, which can be edited in config.yaml

## Differences
Some new options were added
- Under **resources:**
  - walltime = "hours:minutes"
  - disk_scratch = N (in units of mb)
    - accessible only via the $TMPDIR variable 
    - $TMPDIR only survives for the duration of **that** rule
- **log** structure
  - generally logs/{rule}/{wildcard_info}
- Option to modify further for GPU or other specifics

### example
An example which needs 8 hours and 30GB local-node storage for the output
```
rule assembler_hifiasm:
    input:
        'data/{animal}.hifi.fq.gz'
    output:
        'hifiasm/{animal}.asm.p_ctg.gfa'
    threads: 24
    resources:
        mem_mb = 6000,
        walltime = "8:00",
        disk_scratch = 30000
    shell: 'hifiasm -o $TMPDIR -t {threads} {input}; some other job using $TMPDIR'
```
