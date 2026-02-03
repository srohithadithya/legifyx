"""
Legifyx OCR Service
Optical Character Recognition for scanned documents and images
"""

import os
from pathlib import Path
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class OCRService:
    """
    OCR service for extracting text from images and scanned documents
    Supports multiple languages including Hindi and other Indian languages
    """
    
    SUPPORTED_LANGUAGES = {
        'eng': 'English',
        'hin': 'Hindi',
        'tam': 'Tamil',
        'tel': 'Telugu',
        'kan': 'Kannada',
        'mal': 'Malayalam',
        'mar': 'Marathi',
        'guj': 'Gujarati',
        'ben': 'Bengali',
        'pan': 'Punjabi'
    }
    
    def __init__(self, tesseract_path: str = None):
        """
        Initialize OCR service
        
        Args:
            tesseract_path: Path to Tesseract executable (optional)
        """
        self.tesseract_available = False
        
        try:
            import pytesseract
            
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
            
            # Test if Tesseract is available
            pytesseract.get_tesseract_version()
            self.tesseract_available = True
            self.pytesseract = pytesseract
            
        except Exception as e:
            logger.warning(f"Tesseract not available: {e}")
    
    def extract_text(
        self,
        image_path: str,
        languages: str = 'eng+hin',
        preprocess: bool = True
    ) -> Tuple[str, dict]:
        """
        Extract text from an image file
        
        Args:
            image_path: Path to the image file
            languages: OCR languages (Tesseract format, e.g., 'eng+hin')
            preprocess: Whether to preprocess the image for better OCR
        
        Returns:
            Tuple of (extracted_text, metadata)
        """
        if not self.tesseract_available:
            return "", {"error": "Tesseract not available"}
        
        try:
            from PIL import Image
            import PIL.ImageOps
            
            # Load image
            image = Image.open(image_path)
            
            # Preprocess if requested
            if preprocess:
                image = self._preprocess_image(image)
            
            # Perform OCR
            text = self.pytesseract.image_to_string(
                image,
                lang=languages,
                config='--psm 1 --oem 3'  # Automatic page segmentation with LSTM OCR
            )
            
            # Get additional data
            data = self.pytesseract.image_to_data(
                image,
                lang=languages,
                output_type=self.pytesseract.Output.DICT
            )
            
            # Calculate confidence
            confidences = [int(c) for c in data['conf'] if int(c) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            metadata = {
                "languages": languages,
                "word_count": len(text.split()),
                "confidence": round(avg_confidence, 2),
                "image_size": image.size,
                "preprocessed": preprocess
            }
            
            return text.strip(), metadata
            
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return "", {"error": str(e)}
    
    def _preprocess_image(self, image):
        """
        Preprocess image for better OCR results
        
        Args:
            image: PIL Image object
        
        Returns:
            Preprocessed PIL Image
        """
        from PIL import Image, ImageEnhance, ImageFilter
        
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Apply slight sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        # Resize if too small
        width, height = image.size
        if width < 1000:
            scale = 1000 / width
            new_size = (int(width * scale), int(height * scale))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image
    
    def extract_from_pdf_images(
        self,
        pdf_path: str,
        languages: str = 'eng+hin',
        dpi: int = 300
    ) -> Tuple[str, dict]:
        """
        Extract text from a scanned PDF using OCR
        
        Args:
            pdf_path: Path to the PDF file
            languages: OCR languages
            dpi: Resolution for PDF to image conversion
        
        Returns:
            Tuple of (extracted_text, metadata)
        """
        if not self.tesseract_available:
            return "", {"error": "Tesseract not available"}
        
        try:
            from pdf2image import convert_from_path
            
            # Convert PDF pages to images
            images = convert_from_path(pdf_path, dpi=dpi)
            
            all_text = []
            page_metadata = []
            
            for i, image in enumerate(images):
                # Save temporarily
                temp_path = f"temp_page_{i}.png"
                image.save(temp_path)
                
                # Extract text
                text, meta = self.extract_text(temp_path, languages)
                all_text.append(f"--- Page {i + 1} ---\n{text}")
                page_metadata.append(meta)
                
                # Clean up
                os.remove(temp_path)
            
            combined_text = "\n\n".join(all_text)
            
            metadata = {
                "total_pages": len(images),
                "languages": languages,
                "dpi": dpi,
                "pages": page_metadata
            }
            
            return combined_text, metadata
            
        except ImportError:
            logger.error("pdf2image not installed")
            return "", {"error": "pdf2image library not available"}
        except Exception as e:
            logger.error(f"PDF OCR failed: {e}")
            return "", {"error": str(e)}
    
    def detect_document_language(self, image_path: str) -> str:
        """
        Attempt to detect the primary language of a document
        
        Args:
            image_path: Path to the image
        
        Returns:
            Detected language code
        """
        if not self.tesseract_available:
            return 'eng'
        
        try:
            from PIL import Image
            
            image = Image.open(image_path)
            
            # Try OCR with multiple languages
            osd = self.pytesseract.image_to_osd(image)
            
            # Parse the output for script detection
            for line in osd.split('\n'):
                if 'Script:' in line:
                    script = line.split(':')[1].strip()
                    script_map = {
                        'Latin': 'eng',
                        'Devanagari': 'hin',
                        'Tamil': 'tam',
                        'Telugu': 'tel'
                    }
                    return script_map.get(script, 'eng')
            
            return 'eng'
            
        except Exception:
            return 'eng'
    
    def is_available(self) -> bool:
        """Check if OCR service is available"""
        return self.tesseract_available
    
    def get_available_languages(self) -> list:
        """Get list of available OCR languages"""
        if not self.tesseract_available:
            return []
        
        try:
            langs = self.pytesseract.get_languages()
            return langs
        except:
            return list(self.SUPPORTED_LANGUAGES.keys())
