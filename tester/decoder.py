import cantools

class DBCDecoder:
    def __init__(self, dbc_path):
        self.db = cantools.database.load_file(dbc_path)
        
    def decode(self, msg):
        try:
            return self.db.decode_message(msg.arbitration_id, msg.data)
        except KeyError:
            return None
