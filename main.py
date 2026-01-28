#!/usr/bin/env python3
"""
Entry point for local development.
Run with: python main.py
Or with uvicorn: uvicorn src.main:app --reload
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
