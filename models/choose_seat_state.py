from telebot import types

from util.utils import CHOOSE_SEAT, OCCUPIED, SEAT_PAG, NEXT, PREV


class ChooseSeatState:

    def __init__ (self, current=None, pages=None, page_count=None, flight=None, chat_id=None):
        self.current = current
        self.flight = flight
        self.pages = flight.plane.passengers / page_count
        self.page_count = page_count
        self.chat_id=chat_id
        self.changed = True

    def get_page_btns(self, seats):
        reply_markup = types.InlineKeyboardMarkup(row_width=int(self.flight.plane.seat_in_row / 2))

        start_index = (self.current - 1) * self.page_count
        end_index = start_index + self.page_count
        buttons = []

        for seat in seats[start_index:end_index]:
            callback_data = f"{CHOOSE_SEAT}:{seat.number}"
            if seat.number.endswith("(вже зайняте)"):
                callback_data = f"{CHOOSE_SEAT}:{OCCUPIED}"
            buttons.append(types.InlineKeyboardButton(f"{seat.number}", callback_data=callback_data))

        index = 0
        column_count = int(self.flight.plane.seat_in_row / 2)
        while index < len(buttons):
            line = []
            for i in range(column_count):
                line.append(buttons[index + i])
            reply_markup.row(*line)
            index += column_count

        reply_markup.add(types.InlineKeyboardButton('<<', callback_data=f"{SEAT_PAG}:{PREV}"),
                         types.InlineKeyboardButton(f"{self.current}", callback_data="nope"),
                         types.InlineKeyboardButton('>>', callback_data=f"{SEAT_PAG}:{NEXT}"))
        return reply_markup

    def apply_action(self, action):
        if action == NEXT:
            if self.current < self.pages:
                self.current += 1
                self.changed = True
            else:
                self.changed = False
        else:
            if self.current > 1:
                self.current -= 1
                self.changed = True
            else:
                self.changed = False

    def is_changed(self):
        return self.changed
