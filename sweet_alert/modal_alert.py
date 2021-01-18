import json


class modal_message:
    def __init__(self, status, form, text):
        self.form = form
        self.text = text
        self.status = status

    def display_message(self):

        message = {}

        if self.status == 'error' and self.form == None:
            message['tags'] = 'error'
            message['message'] = self.text

        elif self.status == 'success':
            message['tags'] = 'success'
            message['message'] = self.text
        else:
            if self.form.errors:
                for field in self.form:
                    for error in field.errors:
                        message['tags'] = 'error'
                        message['message'] = error

        return json.dumps(message)
