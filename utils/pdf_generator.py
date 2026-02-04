"""
Legifyx PDF Report Generator
Generate professional PDF reports for legal review
"""

from pathlib import Path
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generate PDF reports from analysis results"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "exports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _clean_text(self, text: str) -> str:
        """Clean and escape text for ReportLab Paragraphs"""
        if not text:
            return ""
        
        # Basic XML escaping
        import html
        text = html.escape(text)
        
        # Restore some basic formatting that Paragraph supports
        # Handle line breaks
        text = text.replace('\n', '<br/>')
        
        # Handle Bold (Markdown style **text**)
        # Using a simple approach for now
        import re
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        
        # Handle Headers (### Header)
        text = re.sub(r'###\s*(.*?)(?:<br/>|$)', r'<b>\1</b><br/>', text)
        
        return text

    def generate_report(self, analysis_result, output_filename: str = None) -> Optional[str]:
        """
        Generate comprehensive PDF report
        """
        if not output_filename:
            output_filename = f"legifyx_report_{analysis_result.contract_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        output_path = self.output_dir / output_filename
        
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.platypus import PageBreak
            
            doc = SimpleDocTemplate(str(output_path), pagesize=A4,
                                   leftMargin=0.75*inch, rightMargin=0.75*inch,
                                   topMargin=0.75*inch, bottomMargin=0.75*inch)
            
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle('Title', parent=styles['Heading1'],
                                        fontSize=24, textColor=colors.HexColor('#1E3A5F'),
                                        spaceAfter=20)
            
            heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'],
                                          fontSize=14, textColor=colors.HexColor('#1E3A5F'),
                                          spaceBefore=15, spaceAfter=10)
            
            body_style = ParagraphStyle('Body', parent=styles['Normal'],
                                       fontSize=10, leading=14)
            
            elements = []
            
            # Header
            elements.append(Paragraph("LEGIFYX", title_style))
            elements.append(Paragraph("Contract Analysis Report", styles['Heading2']))
            elements.append(Spacer(1, 20))
            
            # Metadata table
            meta_data = [
                ["Contract ID:", analysis_result.contract_id],
                ["Analysis Date:", analysis_result.analysis_timestamp],
                ["Contract Type:", analysis_result.contract_type],
                ["Word Count:", str(analysis_result.word_count)],
                ["Language:", analysis_result.language.upper()]
            ]
            
            # Clean metadata values
            for i in range(len(meta_data)):
                meta_data[i][1] = str(meta_data[i][1])
            
            meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
            meta_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(meta_table)
            elements.append(Spacer(1, 20))
            
            # Risk Summary
            elements.append(Paragraph("Risk Assessment Summary", heading_style))
            
            if analysis_result.risk_result:
                risk = analysis_result.risk_result
                risk_color = {
                    'low': colors.HexColor('#2E7D32'),
                    'medium': colors.HexColor('#F9A825'),
                    'high': colors.HexColor('#E65100'),
                    'critical': colors.HexColor('#C62828')
                }.get(risk.risk_level.value, colors.black)
                
                risk_data = [
                    ["Overall Risk Score:", f"{risk.overall_score}/10"],
                    ["Risk Level:", risk.risk_level.value.upper()],
                    ["Critical Issues:", str(len(risk.critical_issues))],
                    ["Warnings:", str(len(risk.warnings))]
                ]
                
                risk_table = Table(risk_data, colWidths=[2*inch, 4*inch])
                risk_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('TEXTCOLOR', (1, 1), (1, 1), risk_color),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(risk_table)
            
            elements.append(Spacer(1, 20))
            
            # Executive Summary
            try:
                elements.append(Paragraph("Executive Summary", heading_style))
                summary_html = self._clean_text(analysis_result.executive_summary)
                elements.append(Paragraph(summary_html, body_style))
            except Exception as e:
                logger.error(f"Error adding summary: {e}")
                elements.append(Paragraph("[Summary data error]", body_style))
            
            elements.append(Spacer(1, 15))
            
            # Critical Clauses
            if analysis_result.critical_clauses:
                try:
                    elements.append(Paragraph("Critical Clauses Requiring Attention", heading_style))
                    for clause in analysis_result.critical_clauses[:10]:
                        cleaned_clause = self._clean_text(clause.get('text', 'No text available'))
                        clause_id = clause.get('clause_id', 'Unknown')
                        risk_lvl = clause.get('risk_level', 'unknown').upper()
                        clause_html = f"<b>Clause {clause_id}</b> (Risk: {risk_lvl})<br/>{cleaned_clause}"
                        elements.append(Paragraph(clause_html, body_style))
                        elements.append(Spacer(1, 10))
                except Exception as e:
                    logger.error(f"Error adding clauses: {e}")
            
            # Recommendations
            if analysis_result.recommendations:
                try:
                    if len(elements) > 15: # Add page break if many elements
                        elements.append(PageBreak())
                    elements.append(Paragraph("Recommendations", heading_style))
                    for i, rec in enumerate(analysis_result.recommendations, 1):
                        cleaned_rec = self._clean_text(rec)
                        elements.append(Paragraph(f"{i}. {cleaned_rec}", body_style))
                    elements.append(Spacer(1, 15))
                except Exception as e:
                    logger.error(f"Error adding recommendations: {e}")
            
            # Plain Language Summary
            try:
                elements.append(Paragraph("Plain Language Summary", heading_style))
                plain_html = self._clean_text(analysis_result.plain_language_summary)
                elements.append(Paragraph(plain_html, body_style))
            except Exception as e:
                logger.error(f"Error adding plain summary: {e}")
            
            # Footer
            elements.append(Spacer(1, 30))
            footer_text = f"<i>Generated by Legifyx on {datetime.now().strftime('%Y-%m-%d %H:%M')}. This report is for informational purposes only and does not constitute legal advice.</i>"
            elements.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=body_style, fontSize=8, textColor=colors.gray)))
            doc.build(elements)
            return str(output_path)
            
        except ImportError:
            logger.error("ReportLab not installed. Run: pip install reportlab")
            return None
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def generate_summary_pdf(self, summary_text: str, contract_id: str) -> Optional[str]:
        """Generate a simple summary PDF"""
        output_path = self.output_dir / f"summary_{contract_id}.pdf"
        
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
            
            c = canvas.Canvas(str(output_path), pagesize=A4)
            width, height = A4
            
            c.setFont("Helvetica-Bold", 20)
            c.drawString(50, height - 50, "LEGIFYX - Contract Summary")
            
            c.setFont("Helvetica", 11)
            y = height - 100
            
            for line in summary_text.split('\n'):
                if y < 50:
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, line[:100])
                y -= 15
            
            c.save()
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Summary PDF failed: {e}")
            return None
