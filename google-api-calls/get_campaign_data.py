#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example illustrates how to get all campaigns.

To add campaigns, run add_campaigns.py.
"""


import argparse
import pathlib
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START get_campaigns]
def main(client: GoogleAdsClient, customer_id: str):
    ga_service = client.get_service("GoogleAdsService")

    # put all of the fields that you want to fetch in this list
    fields = [
        "campaign.id",
        "campaign.name",
        "campaign.status",
        "campaign.start_date",
        "campaign.end_date",
        "campaign_budget.amount_micros",
    ]

    query = f"""
        SELECT {', '.join(fields)}
        FROM campaign
        ORDER BY campaign.id"""

    rows = []

    # Issues a search request using streaming.
    stream = ga_service.search_stream(customer_id=customer_id, query=query)
    for batch in stream:
        for row in batch.results:
            # convert the rows into a list of dictionaries
            data = {}
            for field in fields:
                field_start, field_end = field.split(".")
                data[field_end] = getattr(getattr(row, field_start), field_end)

            rows.append(data)
            # [END get_campaigns]

    # the rows can be converted into a JSON string by calling json.dumps(rows)
    print(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Lists all campaigns for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    conf_file_exists = pathlib.Path("./google-ads.yaml").exists()

    googleads_client = GoogleAdsClient.load_from_storage(
        path=("google-ads.yaml" if conf_file_exists else None), version="v16"
    )

    try:
        main(googleads_client, args.customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
