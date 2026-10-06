
# ============================================================
# CA3 PRACTICE PROJECT
# PYTHON-BASED BUSINESS CHATBOT
# OFFICE SUPPLIES PROCUREMENT CHATBOT
# ============================================================
#
# Version 7
#
# Features:
# 1. Greeting
# 2. Multiple product identification
# 3. Accurate product matching
# 4. Quantity collection one-by-one
# 5. Multiple product quantities
# 6. Total cost calculation
# 7. Budget checking
# 8. Quantity reduction when over budget
# 9. Add more products
# 10. Add missing quantities
# 11. Delivery requirement
# 12. Bulk order detection
# 13. Final structured summary
# 14. Conversation continues until "bye"
# ============================================================


import re


# ============================================================
# 1. PRODUCT DATABASE
# ============================================================

PRODUCTS = {

    "ball pen": {
        "category": "Writing Supplies",
        "price": 10,
        "unit": "piece"
    },

    "gel pen": {
        "category": "Writing Supplies",
        "price": 20,
        "unit": "piece"
    },

    "pencil": {
        "category": "Writing Supplies",
        "price": 8,
        "unit": "piece"
    },

    "notebook": {
        "category": "Paper Supplies",
        "price": 60,
        "unit": "piece"
    },

    "printer paper": {
        "category": "Paper Supplies",
        "price": 300,
        "unit": "ream"
    },

    "sticky notes": {
        "category": "Desk Supplies",
        "price": 50,
        "unit": "pack"
    },

    "stapler": {
        "category": "Desk Supplies",
        "price": 120,
        "unit": "piece"
    },

    "staples": {
        "category": "Desk Supplies",
        "price": 40,
        "unit": "box"
    },

    "file folder": {
        "category": "Filing Supplies",
        "price": 30,
        "unit": "piece"
    },

    "marker": {
        "category": "Writing Supplies",
        "price": 25,
        "unit": "piece"
    },

    "envelope": {
        "category": "Paper Supplies",
        "price": 5,
        "unit": "piece"
    },

    "calculator": {
        "category": "Desk Supplies",
        "price": 350,
        "unit": "piece"
    }
}


# ============================================================
# 2. PRODUCT ALIASES
# ============================================================

ALIASES = {

    "pen": "ball pen",
    "pens": "ball pen",
    "ball pens": "ball pen",

    "gel pen": "gel pen",
    "gel pens": "gel pen",

    "pencil": "pencil",
    "pencils": "pencil",

    "notebook": "notebook",
    "notebooks": "notebook",

    "paper": "printer paper",
    "papers": "printer paper",
    "printer paper": "printer paper",
    "printer papers": "printer paper",

    "sticky note": "sticky notes",
    "sticky notes": "sticky notes",

    "stapler": "stapler",
    "staplers": "stapler",

    "staple": "staples",
    "staples": "staples",

    "folder": "file folder",
    "folders": "file folder",
    "file folder": "file folder",
    "file folders": "file folder",

    "marker": "marker",
    "markers": "marker",

    "envelope": "envelope",
    "envelopes": "envelope",

    "calculator": "calculator",
    "calculators": "calculator"
}


# ============================================================
# 3. ACCURATE PRODUCT EXTRACTION
# ============================================================
#
# IMPORTANT:
# Uses WORD BOUNDARIES.
#
# Therefore:
# "pencils" will NOT match "pen"
# "markers" will NOT accidentally match another word
# ============================================================

def extract_products(text):

    text = text.lower()

    found_products = []

    # --------------------------------------------------------
    # Check actual product names first
    # --------------------------------------------------------

    sorted_products = sorted(
        PRODUCTS.keys(),
        key=len,
        reverse=True
    )

    for product in sorted_products:

        pattern = r'\b' + re.escape(product) + r'\b'

        if re.search(pattern, text):

            if product not in found_products:

                found_products.append(product)

    # --------------------------------------------------------
    # Check aliases using word boundaries
    # --------------------------------------------------------

    sorted_aliases = sorted(
        ALIASES.keys(),
        key=len,
        reverse=True
    )

    for alias in sorted_aliases:

        pattern = r'\b' + re.escape(alias) + r'\b'

        if re.search(pattern, text):

            product = ALIASES[alias]

            if product not in found_products:

                found_products.append(product)

    return found_products


# ============================================================
# 4. QUANTITY EXTRACTION
# ============================================================

def extract_quantity(text):

    text = text.lower()

    match = re.search(
        r'\b(\d+(?:\.\d+)?)\b',
        text
    )

    if match:

        quantity = float(match.group(1))

        if quantity.is_integer():

            quantity = int(quantity)

        return quantity

    return None


# ============================================================
# 5. BUDGET EXTRACTION
# ============================================================

def extract_budget(text):

    text = text.lower()

    match = re.search(
        r'(?:₹|rs\.?|rupees)?\s*(\d+(?:,\d+)*)',
        text
    )

    if match:

        value = match.group(1).replace(",", "")

        return float(value)

    return None


# ============================================================
# 6. DELIVERY EXTRACTION
# ============================================================

def extract_delivery(text):

    text = text.lower().strip()

    # Correct common spelling mistake
    text = text.replace("tommorow", "tomorrow")

    if "tomorrow" in text:

        return "Tomorrow"

    if "today" in text:

        return "Today"

    if "urgent" in text or "asap" in text:

        return "Urgent / ASAP"

    if "fast" in text:

        return "Fast Delivery"

    match = re.search(
        r'within\s+(\d+)\s+days?',
        text
    )

    if match:

        return "Within " + match.group(1) + " days"

    match = re.search(
        r'in\s+(\d+)\s+days?',
        text
    )

    if match:

        return "In " + match.group(1) + " days"

    if "standard" in text:

        return "Standard Delivery"

    return text.capitalize()


# ============================================================
# 7. YES / NO DETECTION
# ============================================================

def is_yes(text):

    text = text.lower().strip()

    return text in [
        "yes",
        "y",
        "yeah",
        "yep",
        "sure",
        "okay",
        "ok",
        "of course"
    ]


def is_no(text):

    text = text.lower().strip()

    return text in [
        "no",
        "n",
        "nope",
        "not now"
    ]


# ============================================================
# 8. ADD MORE PRODUCT REQUEST
# ============================================================

def wants_to_add_more(text):

    text = text.lower().strip()

    phrases = [

        "add more",
        "add another",
        "add another product",
        "add more products",
        "i need to add more",
        "i want to add more",
        "need more products",
        "add one more",
        "forgot a product",
        "forgot some products",
        "include another",
        "include more"
    ]

    for phrase in phrases:

        if phrase in text:

            return True

    return False


# ============================================================
# 9. INTENT IDENTIFICATION
# ============================================================

def identify_intent(text, stage):

    text_lower = text.lower().strip()

    if text_lower in [
        "bye",
        "goodbye",
        "exit",
        "quit"
    ]:

        return "GOODBYE"

    if text_lower in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:

        return "GREETING"

    if wants_to_add_more(text):

        return "PRODUCT_SEARCH"

    if stage == "PRODUCTS":

        return "PRODUCT_SEARCH"

    if stage == "QUANTITY":

        return "QUANTITY"

    if stage == "BUDGET":

        return "PRICE"

    if stage == "DELIVERY":

        return "DELIVERY"

    if "category" in text_lower:

        return "CATEGORY"

    if "bulk" in text_lower:

        return "BULK_ENQUIRY"

    return "UNKNOWN"


# ============================================================
# 10. CHATBOT CLASS
# ============================================================

class OfficeSuppliesChatbot:

    def __init__(self):

        self.stage = "PRODUCTS"

        # Products selected by user
        self.selected_products = []

        # Product -> quantity
        self.order_items = {}

        # Current quantity index
        self.current_product_index = 0

        # Budget
        self.budget = None

        # Delivery
        self.delivery = None

        # Whether chatbot is asking about reducing quantity
        self.reducing_quantity = False

        # Whether chatbot is asking which product to reduce
        self.asking_reduction_product = False

        # Whether chatbot is asking new quantity
        self.reduction_product = None

        # Whether chatbot is adding more products
        self.adding_more = False


    # ========================================================
    # SHOW PRODUCTS
    # ========================================================

    def show_products(self):

        print("\nAvailable Office Supplies:")
        print("-" * 65)

        for product, details in PRODUCTS.items():

            print(
                f"{product.title():20} | "
                f"{details['category']:18} | "
                f"₹{details['price']} per {details['unit']}"
            )

        print("-" * 65)


    # ========================================================
    # CALCULATE TOTAL
    # ========================================================

    def calculate_total(self):

        total = 0

        for product, quantity in self.order_items.items():

            price = PRODUCTS[product]["price"]

            total += quantity * price

        return total


    # ========================================================
    # GET CURRENT PRODUCT
    # ========================================================

    def get_current_product(self):

        if self.current_product_index < len(
            self.selected_products
        ):

            return self.selected_products[
                self.current_product_index
            ]

        return None


    # ========================================================
    # ASK QUANTITY
    # ========================================================

    def ask_next_quantity(self):

        product = self.get_current_product()

        if product is None:

            return

        details = PRODUCTS[product]

        print(
            f"\nBot: How many {details['unit']}s of "
            f"{product.title()} would you like?"
        )


    # ========================================================
    # PROCESS PRODUCTS
    # ========================================================

    def process_products(self, text):

        products = extract_products(text)

        if not products:

            print(
                "\nBot: I could not identify any valid "
                "office supply."
            )

            print(
                "Bot: Please enter products such as "
                "pencils, notebooks, markers or printer paper."
            )

            return

        # ----------------------------------------------------
        # Add only products that are not already selected
        # ----------------------------------------------------

        new_products = []

        for product in products:

            if product not in self.selected_products:

                self.selected_products.append(product)

                new_products.append(product)

        if not new_products:

            print(
                "\nBot: Those products are already in your order."
            )

            if self.stage == "PRODUCTS":

                self.ask_next_quantity()

            return

        print(
            f"\nBot: I identified {len(new_products)} product(s):"
        )

        for product in new_products:

            details = PRODUCTS[product]

            print(
                f"     • {product.title()} "
                f"({details['category']})"
            )

        # ----------------------------------------------------
        # If this is a new product addition
        # ----------------------------------------------------

        if self.adding_more:

            print(
                "\nBot: I have added the new product(s) "
                "to your order."
            )

            self.adding_more = False

        self.stage = "QUANTITY"

        # ----------------------------------------------------
        # Find first product without quantity
        # ----------------------------------------------------

        self.current_product_index = 0

        while (
            self.current_product_index
            < len(self.selected_products)
            and self.selected_products[
                self.current_product_index
            ] in self.order_items
        ):

            self.current_product_index += 1

        if self.current_product_index < len(
            self.selected_products
        ):

            self.ask_next_quantity()

        else:

            self.all_quantities_collected()


    # ========================================================
    # PROCESS QUANTITY
    # ========================================================

    def process_quantity(self, text):

        quantity = extract_quantity(text)

        if quantity is None or quantity <= 0:

            print(
                "\nBot: Please enter a valid quantity."
            )

            return

        product = self.get_current_product()

        if product is None:

            self.all_quantities_collected()

            return

        self.order_items[product] = quantity

        details = PRODUCTS[product]

        item_total = quantity * details["price"]

        print(
            f"\nBot: {quantity} {details['unit']}(s) "
            f"of {product.title()} added."
        )

        print(
            f"Bot: Estimated cost: ₹{item_total:,.2f}"
        )

        self.current_product_index += 1

        # ----------------------------------------------------
        # Check for remaining products
        # ----------------------------------------------------

        while (
            self.current_product_index
            < len(self.selected_products)
            and self.selected_products[
                self.current_product_index
            ] in self.order_items
        ):

            self.current_product_index += 1

        if self.current_product_index < len(
            self.selected_products
        ):

            self.ask_next_quantity()

        else:

            self.all_quantities_collected()


    # ========================================================
    # ALL QUANTITIES COLLECTED
    # ========================================================

    def all_quantities_collected(self):

        total = self.calculate_total()

        print(
            "\nBot: All product quantities have been recorded."
        )

        print(
            f"Bot: Combined estimated order total is "
            f"₹{total:,.2f}."
        )

        self.stage = "BUDGET"

        self.ask_budget()


    # ========================================================
    # ASK BUDGET
    # ========================================================

    def ask_budget(self):

        print(
            "\nBot: What is your maximum budget "
            "for this order?"
        )


    # ========================================================
    # PROCESS BUDGET
    # ========================================================

    def process_budget(self, text):

        budget = extract_budget(text)

        if budget is None or budget <= 0:

            print(
                "\nBot: Please enter a valid budget."
            )

            return

        self.budget = budget

        total = self.calculate_total()

        print(
            f"\nBot: Your maximum budget is "
            f"₹{budget:,.2f}."
        )

        print(
            f"Bot: Current order total is "
            f"₹{total:,.2f}."
        )

        # ----------------------------------------------------
        # Order is within budget
        # ----------------------------------------------------

        if total <= budget:

            remaining = budget - total

            print(
                "\nBot: Good news! Your order is "
                "within your budget."
            )

            print(
                f"Bot: Remaining budget: ₹{remaining:,.2f}"
            )

            print(
                "\nBot: Would you like to add any more "
                "products before delivery?"
            )

            self.stage = "ADD_MORE"

        # ----------------------------------------------------
        # Order exceeds budget
        # ----------------------------------------------------

        else:

            excess = total - budget

            print(
                "\nBot: Your order exceeds the budget "
                f"by ₹{excess:,.2f}."
            )

            print(
                "Bot: Would you like to reduce the "
                "quantity of any product?"
            )

            self.stage = "REDUCE"


    # ========================================================
    # PROCESS REDUCTION DECISION
    # ========================================================

    def process_reduction_decision(self, text):

        if is_yes(text):

            print(
                "\nBot: Which product quantity would "
                "you like to reduce?"
            )

            print(
                "Bot: Your current quantities are:"
            )

            for product, quantity in self.order_items.items():

                print(
                    f"     • {product.title()}: {quantity}"
                )

            self.stage = "REDUCE_PRODUCT"

            return

        if is_no(text):

            print(
                "\nBot: No problem. We can keep the "
                "current quantities."
            )

            print(
                "Bot: You can still add more products "
                "if required."
            )

            print(
                "\nBot: Would you like to add more products?"
            )

            self.stage = "ADD_MORE"

            return

        print(
            "\nBot: Please answer Yes or No."
        )


    # ========================================================
    # SELECT PRODUCT TO REDUCE
    # ========================================================

    def process_reduction_product(self, text):

        products = extract_products(text)

        selected_product = None

        for product in products:

            if product in self.order_items:

                selected_product = product

                break

        if selected_product is None:

            print(
                "\nBot: I could not identify a product "
                "from your current order."
            )

            print(
                "Bot: Please choose one of these:"
            )

            for product, quantity in self.order_items.items():

                print(
                    f"     • {product.title()} "
                    f"({quantity} currently)"
                )

            return

        self.reduction_product = selected_product

        current_quantity = self.order_items[
            selected_product
        ]

        print(
            f"\nBot: Current quantity of "
            f"{selected_product.title()} is "
            f"{current_quantity}."
        )

        print(
            f"Bot: What should the new quantity of "
            f"{selected_product.title()} be?"
        )

        self.stage = "REDUCE_QUANTITY"


    # ========================================================
    # PROCESS REDUCED QUANTITY
    # ========================================================

    def process_reduction_quantity(self, text):

        new_quantity = extract_quantity(text)

        if new_quantity is None or new_quantity < 0:

            print(
                "\nBot: Please enter a valid quantity."
            )

            return

        product = self.reduction_product

        old_quantity = self.order_items[product]

        # ----------------------------------------------------
        # Zero means remove product
        # ----------------------------------------------------

        if new_quantity == 0:

            del self.order_items[product]

            self.selected_products.remove(product)

            print(
                f"\nBot: {product.title()} has been "
                "removed from the order."
            )

        else:

            self.order_items[product] = new_quantity

            print(
                f"\nBot: Quantity of {product.title()} "
                f"changed from {old_quantity} "
                f"to {new_quantity}."
            )

        # ----------------------------------------------------
        # Recalculate
        # ----------------------------------------------------

        total = self.calculate_total()

        print(
            f"Bot: New estimated order total: "
            f"₹{total:,.2f}"
        )

        # ----------------------------------------------------
        # Check budget again
        # ----------------------------------------------------

        if self.budget is not None:

            if total <= self.budget:

                remaining = self.budget - total

                print(
                    "\nBot: Great! The revised order is "
                    "now within your budget."
                )

                print(
                    f"Bot: Remaining budget: "
                    f"₹{remaining:,.2f}"
                )

                print(
                    "\nBot: Would you like to add "
                    "more products?"
                )

                self.stage = "ADD_MORE"

            else:

                excess = total - self.budget

                print(
                    "\nBot: The order still exceeds "
                    f"your budget by ₹{excess:,.2f}."
                )

                print(
                    "Bot: Would you like to reduce "
                    "another product?"
                )

                self.stage = "REDUCE"


    # ========================================================
    # PROCESS ADD MORE DECISION
    # ========================================================

    def process_add_more(self, text):

        # ----------------------------------------------------
        # User wants to add more
        # ----------------------------------------------------

        if is_yes(text) or wants_to_add_more(text):

            print(
                "\nBot: Sure! Please tell me the "
                "additional product or products."
            )

            self.stage = "ADD_PRODUCTS"

            return

        # ----------------------------------------------------
        # User does not want more
        # ----------------------------------------------------

        if is_no(text):

            self.stage = "DELIVERY"

            print(
                "\nBot: When would you like the "
                "order delivered?"
            )

            return

        # ----------------------------------------------------
        # User directly provides a product
        # ----------------------------------------------------

        products = extract_products(text)

        if products:

            self.adding_more = True

            self.stage = "ADD_PRODUCTS"

            self.process_products(text)

            return

        print(
            "\nBot: Please answer Yes or No, or "
            "tell me the product you want to add."
        )


    # ========================================================
    # ADD ADDITIONAL PRODUCTS
    # ========================================================

    def process_add_products(self, text):

        products = extract_products(text)

        if not products:

            print(
                "\nBot: I could not identify the "
                "additional product."
            )

            print(
                "Bot: Please enter the product name."
            )

            return

        self.adding_more = True

        self.process_products(text)


    # ========================================================
    # PROCESS DELIVERY
    # ========================================================

    def process_delivery(self, text):

        delivery = extract_delivery(text)

        if not delivery:

            print(
                "\nBot: Please provide a delivery "
                "requirement."
            )

            return

        self.delivery = delivery

        print(
            f"\nBot: Delivery requirement recorded: "
            f"{delivery}"
        )

        self.stage = "COMPLETE"

        print(
            "\nBot: Your order information is complete."
        )

        print(
            "Bot: You can still type "
            "'add more' if you forgot a product."
        )

        print(
            "Bot: Otherwise, type 'bye' to finish "
            "and view your final summary."
        )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    def show_summary(self):

        total = self.calculate_total()

        print("\n")
        print("=" * 80)
        print("                    FINAL ORDER SUMMARY")
        print("=" * 80)

        print(
            f"{'Product':20}"
            f"{'Category':20}"
            f"{'Qty':8}"
            f"{'Unit Price':12}"
            f"{'Total':12}"
        )

        print("-" * 80)

        for product, quantity in self.order_items.items():

            details = PRODUCTS[product]

            item_total = (
                quantity * details["price"]
            )

            print(
                f"{product.title():20}"
                f"{details['category']:20}"
                f"{str(quantity):8}"
                f"₹{details['price']:10.2f}"
                f"₹{item_total:10.2f}"
            )

        print("-" * 80)

        print(
            f"Combined Order Total: ₹{total:,.2f}"
        )

        # ----------------------------------------------------
        # Bulk order
        # ----------------------------------------------------

        bulk = any(
            quantity >= 100
            for quantity in self.order_items.values()
        )

        if bulk:

            order_type = "Bulk Order"

        else:

            order_type = "Regular Order"

        print(
            f"Order Type: {order_type}"
        )

        # ----------------------------------------------------
        # Budget
        # ----------------------------------------------------

        if self.budget is not None:

            print(
                f"Budget: ₹{self.budget:,.2f}"
            )

            if total <= self.budget:

                print(
                    "Budget Status: Within Budget"
                )

            else:

                print(
                    "Budget Status: Over Budget"
                )

        else:

            print(
                "Budget: Not Provided"
            )

        # ----------------------------------------------------
        # Delivery
        # ----------------------------------------------------

        if self.delivery:

            print(
                f"Delivery Requirement: "
                f"{self.delivery}"
            )

        else:

            print(
                "Delivery Requirement: "
                "Not Provided"
            )

        print("=" * 80)


    # ========================================================
    # MAIN RESPONSE FUNCTION
    # ========================================================

    def respond(self, text):

        text = text.strip()

        if not text:

            print(
                "\nBot: Please enter a response."
            )

            return

        # ----------------------------------------------------
        # Greeting
        # ----------------------------------------------------

        if text.lower() in [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]:

            print(
                "\nBot: Hello! Welcome to the "
                "Office Supplies Procurement Chatbot."
            )

            print(
                "Bot: I can help you order multiple "
                "office supplies."
            )

            self.show_products()

            print(
                "\nBot: What product or products "
                "would you like to order?"
            )

            self.stage = "PRODUCTS"

            return


        # ----------------------------------------------------
        # PRODUCT SELECTION
        # ----------------------------------------------------

        if self.stage == "PRODUCTS":

            self.process_products(text)

            return


        # ----------------------------------------------------
        # QUANTITY
        # ----------------------------------------------------

        if self.stage == "QUANTITY":

            # User may have forgotten to provide a product
            # and instead asks to add more.

            if wants_to_add_more(text):

                self.adding_more = True

                print(
                    "\nBot: Sure. Please tell me the "
                    "additional product."
                )

                self.stage = "ADD_PRODUCTS"

                return

            self.process_quantity(text)

            return


        # ----------------------------------------------------
        # BUDGET
        # ----------------------------------------------------

        if self.stage == "BUDGET":

            self.process_budget(text)

            return


        # ----------------------------------------------------
        # REDUCE QUANTITY DECISION
        # ----------------------------------------------------

        if self.stage == "REDUCE":

            self.process_reduction_decision(text)

            return


        # ----------------------------------------------------
        # SELECT PRODUCT TO REDUCE
        # ----------------------------------------------------

        if self.stage == "REDUCE_PRODUCT":

            self.process_reduction_product(text)

            return


        # ----------------------------------------------------
        # NEW REDUCED QUANTITY
        # ----------------------------------------------------

        if self.stage == "REDUCE_QUANTITY":

            self.process_reduction_quantity(text)

            return


        # ----------------------------------------------------
        # ADD MORE DECISION
        # ----------------------------------------------------

        if self.stage == "ADD_MORE":

            self.process_add_more(text)

            return


        # ----------------------------------------------------
        # ADD PRODUCTS
        # ----------------------------------------------------

        if self.stage == "ADD_PRODUCTS":

            self.process_add_products(text)

            return


        # ----------------------------------------------------
        # DELIVERY
        # ----------------------------------------------------

        if self.stage == "DELIVERY":

            # User forgot a product
            if wants_to_add_more(text):

                self.adding_more = True

                print(
                    "\nBot: Sure! Tell me which "
                    "product you want to add."
                )

                self.stage = "ADD_PRODUCTS"

                return

            self.process_delivery(text)

            return


        # ----------------------------------------------------
        # COMPLETE
        # ----------------------------------------------------

        if self.stage == "COMPLETE":

            # Allow user to add more even after delivery
            # information has been entered.

            if wants_to_add_more(text):

                self.adding_more = True

                print(
                    "\nBot: Sure! Which product "
                    "would you like to add?"
                )

                self.stage = "ADD_PRODUCTS"

                return

            print(
                "\nBot: Your order information is "
                "already complete."
            )

            print(
                "Bot: Type 'bye' to finish the "
                "conversation."
            )

            return



# ============================================================
# 11. STREAMLIT INTERFACE
# ============================================================

import streamlit as st
from contextlib import redirect_stdout
from io import StringIO

st.set_page_config(
    page_title="Office Supplies Procurement Chatbot",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 Office Supplies Procurement Chatbot")
st.caption("Python-based business chatbot for office-supplies procurement")

# Keep the student's chatbot object alive across Streamlit reruns.
if "chatbot" not in st.session_state:
    st.session_state.chatbot = OfficeSuppliesChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False

# Sidebar: product catalogue
with st.sidebar:
    st.header("Available Office Supplies")
    for product, details in PRODUCTS.items():
        st.write(
            f"**{product.title()}** — ₹{details['price']} / {details['unit']}"
        )

    if st.button("🔄 Start New Order", use_container_width=True):
        st.session_state.chatbot = OfficeSuppliesChatbot()
        st.session_state.messages = []
        st.session_state.started = False
        st.rerun()

# Welcome message
if not st.session_state.started:
    welcome = (
        "Hello! Welcome to the Office Supplies Procurement Chatbot.\n\n"
        "I can help you order multiple products, manage quantities, "
        "check your budget and arrange delivery.\n\n"
        "**What product or products would you like to order?**"
    )
    st.session_state.messages.append(
        {"role": "assistant", "content": welcome}
    )
    st.session_state.started = True

# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input(
    "Type your request... e.g., 10 pens and 5 notebooks"
)

if user_input:
    # Display and store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Special handling for bye, preserving student's final-summary behaviour
    if user_input.lower().strip() in ["bye", "goodbye", "exit", "quit"]:
        output = StringIO()

        with redirect_stdout(output):
            print("Thank you for using the Office Supplies Procurement Chatbot!")

            if st.session_state.chatbot.order_items:
                st.session_state.chatbot.show_summary()
            else:
                print("No order was created.")

            print("Goodbye! Have a great day.")

        bot_response = output.getvalue()

    else:
        # The student's original respond() uses print().
        # Capture those prints and display them in Streamlit.
        output = StringIO()

        with redirect_stdout(output):
            st.session_state.chatbot.respond(user_input)

        bot_response = output.getvalue()

        if not bot_response.strip():
            bot_response = "I could not generate a response. Please try again."

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_response}
    )

    with st.chat_message("assistant"):
        st.markdown(bot_response)

# Current order status
chatbot = st.session_state.chatbot

if chatbot.order_items:
    with st.expander("📋 Current Order Details", expanded=False):
        rows = []

        for product, quantity in chatbot.order_items.items():
            details = PRODUCTS[product]
            rows.append({
                "Product": product.title(),
                "Category": details["category"],
                "Quantity": quantity,
                "Unit Price": f"₹{details['price']:,.2f}",
                "Item Total": f"₹{quantity * details['price']:,.2f}"
            })

        st.table(rows)

        total = chatbot.calculate_total()
        st.metric("Current Order Total", f"₹{total:,.2f}")

        if chatbot.budget is not None:
            status = (
                "Within Budget"
                if total <= chatbot.budget
                else "Over Budget"
            )
            st.write(f"**Budget:** ₹{chatbot.budget:,.2f}")
            st.write(f"**Budget Status:** {status}")

        if chatbot.delivery:
            st.write(f"**Delivery:** {chatbot.delivery}")
