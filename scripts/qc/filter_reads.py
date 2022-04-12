import os
import subprocess
from collections import OrderedDict

original = int(str(subprocess.getoutput(
    "zcat {} | wc -l".format(snakemake.input.reads))).strip())//4
host = int(subprocess.getoutput(
    "cat {} | wc -l".format(snakemake.input.hostreads)).strip())
nonhost = int(original-host)
os.system("""
gzip -dc {a} | \
rbt fastq-filter {b} | \
gzip > {c}
""".format(a=snakemake.input.reads, b=snakemake.input.hostreads, c=snakemake.output.reads))

hostdict = OrderedDict()
for hostid in snakemake.input.hostids:
    hostname = os.path.basename(os.path.dirname(hostid))
    hostcts = int(subprocess.getoutput("cat {} | wc -l".format(hostid)).strip())
    hostdict[hostname] = hostcts

with open(snakemake.output.log, 'w') as log:
    log.write("{}\n".format("\t".join(list(hostdict.keys()) + ["host","nonhost"] )))
    log.write("{}\n".format("\t".join( map(str, list(hostdict.values()) + [host, nonhost]) )))