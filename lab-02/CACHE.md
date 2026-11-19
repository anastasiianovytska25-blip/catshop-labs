# Cache

What: pip's downloads, through `actions/setup-python` with `cache: pip`. The key is a hash of `lab-02/requirements*.txt`, so it changes when a dependency changes.

cold run (run #1, no cache yet): test job 15s
warm run (run #3, cache restored): test job 9s

What got faster: pip took the packages from the restored cache instead of downloading them from PyPI.
