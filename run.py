from app import runServ, db

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    # db.create_all()
    runServ()