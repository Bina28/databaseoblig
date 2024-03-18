import logging
import pathlib
import pytest
import requests
from kjoretoy import last_opp_kjoretoy, prepp_kjoretoy
from dotenv import load_dotenv
import os
import logging
import os
import pathlib
import pytest
import requests
from dotenv import load_dotenv
from kjoretoy import prepp_kjoretoy, last_opp_kjoretoy

logging.basicConfig(level=logging.DEBUG)

THIS_FOLDER = pathlib.Path(__file__).parent

load_dotenv(dotenv_path=THIS_FOLDER / "test.env")
connstr = os.environ.get("CONN")
TESTDATA = THIS_FOLDER / "testdata"

URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="session")
def db():
    df = prepp_kjoretoy(TESTDATA / "kjoretoyinfo_2022_jan.parquet")
    last_opp_kjoretoy(
        connstr,
        df
    )


def test_kjoretoy_pkkdato(db):
    # Adjusted URL to include the date as a path parameter
    pkkdato_endpoint = URL + "/pkkdato/"
    resp = requests.get(pkkdato_endpoint)
    svar = resp.json()

    forventet = [
        {
            'farge': 'Svart (også blåsvart, grafitt mørk, gråsort, koksgrå mørk, koksgrå mørk metallic)',
            'modell': '2008',
            'merke': 'PEUGEOT',
            'elbil': True,
            'registreringsdato': '2022-01-01',
            'neste_pkk_dato': '2026-01-01'
        }
    ]

    # Sort lists of dictionaries, specifying manual sorting using a lambda function
    sorterer = lambda x: (x["farge"], x["modell"], x["merke"], x["elbil"], x["registreringsdato"], x["neste_pkk_dato"])

    # Sort both lists
    forventet.sort(key=sorterer)
    svar.sort(key=sorterer)

    assert svar == forventet

    # Print expected values for verification
    print("Expected values:")
    for entry in forventet:
        print(entry)

    # Print actual values for verification
    print("Actual values:")
    for entry in svar:
        print(entry)
