"""CRUD functions called by path operations."""
import os

import httpx
from fastapi import HTTPException

from . import utility as util


async def get(age_min: float, age_max: float, sex: str, image_modal: str):
    """
    Makes a POST request to Stardog API using httpx where the payload is a SPARQL query generated by the create_query function.

    Parameters
    ----------
    age_min : float
        Minimum age of subject.
    age_max : float
        Maximum age of subject.
    sex : str
        Sex of subject.
    image_modal: str
        Imaging modality of subject scans.

    Returns
    -------
    httpx.response
        Response of the POST request.

    """
    response = httpx.post(
        url=util.QUERY_URL,
        content=util.create_query(
            age=(age_min, age_max), sex=sex, image_modal=image_modal
        ),
        headers=util.QUERY_HEADER,
        auth=httpx.BasicAuth(
            os.environ.get("USER"), os.environ.get("PASSWORD")
        ),
    )

    try:
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.response.text
        )

    results = response.json()

    return [
        {k: v["value"] for k, v in res.items()}
        for res in results["results"]["bindings"]
    ]
