import json
from typing import Dict, List, Any, Tuple


def convert_data_to_markdown(data: List[Dict[str, Dict[str, Any]]]) -> str:
    """
    Converts Looker API JSON data to Markdown table.

    Args:
        data (List[Dict[str, Dict[str, Any]]]): Looker API JSON data.

    Returns:
        str: Markdown table body.
    """
    markdown_body = ""

    # Get the headers from the first entry in the data list
    headers = list(data[0].keys())

    # Get the rows by extracting the 'value' field from each entry in the data list
    rows = [[entry[key]['value'] for key in headers] for entry in data]

    # Construct the rows
    for row in rows:
        markdown_body += '| ' + ' | '.join(map(str, row)) + ' |\n'

    return markdown_body


def convert_fields_to_markdown(fields: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Converts Looker API JSON fields to Markdown table.

    Args:
        fields (List[Dict[str, Any]]): Looker API JSON fields.

    Returns:
        Tuple[str, str]: A tuple containing the Markdown table header and footer.
                         The header is a string representing the header row of the table.
                         The footer is a string representing the footer with field descriptions.
    """

    markdown_header = "| "
    markdown_footer = "\n"
    header_labels = []

    # Extract header labels from dimensions
    for field in fields:
        label = field.get('label', '')
        # Remove anything after opening parentheses
        clean_label = label.split("(")[0].strip()
        header_labels.append(clean_label)

        description = field.get('description', '')
        expression = field.get('expression', '')
        if description:
            markdown_footer += f"* {label} = {description} {expression}\n"

    # Append header labels to Markdown
    markdown_header += " | ".join(header_labels) + " |\n"

    # Add separator row
    markdown_header += "| --- " * len(header_labels) + "|\n"

    return (markdown_header, markdown_footer)

## MAIN ##


def convert_looker_data_to_markdown(data: Dict[str, Dict[str, Any]]) -> str:
    """
    Converts Looker API JSON data to Markdown table.
    Limits the data to 500 rows and 10000 characters.

    Args:
        data (Dict[str, Dict[str, Any]]): Looker API JSON data.

    Returns:
        str: Markdown table content.
    """
    if len(data.get('fields', {}).get('pivots', [])) > 0:
        raise Exception(
            'Pivots not yet supported. Please use the pivoted dimension as a column.')

    fields = (data.get('fields', {}).get('dimensions', []) +
              data.get('fields', {}).get('measures', []) +
              data.get('fields', {}).get('table_calculations', [])
              )
    data_list = data.get('data', [])[:500]

    header, footer = convert_fields_to_markdown(fields)
    markdown_body = convert_data_to_markdown(data_list)

    return header + markdown_body[:10000] + footer
