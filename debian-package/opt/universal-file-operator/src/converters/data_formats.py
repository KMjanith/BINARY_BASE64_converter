"""
Data Format Converters
======================

This module implements conversions between common data formats like JSON, XML, CSV, and YAML.
These converters handle structured data transformation commonly used in:
- API data exchange
- Configuration files  
- Data import/export
- Web services communication

Learning Concepts:
- JSON parsing and generation
- XML processing
- CSV handling with proper escaping
- YAML serialization
- Data validation and error handling
"""

import json
import csv
import io
from typing import Union, Any, Dict, List
import logging

from .base_converter import ReversibleConverter
from .registry import register_converter
from ..utils.exceptions import ConversionError, ValidationError

logger = logging.getLogger(__name__)

# Optional YAML support
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    logger.warning("PyYAML not installed - YAML conversions will be unavailable")

# XML parsing
try:
    import xml.etree.ElementTree as ET
    from xml.dom import minidom
    XML_AVAILABLE = True
except ImportError:
    XML_AVAILABLE = False


@register_converter('json', 'dict', 'Parse JSON string to Python dictionary', reversible=True)
class JsonDictConverter(ReversibleConverter):
    """
    Convert between JSON string and Python dictionary.
    
    This is useful for:
    - API response processing
    - Configuration file parsing
    - Data serialization/deserialization
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('json', 'dict', 'Convert JSON string to/from Python dictionary')
    
    def validate_input(self, data: Any) -> None:
        """Validate input data."""
        super().validate_input(data)
        
        if self.from_format == 'json' and not isinstance(data, str):
            raise ValidationError(f"JSON input requires string, got {type(data).__name__}")
        elif self.from_format == 'dict' and not isinstance(data, (dict, list)):
            raise ValidationError(f"Dict input requires dict or list, got {type(data).__name__}")
    
    def _convert_a_to_b(self, data: str, **options) -> Union[Dict, List]:
        """Convert JSON string to Python dictionary/list."""
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise ConversionError(f"Invalid JSON: {e}", original_error=e)
        except Exception as e:
            raise ConversionError(f"Failed to parse JSON: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: Union[Dict, List], **options) -> str:
        """Convert Python dictionary/list to JSON string."""
        try:
            # Options for JSON formatting
            indent = options.get('indent', None)
            sort_keys = options.get('sort_keys', False)
            ensure_ascii = options.get('ensure_ascii', True)
            
            return json.dumps(data, 
                            indent=indent, 
                            sort_keys=sort_keys, 
                            ensure_ascii=ensure_ascii,
                            default=str)  # Convert non-serializable objects to strings
        except Exception as e:
            raise ConversionError(f"Failed to serialize to JSON: {e}", original_error=e)


@register_converter('csv', 'dict_list', 'Parse CSV to list of dictionaries', reversible=True)
class CsvDictConverter(ReversibleConverter):
    """
    Convert between CSV string and list of dictionaries.
    
    Each row becomes a dictionary with column headers as keys.
    Useful for:
    - Spreadsheet data processing
    - Database export/import
    - Data analysis preparation
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('csv', 'dict_list', 'Convert CSV to/from list of dictionaries')
    
    def validate_input(self, data: Any) -> None:
        """Validate input data."""
        super().validate_input(data)
        
        if self.from_format == 'csv' and not isinstance(data, str):
            raise ValidationError(f"CSV input requires string, got {type(data).__name__}")
        elif self.from_format == 'dict_list' and not isinstance(data, list):
            raise ValidationError(f"Dict list input requires list, got {type(data).__name__}")
    
    def _convert_a_to_b(self, data: str, **options) -> List[Dict]:
        """Convert CSV string to list of dictionaries."""
        try:
            # Options for CSV parsing
            delimiter = options.get('delimiter', ',')
            quotechar = options.get('quotechar', '"')
            has_header = options.get('has_header', True)
            
            # Create CSV reader
            csv_file = io.StringIO(data)
            
            if has_header:
                reader = csv.DictReader(csv_file, delimiter=delimiter, quotechar=quotechar)
                return list(reader)
            else:
                # No header - create numbered columns
                reader = csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar)
                rows = list(reader)
                if not rows:
                    return []
                
                # Create column names (col0, col1, etc.)
                num_cols = len(rows[0])
                fieldnames = [f'col{i}' for i in range(num_cols)]
                
                result = []
                for row in rows:
                    # Pad row if needed
                    padded_row = row + [''] * (num_cols - len(row))
                    result.append(dict(zip(fieldnames, padded_row)))
                
                return result
                
        except Exception as e:
            raise ConversionError(f"Failed to parse CSV: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: List[Dict], **options) -> str:
        """Convert list of dictionaries to CSV string."""
        try:
            if not data:
                return ""
            
            # Options for CSV generation
            delimiter = options.get('delimiter', ',')
            quotechar = options.get('quotechar', '"')
            include_header = options.get('include_header', True)
            
            # Get fieldnames from first dictionary
            fieldnames = list(data[0].keys()) if data else []
            
            # Create CSV writer
            csv_file = io.StringIO()
            writer = csv.DictWriter(csv_file, 
                                  fieldnames=fieldnames, 
                                  delimiter=delimiter,
                                  quotechar=quotechar,
                                  quoting=csv.QUOTE_MINIMAL)
            
            if include_header:
                writer.writeheader()
            
            writer.writerows(data)
            return csv_file.getvalue()
            
        except Exception as e:
            raise ConversionError(f"Failed to generate CSV: {e}", original_error=e)


@register_converter('query_string', 'dict', 'Parse URL query string to dictionary', reversible=True)
class QueryStringDictConverter(ReversibleConverter):
    """
    Convert between URL query strings and dictionaries.
    
    Examples:
    - "name=John&age=30" <-> {"name": "John", "age": "30"}
    - "tags=python&tags=web" <-> {"tags": ["python", "web"]}
    """
    
    def __init__(self, from_format: str, to_format: str):
        super().__init__('query_string', 'dict', 'Convert query string to/from dictionary')
    
    def _convert_a_to_b(self, data: str, **options) -> Dict:
        """Convert query string to dictionary."""
        try:
            import urllib.parse
            
            # Options
            keep_blank_values = options.get('keep_blank_values', False)
            strict_parsing = options.get('strict_parsing', False)
            
            # Parse query string
            parsed = urllib.parse.parse_qs(data, 
                                         keep_blank_values=keep_blank_values,
                                         strict_parsing=strict_parsing)
            
            # Flatten single-item lists
            result = {}
            for key, value_list in parsed.items():
                if len(value_list) == 1:
                    result[key] = value_list[0]
                else:
                    result[key] = value_list
            
            return result
            
        except Exception as e:
            raise ConversionError(f"Failed to parse query string: {e}", original_error=e)
    
    def _convert_b_to_a(self, data: Dict, **options) -> str:
        """Convert dictionary to query string."""
        try:
            import urllib.parse
            
            # Options
            quote_via = options.get('quote_via', urllib.parse.quote_plus)
            
            pairs = []
            for key, value in data.items():
                if isinstance(value, list):
                    # Multiple values for same key
                    for item in value:
                        pairs.append(f"{quote_via(str(key))}={quote_via(str(item))}")
                else:
                    pairs.append(f"{quote_via(str(key))}={quote_via(str(value))}")
            
            return "&".join(pairs)
            
        except Exception as e:
            raise ConversionError(f"Failed to generate query string: {e}", original_error=e)


# YAML converter (if PyYAML is available)
if YAML_AVAILABLE:
    @register_converter('yaml', 'dict', 'Parse YAML to Python dictionary', reversible=True)
    class YamlDictConverter(ReversibleConverter):
        """
        Convert between YAML and Python dictionary.
        
        YAML is commonly used for:
        - Configuration files
        - Docker Compose files
        - Kubernetes manifests
        - Documentation
        """
        
        def __init__(self, from_format: str, to_format: str):
            super().__init__('yaml', 'dict', 'Convert YAML to/from Python dictionary')
        
        def _convert_a_to_b(self, data: str, **options) -> Union[Dict, List]:
            """Convert YAML string to Python dictionary/list."""
            try:
                # Options for YAML loading
                safe_load = options.get('safe_load', True)
                
                if safe_load:
                    return yaml.safe_load(data)
                else:
                    return yaml.load(data, Loader=yaml.FullLoader)
                    
            except yaml.YAMLError as e:
                raise ConversionError(f"Invalid YAML: {e}", original_error=e)
            except Exception as e:
                raise ConversionError(f"Failed to parse YAML: {e}", original_error=e)
        
        def _convert_b_to_a(self, data: Union[Dict, List], **options) -> str:
            """Convert Python dictionary/list to YAML string."""
            try:
                # Options for YAML dumping
                default_flow_style = options.get('default_flow_style', False)
                indent = options.get('indent', 2)
                
                return yaml.dump(data, 
                               default_flow_style=default_flow_style,
                               indent=indent,
                               allow_unicode=True)
                               
            except Exception as e:
                raise ConversionError(f"Failed to serialize to YAML: {e}", original_error=e)


# Simple XML converter (basic functionality)
if XML_AVAILABLE:
    @register_converter('xml', 'dict', 'Parse simple XML to dictionary')
    class SimpleXmlDictConverter(ReversibleConverter):
        """
        Convert between simple XML and Python dictionary.
        
        Note: This is a basic implementation for simple XML structures.
        Complex XML with namespaces, attributes, etc. may need specialized handling.
        """
        
        def __init__(self, from_format: str, to_format: str):
            super().__init__('xml', 'dict', 'Convert simple XML to/from dictionary')
        
        def _xml_to_dict(self, element):
            """Recursively convert XML element to dictionary."""
            result = {}
            
            # Handle attributes
            if element.attrib:
                result['@attributes'] = element.attrib
            
            # Handle text content
            if element.text and element.text.strip():
                if len(element) == 0:  # No child elements
                    return element.text.strip()
                else:
                    result['#text'] = element.text.strip()
            
            # Handle child elements
            for child in element:
                child_data = self._xml_to_dict(child)
                if child.tag in result:
                    # Multiple elements with same tag - convert to list
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = child_data
            
            return result if result else None
        
        def _convert_a_to_b(self, data: str, **options) -> Dict:
            """Convert XML string to dictionary."""
            try:
                root = ET.fromstring(data)
                return {root.tag: self._xml_to_dict(root)}
                
            except ET.ParseError as e:
                raise ConversionError(f"Invalid XML: {e}", original_error=e)
            except Exception as e:
                raise ConversionError(f"Failed to parse XML: {e}", original_error=e)
        
        def _dict_to_xml(self, data, root_name='root'):
            """Convert dictionary to XML element."""
            if isinstance(data, dict):
                element = ET.Element(root_name)
                
                for key, value in data.items():
                    if key == '@attributes':
                        element.attrib.update(value)
                    elif key == '#text':
                        element.text = str(value)
                    else:
                        if isinstance(value, list):
                            for item in value:
                                child = self._dict_to_xml(item, key)
                                element.append(child)
                        else:
                            child = self._dict_to_xml(value, key)
                            element.append(child)
                
                return element
            else:
                # Simple value
                element = ET.Element(root_name)
                element.text = str(data)
                return element
        
        def _convert_b_to_a(self, data: Dict, **options) -> str:
            """Convert dictionary to XML string."""
            try:
                # Options
                pretty_print = options.get('pretty_print', True)
                root_name = options.get('root_name', 'root')
                
                # Handle case where dict has single root element
                if len(data) == 1:
                    root_key, root_value = next(iter(data.items()))
                    root_element = self._dict_to_xml(root_value, root_key)
                else:
                    root_element = self._dict_to_xml(data, root_name)
                
                if pretty_print:
                    # Pretty print the XML
                    xml_str = ET.tostring(root_element, encoding='unicode')
                    dom = minidom.parseString(xml_str)
                    return dom.toprettyxml(indent="  ", encoding=None)
                else:
                    return ET.tostring(root_element, encoding='unicode')
                    
            except Exception as e:
                raise ConversionError(f"Failed to serialize to XML: {e}", original_error=e)