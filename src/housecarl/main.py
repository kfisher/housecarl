# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

"""
"""

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    """
    """
    return {"message": "Hello World"}
