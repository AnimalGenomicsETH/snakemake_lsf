#!/usr/bin/env python3
"""
sync-submit.py

Script to wrap bsub sync command for Snakemake. Uses the following job or
cluster parameters:

+ `threads`
+ `resources`
    - `mem_mb`: Expected memory requirements in megabytes. Overrides
      cluster.mem_mb
+ `cluster`
    - `mem_mb`: Memory that will be requested for the cluster for the job.
      Overriden by resources.mem_mb, if present.
      `resources`
    - `queue`: Which queue to run job on
    - `logdir`: Where to log stdout/stderr from cluster command
    - `output`: Name of stdout logfile
    - `error`: Name of stderr logfile
    - `jobname`: Job name (with wildcards)

Author: Michael B Hall
Adapted from: https://github.com/jaicher/snakemake-sync-bq-sub
"""

import sys
from pathlib import Path
from snakemake.utils import read_job_properties
from snakemake.shell import shell


DEFAULT_NAME = "jobname"


jobscript = sys.argv[-1]
job = read_job_properties(jobscript)
cluster = job.get("cluster", dict())

# get the group or rule name. If neither exists, use the DEFAULT_NAME
# NOTE: if group is present rule is not valid therefore group must come before rule
if job.get("type", "") == "group":
    name = job.get("groupid", "group") + "_" + job.get("jobid", "").split("-")[0]
else:
    name = job.get("rule", "") or DEFAULT_NAME

wildcards = job.get("wildcards", dict())
wildcards_str = ".".join("{}={}".format(k, v) for k, v in wildcards.items()) or "unique"

threads = job.get("threads", int({{cookiecutter.default_threads}}))
resources = job.get("resources", dict())
# get the memory usage in megabytes that we will request
mem_mb = resources.get(
    "mem_mb",  # first see if the job itself specifies the memory it needs
    # if not, check if the cluster configuration gives guidance
    cluster.get("mem_mb", int({{cookiecutter.default_mem_mb}})),
)

log_dir = Path(cluster.get("logdir", "{{cookiecutter.default_cluster_logdir}}"))
jobname = cluster.get("jobname", "{0}.{1}".format(name, wildcards_str))
out_log = str(log_dir / cluster.get("output", "{}.out".format(jobname)))
err_log = str(log_dir / cluster.get("error", "{}.err".format(jobname)))
queue = cluster.get("queue", "")


jobinfo_cmd = "-o {out_log:q} -e {err_log:q} -J {jobname:q}"
resources_cmd = (
    "-M {mem_mb} -n {threads} "
    "-R 'select[mem>{mem_mb}] rusage[mem={mem_mb}] span[hosts=1]'"
)
queue_cmd = "-q {queue}" if queue else ""
cluster_cmd = " ".join(sys.argv[1:-1])

# get command to do cluster sync
sync_cmd = "bsub -K"


# run commands
shell(
    sync_cmd
    + " "
    + resources_cmd
    + " "
    + jobinfo_cmd
    + " "
    + queue_cmd
    + " "
    + cluster_cmd
    + " {jobscript}"
)
