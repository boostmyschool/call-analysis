#!/usr/bin/env python

import sys

from src.cold_call_collection import ColdCallCollection
from src.graph_server import GraphServer

def run_analysis(csv_path):
    calls = ColdCallCollection.import_from_csv(csv_path)
    server = GraphServer(calls=calls)
    server.run_server()

if __name__ == "__main__":
    run_analysis(sys.argv[1])
