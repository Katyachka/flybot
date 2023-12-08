
class ChatCache:

    def __init__(self):
        self.personal_data_cache = {}
        self.messages_to_edit_cache = {}
        self.messages_to_delete_cache = {}
        self.flights_cache = {}
        self.seats_cache = {}
        self.choose_seat_pagination_state = {}

    def put_pers_data(self, chat_id, value):
        self.personal_data_cache[chat_id] = value

    def get_pers_data(self, chat_id):
        return self.personal_data_cache[chat_id]

    def rem_pers_data(self, chat_id):
        del self.personal_data_cache[chat_id]

    def put_msg_to_edit(self, chat_id, value):
        self.messages_to_edit_cache[chat_id] = value

    def get_msg_to_edit(self, chat_id):
        return self.messages_to_edit_cache[chat_id]

    def put_msg_to_del(self, chat_id, value):
        self.messages_to_delete_cache[chat_id] = value

    def add_msg_to_del(self, chat_id, msg_id):
        if self.messages_to_delete_cache[chat_id] is None:
            self.messages_to_delete_cache[chat_id] = [msg_id]
        else:
            self.messages_to_delete_cache[chat_id].append(msg_id)

    def get_msgs_to_delete(self, chat_id):
        return self.messages_to_delete_cache[chat_id]

    def get_flight(self, chat_id):
        return self.flights_cache[chat_id]

    def put_flight(self, chat_id, flight):
        self.flights_cache[chat_id] = flight

    def get_seat(self, chat_id):
        return self.seats_cache[chat_id]

    def put_seat(self, chat_id, seat):
        self.seats_cache[chat_id] = seat

    def put_chs_seat_pag_state(self, chat_id, pag_state):
        self.choose_seat_pagination_state[chat_id] = pag_state

    def get_chs_seat_pag_state(self, chat_id):
        return self.choose_seat_pagination_state[chat_id]