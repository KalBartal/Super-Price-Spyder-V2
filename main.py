# Super Price Spyder V2 with GUI

# This code is a python script to create a GUI (Graphical User Interface) application. It creates a window with
# labels and entry fields, where a user can enter the URL of an Amazon product and request a price alert. Once the
# price alert button is clicked, it pulls the data from the URL entered, scrapes it and extracts the item title and
# price and then utilizes the SMTP protocol to send an email with the item information to the user when the price
# changes to a certain value.


import os
import smtplib
from tkinter import *
import requests
from bs4 import BeautifulSoup

# set up window
main_window = Tk()
main_window.configure(background="#FAD6A5", padx=20, pady=50)
main_window.title("Super Price Spyder V2")  # Window title

# Create Labels
l1 = Label(main_window, text="Welcome to Super Price Spyder!", font=("Arial Bold", 36), fg="#567189")
l1.configure(background="#CFB997")
l1.grid(columnspan=2, padx=10, pady=10)
l2 = Label(main_window, text="Please enter the Amazon product URL for the item you wish to check the price for:",
           fg="#567189", font=("Arial Bold", 14))
l2.configure(background="#CFB997")
l2.grid(row=1, columnspan=2, padx=10, pady=10)

# Create Entry fields
url_field = Entry(main_window)
url_field.configure(background="#FAD6A5", foreground="#567189")
url_field.grid(row=2, column=0, pady=10, ipadx=100)


def price_alert():
    url = url_field.get()
    my_email = os.environ.get("MY_EMAIL")
    password = os.environ.get("MY_PASSWORD")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                      "Version/16.2 Safari/605.1.15",
        "Accept-Language": "en-GB,en;q=0.9",
    }

    page = requests.get(url, headers=headers)

    # print(page.text)

    soup = BeautifulSoup(page.text, 'lxml')
    # print(soup.prettify())
    price = soup.find(class_="a-offscreen").getText()
    price_float = float(price.replace("£", ""))
    title = soup.find(id="productTitle").getText().replace("        ", "")

    # print(price)

    if price_float < 28:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject:Amazon Price Alert!\n\n{title}\n\n now ${price_float}\n\n{url}"
            )

    print(f"{title}\n{price}\n{url}")


# Create buttons
p_alert = Button(main_window, text="Price Alert", font=("Arial Bold", 16), command=price_alert, fg="#567189")
p_alert.configure(background="green")
p_alert.grid(row=2, column=1, columnspan=3, pady=10)

exit_button = Button(main_window, text="Exit", font=("Arial Bold", 16), command=main_window.quit)
exit_button.configure(fg="#567189")
exit_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

main_window.mainloop()  # Call main loop to show window on screen
