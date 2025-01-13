from datetime import datetime

def parse_file(file):
    return {
        'id': file['id'],
        'name': file['name'],
        'extension': file['mimeType'].split('.')[-1] if '.' in file['mimeType'] else 'unknown',
        'owner': file['owners'][0]['emailAddress'],
        'visibility': file.get('shared', False),
        'last_modified': datetime.strptime(file['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ")
    }