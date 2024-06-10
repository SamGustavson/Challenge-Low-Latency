"""Functional requirements:

 1.1. Read messages from text_in.dat files with extension '.
 in' in the given directory.

 1.2. Update the timestamp (tag 52) in all messages to the current time.

 1.3. Swap the positions of tags 150 and 205.

 1.4. Save the processed messages to files with same name but with the .out extension.

2. Write python tests for your class."""

import datetime
import pathlib


class MessageHandler:

    def read_messages(self, path):

        """ 1.1. Read messages from text_in.dat files with extension '.
                                                        in' in the given directory."""
        message_data = {}
        with open(path, mode='r', newline='\n', encoding='utf-8') as in_text:
            message_data = in_text.read()

        return message_data

    def update_timestamp(self, msg):
        """ 1.2.Updates the timestamp (tag 52) in the message to the current time."""
        current_time = datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')
        sorted_data = []
        for part in msg.split('|'):
            if part.startswith('52='):
                sorted_data.append(f'52={current_time}')
            else:
                sorted_data.append(part)
        return '|'.join(sorted_data)

    def swap_tags(self, message):

        """1.3. Swap the positions of tags 150 and 205.


        8=FIX.4.2|9=448|35=8|49=FASTLB|56=FIXDBS|34=26|57=DASHFIX|
        52=20240510-06:45:00.361|37=660000606240|11=KATE20240424-056|
        76=792|17=660003962267|20=0|150=D|39=0|378=1|1=katetest6|
        55=AAPL|167=OPT|200=202501|205=17|201=1|202=280|54=1|38=12|
        40=2|44=75|59=1|32=0|31=0|151=12|14=0|6=0|60=20240510-06:45:00.275
        |77=O|442=1|204=0|10606=0|6606=KATETEST|10002=660000387118|
        10526=KATE20240424-056|5049=DASHLB|5056=KATETEST|5050=20240510-06:45:00.276819|
        10006=SEG6_OSR6|10057=66|10=144|


        This method does not work for all rows, since the variables that we
        exchange are not present in the appropriate ratio, i.e. tags '205=" less than "150=" """

        parts = message.split('|')
        tag_dict = {part.split('=')[0]: part for part in parts}

        if '150' in tag_dict and '205' in tag_dict:
            tag_150 = tag_dict['150']
            tag_205 = tag_dict['205']
            tag_dict['150'], tag_dict['205'] = tag_205, tag_150

        return '|'.join(tag_dict.values())

    def process_messages(self, message):

        """ 1.3. Swap the positions of tags 150 and 205."""
        updated_message = self.update_timestamp(message)
        updated_message = self.swap_tags(updated_message)
        processed_messages = updated_message
        return processed_messages

    def save_messages(self, path, message):
        """ 1.4. Save the processed messages to files with same name but with the .out extension."""
        # for message in processed_messages:
        with open(path, 'w') as file:
            file.write(message)


    def save_all_messages(self, path_in,path_out ):
        """Processes all .in messages in the directory and saves the results."""

        messages = self.read_messages(path_in)
        row_counter = 0
        # processed_messages = {}
        lines = messages.split('\n')
        with open(path_out, mode='w', newline='\n') as out_file:
            for line in lines:
                row_counter = len(lines)

                updated_message = self.update_timestamp(line)
                updated_message = self.swap_tags(updated_message)
                processed_messages = updated_message
                # print(processed_messages)
                out_file.writelines(processed_messages)
                out_file.writelines("\n")
            out_file.close()

        return row_counter



if __name__ == "__main__":
    path = pathlib.Path(__file__).parent.resolve()
    path_to_file_in = f"{path}/data/text_in.dat"
    path_to_file_out = f"{path}/data/text_out.dat"
    processor = MessageHandler()
    print(processor.read_messages(path_to_file_in))
