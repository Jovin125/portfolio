import tkinter as tk
from tkinter import messagebox

DISCOUNTS = {"senior":{'percent':0.1, 'status':False},
             "Members":{'percent':0.08, 'status':False},
             "NS_Men":{'percent':0.05, 'status':False}}
GST = 0.09
Appendix = [[f'{"Item":<30}', "Code", "Price($)", f'{"Qty":^8}', f'{"total($)":^8}'],  # list[0]
            ["1. Drinks(CD10)",  # list[1][0 to 4]
             [f'{"Neo’s Green Tea":<30}', "N32", {"cost": 3.00, "qty": 0}],# to call for dictionary, Appendix[1][1][2]['qty']
             [f'{"Melo Chocolate Malt Drink":<30}', "M13", {"cost": 2.85, "qty": 0}],
             [f'{"Very-Fair Full Cream Milk":<30}', "V76", {"cost": 3.50, "qty": 0}],
             [f'{"Nirigold UHT Milk":<30}', "N14", {"cost": 4.15, "qty": 0}],
             ],  # end of list[1]
            ["2. Beer(CB20)",  # list[2][0 to 4]
             [f'{"Lion (24 x 320 ml)":<30}', "L11", {"cost": 52.0, "qty": 0}],
             [f'{"Panda (24 x 320 ml)":<30}', "P21", {"cost": 78.0, "qty": 0}],
             [f'{"Axe (24 x 320 ml)":<30}', "A54", {"cost": 58.0, "qty": 0}],
             [f'{"Henekan (24 x 320 ml)":<30}', "H91", {"cost": 68.0, "qty": 0}]
             ],  # end of list[2]
            ["3. Frozen(CF30)",  # list[3][0 to 4]
             [f'{"Edker Ristorante Pizza 355g":<30}', "E11", {"cost": 6.95, "qty": 0}],
             [f'{"Fazzler Frozen Soup 500g":<30}', "F43", {"cost": 5.15, "qty": 0}],
             [f'{"CP Frozen Ready Meal 250g":<30}', "CP31", {"cost": 4.12, "qty": 0}],
             [f'{"Duitoni Cheese 270g":<30}', "D72", {"cost": 5.60, "qty": 0}]
             ],  # end of list[3]
            ["4. Household(CH40)",  # list[4][0 to 4]
             [f'{"FP Facial Tissues":<30}', "FP76", {"cost": 9.50, "qty": 0}],
             [f'{"FP Premium Kitchen Towel":<30}', "FP32", {"cost": 5.85, "qty": 0}],
             [f'{"Klinex Toilet Tissue Rolls":<30}', "K22", {"cost": 7.50, "qty": 0}],
             [f'{"Danny Softener":<30}', "D14", {"cost": 9.85, "qty": 0}]
             ],  # end of list[4]
            ["5. Snacks(CS50)",  # list[5][0 to 4]
             [f'{"Singshort Seaweed":<30}', "SS93", {"cost": 3.10, "qty": 0}],
             [f'{"Mei Crab Cracker":<30}', "MC14", {"cost": 2.05, "qty": 0}],
             [f'{"Reo Pokemon Cookie":<30}', "R35", {"cost": 4.80, "qty": 0}],
             [f'{"Huat Seng Crackers":<30}', "HS11", {"cost": 3.85, "qty": 0}]
             ]  # end of list[5]
            ]  # end of list
cart_dict = {}
root = tk.Tk()
root.configure(bg='cornflower blue')
root.title('Shopping cart')
root.geometry('1200x600')

def total_cost_current_cat(catergory_chosen):
    currrent_cat_total = 0
    for item in range(1, 5):
        currrent_cat_total += Appendix[catergory_chosen][item][2]['total']
    return float(f"{currrent_cat_total:.2f}")

def total_cost_all_cat():
    sum_total_across_cat = 0
    for cat in range(1, 6):
        for item in range(1, 5):
            price = Appendix[cat][item][2]['cost']
            selected_qty = Appendix[cat][item][2]['qty']
            Appendix[cat][item][2]['total'] = float(f"{price * selected_qty:.2f}")# adds to dictionary part of appendix
                                                                                # with key 'total' and value calculated
            sum_total_across_cat += Appendix[cat][item][2]['total'] #adds the value of all item total calulated
    return float(f"{sum_total_across_cat:.2f}")

def percent_calc(): #calculates percentage
    percent_off = 0
    for discounts in DISCOUNTS:
        percent_off += DISCOUNTS[discounts]['percent'] * DISCOUNTS[discounts]['status']
    shown_percent = percent_off*100 #percentage to be shown to user
    print(DISCOUNTS)
    return shown_percent

def reset():
    remove_current_page()
    for cat in range(1,6):
        for items in range(1,5):
            Appendix[cat][items][2]['qty'] = 0 #sets all item qty to 0
    for discounts in DISCOUNTS:
        DISCOUNTS[discounts]['status'] = False #sets all discounts as false
    main()

def remove_current_page():
    for widgets in root.winfo_children(): #gets the name of items which have their parent set as root
        widgets.destroy() #destroys items

def bill_statement(category_chosen):
    def paymentcheck(): #checks if user inputted amount is valid and covers the final price
        amt = howmuch.get()
        amt = str(amt)
        if amt.isdigit(): #checks if input is a digit, decimals not allowed
            spare_change = int(amt) - finalprice
            if spare_change > 0: #checks if input covers final price
                recipt_item = []
                for items in cart_dict:
                    recipt_item.append([f'name:{cart_dict[items]['Name']}',
                                        f'qty:{cart_dict[items]['qty']}',
                                        f'total:{cart_dict[items]['total']}'])

                accepted = tk.messagebox.askquestion('Receipt',
                                                     f'{recipt_item}\n'
                                                     f'Your payment was ${amt}\n'
                                                     f'Your total was ${finalprice:.2f}\n'
                                                     f'Your change is ${spare_change:.2f}\n'
                                                             f'This is your Receipt.\n'
                                                     f'Would you like to continue shopping?')
                if accepted == 'yes': #user wants to continue shopping
                    reset() #sends user back to start with everything reset
                if accepted == 'no': #user does not want to continue
                    root.quit() #quits the root page
            else: #user did not input enough money to cover final price
                denied = tk.messagebox.showwarning('Payment not enough',
                                                     f'Your payment of ${amt} '
                                                     f'is not enough to pay for ${finalprice:.2f}')
        else: #user did not input a digit(whole number)
            invalid = tk.messagebox.showerror("Show error", "Invalid, Please input a whole number")
    remove_current_page()
    money = tk.Frame(root, bg='cornflower blue')
    money.pack(expand=True, fill='both')
    for x in range(8): #add grid placements for widgets
        money.columnconfigure(index=x, weight=1)
    back_to_checkout = tk.Button(money, text='Back',font=('Arial', 18), command= lambda: show_cart(category_chosen))
    back_to_checkout.grid(column=0, row=0, padx=20, pady=10, sticky='NW')
    label = tk.Label(money, text='Checkout(Bill statement)', font=('Arial', 18))
    label.grid(column=1, row=0, padx=20, pady=10, sticky='NW')

    for itemdetails in range(len(Appendix[0])): #item frame(Item, code, price, qty, total)
        details = tk.Label(money, text = Appendix[0][itemdetails], font=('Arial', 12))
        details.grid(column=itemdetails+1, row=1, sticky='NW')

    yrow = 2
    for items in cart_dict:
        xcolumn = 1
        for details in cart_dict[items]: #item information(name, code, price, qty, total is displayed as labels)
            iteminformation = tk.Label(money, text=cart_dict[items][details], font=('Arial', 12))
            iteminformation.grid(column=xcolumn, row=yrow, sticky='NW')
            xcolumn += 1
        yrow += 1

    totalprice = total_cost_all_cat()

    total = tk.Label(money, text=f'The total(before GST and discount):${totalprice}', font=('Arial', 12))
    total.grid(row=yrow+3, columnspan=7, sticky='N', pady=5)

    discounted = totalprice * (percent_calc()/100)
    discount = tk.Label(money, text=f'Discount of {percent_calc()}%:${discounted:.2f}'
                        , font=('Arial', 12))
    discount.grid(row=yrow + 4, columnspan=7, sticky='N', pady=5)

    gst = (totalprice-discounted) *GST
    gst_amt = tk.Label(money, text=f'GST(9%):${gst:.2f}', font=('Arial', 12))
    gst_amt.grid(row=yrow+5, columnspan=7, sticky='N', pady=5)

    finalprice = totalprice + gst - discounted
    final = tk.Label(money, text=f'The final total(inclusive of GST and discounts):${finalprice:.2f}'
                     , font=('Arial', 12))
    final.grid(row=yrow + 6, columnspan=7, sticky='N', pady=5)

    howmuch = tk.StringVar()
    howmuch.set(0)
    payment_label = tk.Label(money, text ='Type payment amount:', font=('Arial', 12))
    payment_label.grid(row=yrow + 7, columnspan=3, sticky='E', pady=10)
    payment = tk.Entry(money, textvariable=howmuch, bd=5)
    payment.grid(row=yrow + 7, column=3, sticky='W', pady=10)
    confirm = tk.Button(money, text='Confirm payment',font=('Arial', 12), command=paymentcheck)
    confirm.grid(row=yrow + 7, column=4, sticky='W', pady=10)

def show_cart(category_chosen):
    remove_current_page()
    def cart_change(itemcode, category_chosen): #if users wants to remove a selected item from cart
        print(itemcode)
        for category in range(1,6):
            for item in range(1,5):
                if Appendix[category][item][1] == itemcode:
                    Appendix[category][item][2]['qty'] = 0
                    show_cart(category_chosen)

    def apply_discount(current, discount): #occurs when a checkbutton for discounts is clicked
        checker = current.get()
        if checker == 1:
            DISCOUNTS[discount]['status'] = True
        elif checker == 0:
            DISCOUNTS[discount]['status'] = False

        if DISCOUNTS['NS_Men']['status'] == True and DISCOUNTS['senior']['status'] == True:
            DISCOUNTS['NS_Men']['status'] = False
            DISCOUNTS['senior']['status'] = False
            status_senior.set(False)
            status_NS_Men.set(False)
        percentage = f'Current discount: {percent_calc()}%'
        x.set(percentage)

    cart_dict.clear() #removes all items in cart_dict
    for cat in range(1,6):
        for items in range(1,5):
            if Appendix[cat][items][2]['qty']>0:
                item = Appendix[cat][items][1]
                cart_dict[f'{item}'] = {'Name':Appendix[cat][items][0],
                                        'item code':item,
                                        'cost':Appendix[cat][items][2]['cost'],
                                        'qty':Appendix[cat][items][2]['qty'],
                                        'total':Appendix[cat][items][2]['total']
                                        } # adds items and their information to cart_dict

    cartpageframe = tk.Frame(root, bg='cornflower blue')
    cartpageframe.pack(expand=True, fill='both',side='top')

    bottompage = tk.Frame(root)
    bottompage.pack(fill='x', side='bottom')

    for x in range(8):
        cartpageframe.columnconfigure(index=x,weight=1)

    back_to_item_select = tk.Button(cartpageframe, text='Back', font=(18), bg='light blue', bd=10,
                          command=lambda: item_list_show(category_chosen))
    back_to_item_select.grid(column=0, row=0, padx=5, pady=5)

    pagename = tk.Label(cartpageframe, text='Cart', font=('Arial', 18),bg='dodger blue')
    pagename.grid(column=1, row=0, sticky='W', padx=20, pady=10)

    total_cost_All = total_cost_all_cat()
    for item in range(5):  # shows item frame(item,itemcode,cost,qty and total labels)
        frameitem = tk.Label(cartpageframe, text=Appendix[0][item], font=('Arial', 10))
        frameitem.grid(column=1+item, row=1, sticky='NW', padx=20, pady=5)

    rowset=2
    for itemcode in cart_dict:
        columnset = 1 #starting column grid for item details
        for items_details in cart_dict[itemcode]:
            frameitem = tk.Label(cartpageframe, text=cart_dict[itemcode][items_details], font=('Arial', 12))
            frameitem.grid(column=columnset, row=rowset, sticky='NW', padx=20)
            columnset += 1 #postion changing for columns in grid
        changebutton = tk.Button(cartpageframe, text='Remove', font=('Arial',15), bg='green', bd=3,
                                command=lambda itemcode = itemcode:
                                cart_change(itemcode, category_chosen))
        changebutton.grid(column=columnset, row=rowset, sticky='NW', padx=20)
        rowset += 1 #postion changing for rows in grid

    total = tk.Label(bottompage, text=f'Total cost = ${total_cost_All}', font=('Arial', 18))
    total.pack(anchor='w')

    x = tk.IntVar()
    percentage = f'Current discount: {percent_calc()}%'
    x.set(percentage)
    current_discount = tk.Label(bottompage, textvariable=x, font=('Arial', 12))
    current_discount.pack(anchor='nw')

    status_senior = tk.IntVar()
    status_senior.set(DISCOUNTS['senior']['status'])
    senior = tk.Checkbutton(bottompage, text='senior(10%)', variable=status_senior,
                                  command=lambda :apply_discount(status_senior, 'senior'))
    senior.pack(anchor='nw', side='left')

    status_Members_discount = tk.IntVar()
    status_Members_discount.set(DISCOUNTS['Members']['status'])
    Members_discount = tk.Checkbutton(bottompage, text='Members_discount(8%)', variable=status_Members_discount,
                            command=lambda: apply_discount(status_Members_discount, 'Members'))
    Members_discount.pack(anchor='nw',side='left')

    status_NS_Men = tk.IntVar()
    status_NS_Men.set(DISCOUNTS['NS_Men']['status'])
    NS_Men = tk.Checkbutton(bottompage, text='NS_Men(5%)', variable=status_NS_Men,
                            command=lambda: apply_discount(status_NS_Men, 'NS_Men'))
    NS_Men.pack(anchor='nw', side='left')

    restart = tk.Button(bottompage, text='Reset cart items', font=('Arial', 15),
                        command=reset)
    restart.pack(anchor='w')
    checkingout = tk.Button(bottompage, text='Checkout', font=('Arial', 15),
                            command= lambda: bill_statement(category_chosen))
    checkingout.pack(anchor='w')
    if total_cost_All == 0:
        checkingout.configure(state='disabled') #prevents user from assessing checkout if cart is empty

def back_to_main(): #Returns user back to main()
    remove_current_page()
    main()

def Qty_change_item_page(category_chosen, items): #creates a new page holding the current qty of item selected to be changed
    qty_change_item_page = tk.Tk()
    qty_change_item_page.title(f'Change item Qty of {Appendix[category_chosen][items][1]}')
    qty_change_item_page.geometry('350x100')
    def Qty_add_item(chosen): #addition to current amount in created page
        changed = str(chosen.get())
        if changed.isdigit():
            chosen.set(int(chosen.get()) + 1)
        else:
            chosen.set(0)

    def Qty_minus_item(chosen): #subtraction to current amount in created page
        changed = str(chosen.get())
        if changed.isdigit():
            if int(changed) - 1 >= 0:
                chosen.set(int(chosen.get()) - 1)
        else:
            chosen.set(0)

    def set_qty(): #Sends the value(if its a digit) to the Appendix list to be saved.
        typed = str(chosen.get())
        if typed.isdigit():
            Appendix[category_chosen][items][2]['qty'] = int(typed)
            item_list_show(category_chosen)
            qty_change_item_page.destroy()
        else:
            chosen.set('Numbers only')

    for x in range(3):
        qty_change_item_page.columnconfigure(index=x, weight=1)

    add_item = tk.Button(qty_change_item_page, text='+1', font=(18),
                         command=lambda: Qty_add_item(chosen))
    add_item.grid(column=0, row=0)
    minus_item = tk.Button(qty_change_item_page, text='-1', font=(18),
                           command=lambda: Qty_minus_item(chosen))
    minus_item.grid(column=2, row=0)
    chosen = tk.StringVar(qty_change_item_page)
    chosen.set(Appendix[category_chosen][items][2]['qty'])
    num = tk.Entry(qty_change_item_page, textvariable=chosen, font=20)
    num.grid(column=1, row=0)
    num.configure(width=15)

    Changebutton = tk.Button(qty_change_item_page, text='Confirm change', font=(18), bd=10, bg='lime',
                             command=set_qty)
    Changebutton.grid(column=1, row=1)

def item_list_show(category_chosen): #shows the category selected by user
    remove_current_page()
    page2_frame = tk.Frame(bg='cornflower blue')
    page2_frame.pack(expand=True, fill='both')
    for x in range(9): #sets the spacing of each row and column across the entire page.
        page2_frame.columnconfigure(index=x, weight=1)
        page2_frame.rowconfigure(index=x, weight=1)

    back_page = tk.Button(page2_frame, text='Home', font=(18), bg='light blue', bd=10,
                          command=back_to_main)
    back_page.grid(column=0, row=0, pady=15)

    show_all_items = tk.Button(page2_frame, text='Show all(categories and items)', font=(18), bg='light blue', bd=10,
                               command=lambda: show_items_of_category_selected(6)) #send 6 as the information
    show_all_items.grid(column=1, row=8, pady=15, sticky='w')                       #category_chosen.
    cost_all_cat = total_cost_all_cat() #calulates and return value of total across all categories
    cost_current_cat = total_cost_current_cat(category_chosen) #calculates and retun value of total in current category

    category = tk.Label(page2_frame, text=Appendix[category_chosen][0], bg="dodger blue", font=('Arial', 22))
    category.grid(column=1, row=0, pady=15, sticky='w')
    for item_details in range(5):
        # shows item frame(item, itemcode, cost, qty and total as labels)
        frameitem = tk.Label(page2_frame, text=Appendix[0][item_details], font=('Arial', 15))
        frameitem.grid(column=item_details + 1, row=1, sticky='W', padx=10, pady=10)
    for items in range(1, 5):
        for iteminfo in range(2):  # shows the name and code of each item
            item_called = tk.Label(page2_frame, text=Appendix[category_chosen][items][iteminfo], font=('Arial', 15))
            item_called.grid(column=1 + iteminfo, row=items + 1, sticky='W', padx=10, pady=10)
        xpos = 3
        for numbers in Appendix[category_chosen][items][2]: #shows the qty, cost, and total of each item
            cost_of_one = tk.Label(page2_frame, text=Appendix[category_chosen][items][2][numbers], font=('Arial', 15))
            cost_of_one.grid(column=xpos, row=items + 1, sticky='W', padx=10, pady=10)
            xpos += 1 #changes the column positioning in grid

        changebutton = tk.Button(page2_frame, text='Change Qty', font=(18), bg='green', bd=5,
                                 command=lambda items=items: Qty_change_item_page(category_chosen, items))
        changebutton.grid(column=6, row=1 + items)

    total_cost_this_cat = tk.Label(page2_frame,
                                   text=f'Sum cost of category {Appendix[category_chosen][0]}:${cost_current_cat}',
                                   font=('Arial', 15))
    total_cost_this_cat.grid(column=1, row=6, sticky='w')
    total_cost_All = tk.Label(page2_frame,
                              text=f'Sum cost of all categories :${cost_all_cat}',
                              font=('Arial', 15))
    total_cost_All.grid(column=1, row=7, sticky='w')

    cart_page = tk.Button(page2_frame, text='Cart', font=(18),
                          bd=10, command=lambda: show_cart(category_chosen))
    cart_page.grid(column=7, row=8, padx=25)
    if cost_all_cat == 0:
        cart_page.configure(state='disabled') # diabled prevents the button from being pressed

def showall():
    showall = tk.Frame(bg='cornflower blue')
    showall.pack(expand=True, fill='both')
    for x in range(17):
        showall.columnconfigure(index=x, weight=1)
    back_page = tk.Button(showall, text='Home', font=(18), bg='light blue', bd=10,
                          command=back_to_main)
    back_page.grid(column=0, row=0, padx=10, pady=10)
    #postioning for labels and buttons
    xcolumn = 1
    yrow = 2
    for category in range(1, 6):
        if category == 4:
            xcolumn = 1
            yrow = 8

        button_cat = tk.Button(showall, text=Appendix[category][0], bg="light blue", bd=10,
                               font=('Arial', 15),
                               command=lambda category_chosen=category: show_items_of_category_selected(category_chosen))
        button_cat.grid(column=xcolumn, row=yrow - 1, sticky='w', pady=15)
        for items_frame in range(4):  # shows item frame(item, itemcode, cost, and qty  as labels)
            frameitem = tk.Label(showall, text=Appendix[0][items_frame], font=('Arial', 9))
            frameitem.grid(column=xcolumn + items_frame, row=yrow, sticky='w', pady=5)
        for items in range(1, 5): # shows item information(name, itemcode, cost, and qty as labels)
            item_name = tk.Label(showall, text=Appendix[category][items][0], font=('Arial', 9))
            item_name.grid(column=xcolumn, row=yrow + items, sticky='w', pady=5)
            item_code = tk.Label(showall, text=Appendix[category][items][1], font=('Arial', 9))
            item_code.grid(column=xcolumn + 1, row=yrow + items, sticky='w', pady=5)
            item_cost = tk.Label(showall, text=Appendix[category][items][2]['cost'], font=('Arial', 9))
            item_cost.grid(column=xcolumn + 2, row=yrow + items, sticky='w', pady=5)
            item_qty = tk.Label(showall, text=Appendix[category][items][2]['qty'], font=('Arial', 9))
            item_qty.grid(column=xcolumn + 3, row=yrow + items, sticky='s', pady=5)
        xcolumn += 4

    totalcostlabel = tk.Label(showall, text=f'total cost =${total_cost_all_cat()}', font=('Arial', 15))
    totalcostlabel.grid(column=9, row=13, sticky='w')

def show_items_of_category_selected(category_chosen): #displays depend on category chosen by user
    remove_current_page()
    if category_chosen != 6: #if user does not want 'Show all'
        item_list_show(category_chosen)
    else:
        showall()

def main():
    mainframe = tk.Frame(bg='cornflower blue')
    mainframe.pack(expand=True, fill='both')
    exitbutton = tk.Button(mainframe, text='Exit', font=('Arial', 18), bd=5, command=root.quit)
    exitbutton.grid(column=0, row=0, padx=10, pady=10)
    label = tk.Label(mainframe, text='Shopping GUI', font=('Arial', 35),
                     bg="dodger blue")
    label.grid(column=2, row=0, pady=20)
    categories = tk.Label(mainframe, text='Categories:', font=('Arial', 30),
                          bg="dodger blue")
    categories.grid(column=2, row=1, pady=20)
    yrow = 2
    for y in range(4):
        mainframe.rowconfigure(index=y, weight=1)
    for x in range(5):
        mainframe.columnconfigure(index=x, weight=1)
        xcolumn = x + 1
        cat = x + 1 #cat is category
        if x >= 3: #this if formatting for button positions
            yrow = 3
            xcolumn = x - 2
        button = tk.Button(mainframe, text=Appendix[cat][0], font=(18), bg="light blue", bd=10,
                           command=lambda category_chosen=cat: show_items_of_category_selected(category_chosen))
        button.grid(column=xcolumn, row=yrow, pady=20, ipadx=20, ipady=10)
    all_button = tk.Button(mainframe, text='Show All', font=(18), bg="light blue", bd=10,
                           command=lambda: show_items_of_category_selected(6))
    all_button.grid(column=3, row=3, pady=20, ipadx=20, ipady=10)

main()
root.mainloop()