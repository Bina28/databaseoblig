# Saksa fra tutorialen her: https://fastapi.tiangolo.com/tutorial/first-steps/
from idlelib.query import Query
from fastapi import FastAPI, Query, Path
from kjoretoy import kjoretoy_tabell
from dotenv import load_dotenv
from sqlalchemy import create_engine, literal, and_
import os

load_dotenv()
connstr = os.environ.get("CONN")
if connstr is None:
    connstr = "postgresql+psycopg2://postgres:mysecretpassword@localhost/postgres"

kjoretoy = kjoretoy_tabell()
engine = create_engine(connstr)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/regdato/{reg_date}")
async def regdato(reg_date: str = Path(..., description="Registration date in format YYYY-MM-DD")):
    with engine.connect() as conn:
        res = conn.execute(
            kjoretoy.select().with_only_columns(
                kjoretoy.c.farge_navn,
                kjoretoy.c.tekn_modell,
                kjoretoy.c.merke_navn,
                kjoretoy.c.tekn_drivstoff
            ).where(
                kjoretoy.c.tekn_reg_f_g_n == literal(reg_date)
            )
        )

        out_list = []
        for r in res:
            out = {}
            out["farge"] = r[0]
            out["modell"] = r[1]
            out["merke"] = r[2]
            out["elbil"] = r[3] == "5"
            out_list.append(out)

        return out_list


@app.get("/pkkdato")
async def pkkdato(pkk_date: str = Query("2026-01-01",  description="Next EU inspection date in format YYYY-MM-DD")):
    with engine.connect() as conn:
            res = conn.execute(
                    kjoretoy.select().with_only_columns(
                        kjoretoy.c.farge_navn,
                        kjoretoy.c.tekn_modell,
                        kjoretoy.c.merke_navn,
                        kjoretoy.c.tekn_drivstoff,
                        kjoretoy.c.tekn_reg_f_g_n,  # First registration date
                        kjoretoy.c.tekn_neste_pkk
                    ).where(
                        kjoretoy.c.tekn_neste_pkk == literal(pkk_date)
                    )
                )

            out_list = []
            for r in res:
                    out = {
                        "farge": r[0],
                        "modell": r[1],
                        "merke": r[2],
                        "elbil": r[3] == "5",  # Assuming "5" represents an electric vehicle
                        "registreringsdato": str(r[4]),  # Convert date to string
                        "neste_pkk_dato": str(r[5])  # Convert date to string
                    }
                    out_list.append(out)

                    return out_list


