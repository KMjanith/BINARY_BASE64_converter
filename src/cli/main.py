"""
Command Line Interface for Universal File Operator
===================================================

This module provides a user-friendly CLI using the Click framework.
It demonstrates command-line argument parsing, subcommands, and interactive usage.

Learning Concepts:
- Click framework for CLI development
- Command-line argument parsing and validation
- Subcommands and command groups
- Interactive user input
- Error handling in CLI applications
- Progress bars and rich console output
"""

import click
import sys
from pathlib import Path
from typing import Optional
import logging

# Rich for beautiful output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress
    from rich.text import Text
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None

# Import our converter system
try:
    from ..converters.registry import get_global_registry, convert, list_conversions
    from ..utils.exceptions import ConversionError, UnsupportedFormatError, ValidationError
except ImportError:
    # Handle relative import issues during development
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.converters.registry import get_global_registry, convert, list_conversions
    from src.utils.exceptions import ConversionError, UnsupportedFormatError, ValidationError


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    """
    Universal File Operator - Convert between various data formats.
    
    This tool supports bidirectional conversions between text encodings,
    data formats, number bases, and more.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    setup_logging(verbose)
    
    if RICH_AVAILABLE:
        console.print("🔄 [bold blue]Universal File Operator[/bold blue]", style="bold")
    else:
        print("🔄 Universal File Operator")


@cli.command()
@click.argument('data')
@click.option('--from', 'from_format', 
              type=click.Choice([
                  'binary', 'base64', 'hex', 'text', 'url_encoded', 'html_encoded',
                  'json', 'dict', 'decimal', 'md5', 'sha256'
              ]), 
              required=True, help='Source format')
@click.option('--to', 'to_format', 
              type=click.Choice([
                  'binary', 'base64', 'hex', 'text', 'url_encoded', 'html_encoded',
                  'json', 'dict', 'decimal', 'md5', 'sha256'
              ]), 
              required=True, help='Target format')
@click.option('--output', '-o', help='Output file (default: print to stdout)')
@click.option('--indent', type=int, help='Indentation for formatted output (JSON)')
@click.option('--uppercase', is_flag=True, help='Use uppercase for hex output')
@click.option('--include-prefix', is_flag=True, help='Include prefix (0x for hex, 0b for binary)')
@click.option('--encoding', default='utf-8', help='Text encoding (default: utf-8)')
@click.pass_context
def convert_data(ctx, data, from_format, to_format, output, indent, uppercase, include_prefix, encoding):
    """
    Convert DATA from one format to another.
    
    Examples:
    \b
        convert-data "Hello World" --from text --to base64
        convert-data "SGVsbG8gV29ybGQ=" --from base64 --to text
        convert-data "42" --from decimal --to binary_num
        convert-data '{"name": "John"}' --from json --to yaml
    """
    try:
        # Prepare conversion options
        options = {}
        if indent is not None:
            options['indent'] = indent
        if encoding != 'utf-8':
            options['encoding'] = encoding
        if uppercase:
            options['uppercase'] = True
        if include_prefix:
            options['include_prefix'] = True
        
        # Perform conversion
        result = convert(data, from_format, to_format, **options)
        
        # Output result
        if output:
            Path(output).write_text(str(result), encoding=encoding)
            if RICH_AVAILABLE:
                console.print(f"✅ [green]Conversion saved to {output}[/green]")
            else:
                print(f"✅ Conversion saved to {output}")
        else:
            if RICH_AVAILABLE:
                console.print("📤 [bold]Result:[/bold]")
                console.print(result)
            else:
                print("📤 Result:")
                print(result)
                
    except UnsupportedFormatError as e:
        if RICH_AVAILABLE:
            console.print(f"❌ [red]Unsupported conversion: {e}[/red]")
            console.print("💡 Use 'list-formats' to see available conversions")
        else:
            print(f"❌ Unsupported conversion: {e}")
            print("💡 Use 'list-formats' to see available conversions")
        sys.exit(1)
        
    except ValidationError as e:
        if RICH_AVAILABLE:
            console.print(f"❌ [red]Validation error: {e}[/red]")
        else:
            print(f"❌ Validation error: {e}")
        sys.exit(1)
        
    except ConversionError as e:
        if RICH_AVAILABLE:
            console.print(f"❌ [red]Conversion error: {e}[/red]")
        else:
            print(f"❌ Conversion error: {e}")
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--from', 'from_format', 
              type=click.Choice([
                  'binary', 'base64', 'hex', 'text', 'url_encoded', 'html_encoded',
                  'json', 'dict', 'decimal', 'md5', 'sha256'
              ]), 
              required=True, help='Source format')
@click.option('--to', 'to_format', 
              type=click.Choice([
                  'binary', 'base64', 'hex', 'text', 'url_encoded', 'html_encoded',
                  'json', 'dict', 'decimal', 'md5', 'sha256'
              ]), 
              required=True, help='Target format')
@click.option('--output', '-o', help='Output file (default: input_file.converted)')
@click.option('--encoding', default='utf-8', help='Text encoding')
@click.pass_context
def convert_file(ctx, input_file, from_format, to_format, output, encoding):
    """
    Convert a file from one format to another.
    
    Examples:
    \b
        convert-file data.json --from json --to yaml -o data.yaml
        convert-file image.base64 --from base64 --to binary -o image.bin
    """
    try:
        # Read input file
        input_path = Path(input_file)
        
        if from_format in ['binary', 'base64'] and to_format in ['binary']:
            # Handle binary files
            data = input_path.read_bytes()
        else:
            data = input_path.read_text(encoding=encoding)
        
        if RICH_AVAILABLE:
            console.print(f"📖 Reading {input_path.name}...")
        
        # Perform conversion
        result = convert(data, from_format, to_format)
        
        # Determine output file
        if not output:
            output = f"{input_path.stem}.{to_format}"
        
        output_path = Path(output)
        
        # Write result
        if isinstance(result, bytes):
            output_path.write_bytes(result)
        else:
            output_path.write_text(str(result), encoding=encoding)
        
        if RICH_AVAILABLE:
            console.print(f"✅ [green]Converted {input_path.name} → {output_path.name}[/green]")
        else:
            print(f"✅ Converted {input_path.name} → {output_path.name}")
            
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"❌ [red]Error: {e}[/red]")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
@click.option('--format', 'format_filter', help='Filter by format name')
@click.option('--output-format', type=click.Choice(['table', 'json']), default='table', help='Output format')
def list_formats(format_filter, output_format):
    """
    List all supported conversion formats and pairs.
    
    Examples:
    \b
        list-formats                    # Show all conversions
        list-formats --format base64    # Show conversions involving base64
        list-formats --output-format json  # Output as JSON
    """
    try:
        conversions = list_conversions()
        
        # Apply filter if specified
        if format_filter:
            conversions = [
                conv for conv in conversions 
                if format_filter.lower() in conv['from'].lower() or 
                   format_filter.lower() in conv['to'].lower()
            ]
        
        if output_format == 'json':
            import json
            print(json.dumps(conversions, indent=2))
            return
        
        # Table format
        if RICH_AVAILABLE:
            table = Table(title="🔄 Supported Conversions")
            table.add_column("From", style="cyan")
            table.add_column("To", style="magenta")
            table.add_column("Description", style="white")
            table.add_column("Reversible", style="green")
            
            for conv in conversions:
                reversible = "✅" if conv.get('reversible', False) else "❌"
                table.add_row(
                    conv['from'],
                    conv['to'],
                    conv['description'],
                    reversible
                )
            
            console.print(table)
        else:
            # Simple text table
            print("From          To            Description                      Reversible")
            print("-" * 80)
            for conv in conversions:
                reversible = "Yes" if conv.get('reversible', False) else "No"
                print(f"{conv['from']:<12} {conv['to']:<12} {conv['description']:<30} {reversible}")
        
        if RICH_AVAILABLE:
            console.print(f"\n📊 Total: {len(conversions)} conversions available")
        else:
            print(f"\nTotal: {len(conversions)} conversions available")
            
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"❌ [red]Error: {e}[/red]")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)


@cli.command()
def interactive():
    """
    Start interactive conversion mode.
    
    This provides a user-friendly interface for multiple conversions
    with guided format selection.
    """
    formats = [
        'binary', 'base64', 'hex', 'text', 'url_encoded', 'html_encoded',
        'json', 'dict', 'decimal', 'md5', 'sha256'
    ]
    
    if RICH_AVAILABLE:
        console.print("🎮 [bold blue]Interactive Conversion Mode[/bold blue]")
        console.print("Type 'quit' or 'exit' to stop\n")
        
        # Show available formats
        console.print("📋 [bold]Available Formats:[/bold]")
        for i, fmt in enumerate(formats, 1):
            console.print(f"  {i:2d}. {fmt}")
        console.print()
    else:
        print("🎮 Interactive Conversion Mode")
        print("Type 'quit' or 'exit' to stop\n")
        
        print("📋 Available Formats:")
        for i, fmt in enumerate(formats, 1):
            print(f"  {i:2d}. {fmt}")
        print()
    
    while True:
        try:
            # Get input data
            data = input("📝 Enter data to convert: ").strip()
            if data.lower() in ['quit', 'exit']:
                break
            
            # Get format information with number selection
            print("📥 Select source format:")
            try:
                from_choice = int(input("   Enter number (1-{}): ".format(len(formats))))
                if 1 <= from_choice <= len(formats):
                    from_format = formats[from_choice - 1]
                else:
                    print("❌ Invalid choice. Please enter a number between 1 and", len(formats))
                    continue
            except ValueError:
                print("❌ Please enter a valid number")
                continue
            
            print("📤 Select target format:")
            try:
                to_choice = int(input("   Enter number (1-{}): ".format(len(formats))))
                if 1 <= to_choice <= len(formats):
                    to_format = formats[to_choice - 1]
                else:
                    print("❌ Invalid choice. Please enter a number between 1 and", len(formats))
                    continue
            except ValueError:
                print("❌ Please enter a valid number")
                continue
            
            # Show selected conversion
            print(f"🔄 Converting: {from_format} → {to_format}")
            
            # Perform conversion
            result = convert(data, from_format, to_format)
            
            if RICH_AVAILABLE:
                console.print("✅ [green]Result:[/green]")
                console.print(result)
            else:
                print("✅ Result:")
                print(result)
            
            print()  # Empty line for spacing
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            if RICH_AVAILABLE:
                console.print(f"❌ [red]Error: {e}[/red]")
            else:
                print(f"❌ Error: {e}")
            print()
    
    if RICH_AVAILABLE:
        console.print("👋 [blue]Goodbye![/blue]")
    else:
        print("👋 Goodbye!")


@cli.command()
@click.option('--samples', type=int, default=5, help='Number of sample conversions to show')
def demo(samples):
    """
    Run a demonstration of various conversions.
    
    This command shows examples of different conversion types to help
    users understand the capabilities of the tool.
    """
    demo_data = [
        ("Hello World", "text", "base64"),
        ("SGVsbG8gV29ybGQ=", "base64", "hex"),
        ("42", "decimal", "binary"),
        ("101010", "binary", "decimal"),
        ('{"name": "John", "age": 30}', "json", "dict"),
        ("Hello World", "text", "md5"),
        ("Hello <World>", "text", "html_encoded"),
        ("Hello%20World", "url_encoded", "text"),
    ]
    
    if RICH_AVAILABLE:
        console.print("🎯 [bold blue]Conversion Demonstration[/bold blue]\n")
    else:
        print("🎯 Conversion Demonstration\n")
    
    for i, (data, from_fmt, to_fmt) in enumerate(demo_data[:samples]):
        try:
            if RICH_AVAILABLE:
                console.print(f"[cyan]Example {i+1}:[/cyan] {from_fmt} → {to_fmt}")
                console.print(f"  Input:  {data}")
            else:
                print(f"Example {i+1}: {from_fmt} → {to_fmt}")
                print(f"  Input:  {data}")
            
            result = convert(data, from_fmt, to_fmt)
            
            if RICH_AVAILABLE:
                console.print(f"  Output: [green]{result}[/green]\n")
            else:
                print(f"  Output: {result}\n")
                
        except Exception as e:
            if RICH_AVAILABLE:
                console.print(f"  [red]Error: {e}[/red]\n")
            else:
                print(f"  Error: {e}\n")


def main():
    """Main entry point for the CLI."""
    try:
        # Import and register all simple converters
        from ..converters import simple_converters
        cli()
    except ImportError:
        # Handle development mode
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from src.converters import simple_converters
        cli()


if __name__ == '__main__':
    main()