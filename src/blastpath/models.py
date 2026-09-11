from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Provenance(str, Enum):
    EXTRACTED = "extracted"
    INFERRED = "inferred"
    AMBIGUOUS = "ambiguous"


class NodeKind(str, Enum):
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    FILE = "file"


class Node(BaseModel):
    id: str
    kind: NodeKind
    name: str
    file: str
    line: int = 1
    qualname: Optional[str] = None


class Edge(BaseModel):
    src: str
    dst: str
    kind: str = "calls"
    provenance: Provenance = Provenance.EXTRACTED
    file: Optional[str] = None
    line: Optional[int] = None


class PathHop(BaseModel):
    src: str
    dst: str
    kind: str
    provenance: Provenance
    file: Optional[str] = None
    line: Optional[int] = None


class BlastReport(BaseModel):
    changed_files: list[str] = Field(default_factory=list)
    changed_symbols: list[str] = Field(default_factory=list)
    radius_nodes: list[str] = Field(default_factory=list)
    must_read: list[str] = Field(default_factory=list)
    god_hits: list[str] = Field(default_factory=list)
    hops: int = 2
    risk: int = 0
    paths: list[list[PathHop]] = Field(default_factory=list)
