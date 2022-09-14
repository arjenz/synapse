#!/usr/bin/env python
# Copyright 2022 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Calculate the trial jobs to run based on if we're in a PR or not.

import json
import os

IS_PR = os.environ["GITHUB_REF"].startswith("refs/pull/")

# First calculate the various trial jobs.
#
# For each type of test we only run on Py3.7 on PRs

trial_sqlite_tests = [
    {
        "python-version": "3.7",
        "database": "sqlite",
        "extras": "all",
    }
]

if not IS_PR:
    trial_sqlite_tests.extend(
        {
            "python-version": version,
            "database": "sqlite",
            "extras": "all",
        }
        for version in ("3.8", "3.9", "3.10", "3.11-dev")
    )


trial_postgres_tests = [
    {
        "python-version": "3.11-dev",
        "database": "postgres",
        "postgres-version": "10",
        "extras": "all",
    }
]

if not IS_PR:
    trial_postgres_tests.append(
        {
            "python-version": "3.11-dev",
            "database": "postgres",
            "postgres-version": "14",
            "extras": "all",
        }
    )

trial_no_extra_tests = [
    {
        "python-version": "3.11-dev",
        "database": "sqlite",
        "extras": "",
    }
]

print("::group::Calculated trial jobs")
print(
    json.dumps(
        trial_sqlite_tests + trial_postgres_tests + trial_no_extra_tests, indent=4
    )
)
print("::endgroup::")

test_matrix = json.dumps(
    trial_sqlite_tests + trial_postgres_tests + trial_no_extra_tests
)
print(f"::set-output name=trial_test_matrix::{test_matrix}")


# First calculate the various sytest jobs.
#
# For each type of test we only run on focal on PRs


sytest_tests = [
    {
        "sytest-tag": "focal",
    },
    {
        "sytest-tag": "focal",
        "postgres": "postgres",
    },
    {
        "sytest-tag": "focal",
        "postgres": "multi-postgres",
        "workers": "workers",
    },
]

if not IS_PR:
    sytest_tests.extend(
        [
            {
                "sytest-tag": "testing",
                "postgres": "postgres",
            },
            {
                "sytest-tag": "buster",
                "postgres": "multi-postgres",
                "workers": "workers",
            },
        ]
    )


print("::group::Calculated sytest jobs")
print(json.dumps(sytest_tests, indent=4))
print("::endgroup::")

test_matrix = json.dumps(sytest_tests)
print(f"::set-output name=sytest_test_matrix::{test_matrix}")
