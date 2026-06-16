"""
TTB AI Alcohol Label Verification Engine - Data Ingestion Layer
Orchestrates ingestion protocols, vector asset transformation (PDF rasterization),
and optical character recognition (OCR) parsing via unified vision controllers.
"""

import os
import sys
import platform
import numpy as np
from pdf2image import convert_from_path

# Ingest centralized configuration architectures
try:
    from config import AppConfig, logger
except ImportError as e:
    print(f"CRITICAL: Failed to load core configuration context in ingestion layer. Error: {e}")
    sys.exit(1)

# Structural encapsulation for engine instantiation
_reader_instance = None

def _get_ocr_reader():
    """
    Ensures safe initialization of the optical character recognition model backend,
    preventing arbitrary memory allocations during ambient module compilation.
    """
    global _reader_instance
    if _reader_instance is None:
        try:
            import easyocr
            logger.info("Initializing Computer Vision Engine: Instantiating EasyOCR Reader Baseline...")
            # Enforce CPU execution constraints via configuration contexts
            _reader_instance = easyocr.Reader(['en'], gpu=False)
            logger.info("Computer Vision Engine: Reader instance compiled successfully.")
        except Exception as e:
            logger.critical(f"INGESTION LAYER FAILURE: Failed to instantiate vision model library. Context: {e}")
            raise e
    return _reader_instance


def extract_text_from_image(file_path: str) -> list:
    """
    Ingests target asset paths, evaluates file extensions, transforms vector 
    structures to pixel matrices, and routes arrays to the computer vision backend.
    """
    logger.info(f"Ingestion Pipeline: Initiating character extraction suite for target asset -> '{file_path}'")
    
    try:
        # 1. Handle Vector Asset Parsing (PDF Transformation Boundary)
        if file_path.lower().endswith('.pdf'):
            logger.info("Ingestion Pipeline: PDF Vector Asset detected. Invoking rasterization driver...")
            
            # Cross-platform environment resolution for underlying binary binaries
            if platform.system() == "Windows":
                poppler_bin = r'C:\treasury-ai-governance_label-verification-project\poppler\poppler-26.02.0\Library\bin'
                if not os.path.exists(poppler_bin):
                    logger.warning(f"FS Topology Discrepancy: Target Poppler binary directory missing at '{poppler_bin}'")
                pages = convert_from_path(file_path, poppler_path=poppler_bin)
            else:
                # Linux/GitHub Codespaces environments utilize system-level poppler-utils automatically via PATH
                pages = convert_from_path(file_path)
            
            if not pages:
                raise ValueError("Vector Asset Transformation Error: Resulting page matrix array is empty.")
                
            logger.info("Ingestion Pipeline: Page [0] isolated. Mapping vector to pixel array context.")
            image_input = np.array(pages[0])
            
        else:
            logger.info("Ingestion Pipeline: Image binary asset detected. Mapping directly to data layer input array.")
            image_input = file_path 

        # 2. Invoke Machine Vision Parser Lifecycle
        vision_client = _get_ocr_reader()
        logger.info("Computer Vision Engine: Processing target data stream tokens...")
        raw_token_results = vision_client.readtext(image_input, detail=1)
        
        logger.info(f"Computer Vision Engine: Ingestion finalized. Extracted {len(raw_token_results)} character text tokens.")
        return raw_token_results

    except Exception as e:
        logger.error(f"INGESTION LAYER FAILURE: Exception flagged inside raw character extraction loop. Context: {str(e)}")
        raise e


def analyze_label(file_path: str) -> list:
    """
    Transforms raw machine vision extraction matrices into structured, self-documenting 
    dictionaries optimized for downstream validation against federal business rules.
    """
    try:
        raw_results = extract_text_from_image(file_path)
        
        structured_data = []
        for bbox, text, conf in raw_results:
            structured_data.append({
                "text": str(text).strip(),
                "bbox": bbox,
                "confidence": float(conf)  # Normalizes numpy float primitives to native python floats
            })
            
        return structured_data
        
    except Exception as e:
        logger.error(f"PIPELINE REGRESSION: Aborting data normalization layer inside 'analyze_label'. Error: {str(e)}")
        raise e