import datetime
import aiohttp
import os
import time
import math
from download_from_url import get_size, time_formatter

async def progress(current, total, event, start):
    """Generic progress_callback for both
    upload.py and download.py"""
    now = time.time()
    diff = now - start
    if round(diff % 1.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        prog_bar = "[{0}{1}]".format(
            ''.join(["◾" for i in range(math.floor(percentage / 10))]),
            ''.join(["◽" for i in range(10 - math.floor(percentage / 10))]))
        
        progress_str = f"""**Downloading: {round(percentage,2)}**\n{prog_bar}\n{get_size(current)} of {get_size(total)}\
        \nSpeed: {get_size(speed)}/sec\nETA: {time_formatter(estimated_total_time)}"""
        await event.edit(progress_str)

def get_date_in_two_weeks():
    """
    get maximum date of storage for file
    :return: date in two weeks
    """
    today = datetime.datetime.today()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()

async def send_to_transfersh_async(file, message):
    
    size = os.path.getsize(file)
    size_of_file = get_size(size)
    final_date = get_date_in_two_weeks()
    file_name = os.path.basename(file)

    print("\nSending file: {} (size of the file: {})".format(file_name, size_of_file))
    url = 'https://transfer.sh/'
    
    with open(file, 'rb') as f:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={ file_name : f}) as response:
                download_link =  await response.text()
                        
    print("Link to download file(will be saved till {}):\n{}".format(final_date, download_link))
    return download_link, final_date, size_of_file