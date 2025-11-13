"""Parsing helpers."""

def parse_graphql_data(response_data: dict, key_path: str) -> dict:
    """Extract nested GraphQL data, e.g., 'data.user.edge_owner_to_timeline_media'."""
    keys = key_path.split(".")
    data = response_data
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return {}
    return data