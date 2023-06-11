#!/usr/bin/env python3

import os
import platform
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Literal, Optional, Union

try:
    import chromadb
    CHROMA_INSTALLED = True
except ModuleNotFoundError:
    CHROMA_INSTALLED = False