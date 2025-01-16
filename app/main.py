from db import Session, init_db
from drive import list_files, change_visibility, get_authenticated_user_email
from emailer import send_email
from utils import parse_file
from datetime import datetime
from db import DriveFile, PublicFileHistory

init_db()
session = Session()

authenticated_user_email = get_authenticated_user_email()

def main():
    files = list_files()
    print('Iniciando inventario de archivos...')
    for file in files:
        parsed_file = parse_file(file)
        if parsed_file['owner'] != authenticated_user_email:
            continue  

        existing_file = session.query(DriveFile).filter_by(id=parsed_file['id']).first()

        if existing_file:
            existing_file.last_modified = parsed_file['last_modified']
            session.commit()
        else:
            new_file = DriveFile(**parsed_file)
            session.add(new_file)
            session.commit()

        if parsed_file['visibility']:
            change_visibility(parsed_file['id'])
            send_email(parsed_file['owner'], parsed_file['name'])
  
            existing_history = session.query(PublicFileHistory).filter_by(id=parsed_file['id']).first()
            if not existing_history:
                history = PublicFileHistory(
                    id=parsed_file['id'],
                    name=parsed_file['name'],
                    owner=parsed_file['owner'],
                    changed_at=datetime.now()
                )
                session.add(history)
                session.commit()

if __name__ == '__main__':
    main()
