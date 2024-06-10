import os
import pathlib
import pytest
import datetime
from message_handler import MessageHandler

path = pathlib.Path(__file__).parent.parent.resolve()
path_to_file_in = f"{path}/data/text_in.dat"
path_to_file_out = f"{path}/data/text_out.dat"


def test_current():
    print(os.getenv('PYTEST_CURRENT_TEST'))
    filepath = path_to_file_in
    # print('\n', filepath)
    assert "text_in.dat" in filepath



def test_read_messages():
    """reading messages from .in files."""
    processor = MessageHandler()
    messages = processor.read_messages(path_to_file_in)
    assert "8=FIX.4.2" in messages


def test_update_timestamp():
    """updating the timestamp in the message."""
    processor = MessageHandler()
    original_message = processor.read_messages(path_to_file_in)
    updated_message = processor.update_timestamp(original_message)
    current_time = datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')
    # print("\n", "INSIDE TEST: current time is: ", current_time)
    assert f'52={current_time}' in updated_message


def test_swap_tags():
    """swapping the positions of tags 150 and 205."""
    processor = MessageHandler()
    original_message = processor.read_messages(path_to_file_in)
    swapped_message = processor.swap_tags(original_message)
    # print(swapped_message)
    assert "|205=*|39=0|" and "|150=D|201=1|" in swapped_message


def test_save_message():
    """saving a single message."""
    processor = MessageHandler()
    read_message = processor.read_messages(path_to_file_in)
    processed_message = processor.process_messages(read_message)
    # print(processed_message, "INSIDE TEST SAVE")
    processor.save_messages(path_to_file_out, processed_message)
    current_time = datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')
    assert f'52={current_time}' in processed_message
    assert "|205=*|39=0|" and "|150=D|201=1|" in processed_message


def test_save_all_messages():
    """Tests saving all messages in the directory."""
    processor = MessageHandler()
    lines = processor.save_all_messages(path_to_file_in, path_to_file_out)
    assert lines == 18
    read_message = processor.read_messages(path_to_file_out)
    assert '52=' in read_message
    assert '150=' in read_message
    assert '205=' in read_message
