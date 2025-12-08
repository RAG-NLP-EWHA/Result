#!/usr/bin/env python3
"""
Utility script for analyzing outputs from NLP and RAG systems.

This script provides basic analysis functionality for output files.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any


def load_output_file(filepath: str) -> Dict[str, Any]:
    """Load a single output file (JSON format)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_output(output_data: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a single output entry."""
    analysis = {
        'model': output_data.get('model', 'unknown'),
        'task': output_data.get('task', 'unknown'),
        'output_length': len(output_data.get('output', '')),
        'has_metadata': 'metadata' in output_data,
        'timestamp': output_data.get('timestamp', 'not provided')
    }
    return analysis


def analyze_directory(directory: str = 'outputs') -> List[Dict[str, Any]]:
    """Analyze all output files in a directory."""
    results = []
    output_dir = Path(directory)
    
    if not output_dir.exists():
        print(f"Directory {directory} does not exist.")
        return results
    
    json_files = list(output_dir.glob('*.json'))
    
    if not json_files:
        print(f"No JSON files found in {directory}")
        return results
    
    for filepath in json_files:
        try:
            data = load_output_file(filepath)
            analysis = analyze_output(data)
            analysis['filename'] = filepath.name
            results.append(analysis)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    return results


def print_summary(results: List[Dict[str, Any]]) -> None:
    """Print a summary of the analysis results."""
    if not results:
        print("No results to summarize.")
        return
    
    print(f"\n{'='*60}")
    print(f"Analysis Summary: {len(results)} file(s) analyzed")
    print(f"{'='*60}\n")
    
    for result in results:
        print(f"File: {result['filename']}")
        print(f"  Model: {result['model']}")
        print(f"  Task: {result['task']}")
        print(f"  Output Length: {result['output_length']} characters")
        print(f"  Timestamp: {result['timestamp']}")
        print()


if __name__ == '__main__':
    import sys
    
    # Default to 'outputs' directory, or use provided argument
    directory = sys.argv[1] if len(sys.argv) > 1 else 'outputs'
    
    print(f"Analyzing outputs in '{directory}' directory...")
    results = analyze_directory(directory)
    print_summary(results)
