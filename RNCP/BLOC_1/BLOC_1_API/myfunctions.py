#########################
###     LIBRARIES     ###
#########################

from datetime import datetime



#########################
###     FUNCTIONS     ###
#########################

# FUNCTION to print Statistics
def print_statistics(start_time: datetime, end_time: datetime, start_page: int, end_page: int):
    # Calculate the total_time and total_pages
    total_time = (end_time - start_time)
    total_pages = (end_page - start_page)

    # Calculate the total time in days, hours, minutes, and seconds
    total_seconds = total_time.total_seconds()
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    statistics = (total_pages / (total_seconds / 60))

    # Print the time
    print("\n****************************************")
    print("Webscraping started @ :", start_time)
    print("Webscraping finished @ :", end_time)
    print(total_pages, "webscraped page(s).")
    print("\nThe execution took :", int(days), "days,", int(hours), "hours,", int(minutes), "minutes and", int(seconds), "seconds.")
    print(f"Statistics : {statistics:.2f} pages/min.")
    print("****************************************\n")