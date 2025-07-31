"""
Vercel entry point for the Appear‑AI backend.

This module exposes the FastAPI `app` instance so that Vercel's Python
runtime can serve it.  We import the existing FastAPI app from the
``appear_ai_backend.app`` module and assign it to a top‑level variable
named ``app``.  Vercel looks for this name when deploying Python
applications.

The ``vercel.json`` configuration in this repository specifies that
Vercel should use the Python runtime for this file and route all
requests to it.

See https://vercel.com/docs/runtimes#python for more details on
deploying Python apps on Vercel.
"""

from appear_ai_backend.app import app as app  # re‑export FastAPI app

# Note: No additional code is necessary here.  The `app` object will be
# picked up by Vercel and served as the ASGI application.