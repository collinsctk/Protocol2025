#!/bin/bash

set -e

influx <<-EOSQL
create retention policy "qytdb_rp_policy" on "qytdb" duration 3w replication 1 default
EOSQL