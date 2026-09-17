from datetime import datetime

start_date = input("Enter Start Date (DD/MM/YYYY): ")
end_date = input("Enter End Date (DD/MM/YYYY: )")

start = datetime.strptime(start_date, "%d/%m/%Y")
end = datetime.strptime(end_date, "%d/%m/%Y")

duration  = end - start

print(duration.days)