import re

# ============================================================
# 1. PRODUCT DATABASE
# ============================================================

products = {
    "t-shirt": {
        "category": "T-Shirts",
        "brand": "UrbanWear",
        "price_min": 499,
        "price_max": 999,
        "sizes": ["S", "M", "L", "XL"],
        "stock": 15
    },
    "shirt": {
        "category": "Shirts",
        "brand": "UrbanWear",
        "price_min": 999,
        "price_max": 1899,
        "sizes": ["S", "M", "L", "XL"],
        "stock": 8
    },
    "jeans": {
        "category": "Jeans",
        "brand": "DenimCo",
        "price_min": 1499,
        "price_max": 2799,
        "sizes": ["28", "30", "32", "34", "36"],
        "stock": 6
    },
    "jacket": {
        "category": "Jackets",
        "brand": "StyleHub",
        "price_min": 1999,
        "price_max": 3999,
        "sizes": ["M", "L", "XL"],
        "stock": 4
    },
    "dress": {
        "category": "Dresses",
        "brand": "StyleHub",
        "price_min": 1599,
        "price_max": 3299,
        "sizes": ["S", "M", "L"],
        "stock": 7
    },
    "hoodie": {
        "category": "Hoodies",
        "brand": "UrbanWear",
        "price_min": 1299,
        "price_max": 2499,
        "sizes": ["S", "M", "L", "XL"],
        "stock": 10
    }
}


# ============================================================
# 2. HELPER EXTRACTION FUNCTIONS
# ============================================================

def find_product(message):
    message = message.lower()

    plural_map = {
        "dresses": "dress",
        "dress": "dress",
        "t-shirts": "t-shirt",
        "t-shirt": "t-shirt",
        "tshirts": "t-shirt",
        "tshirt": "t-shirt",
        "shirts": "shirt",
        "shirt": "shirt",
        "jeans": "jeans",
        "jackets": "jacket",
        "jacket": "jacket",
        "hoodies": "hoodie",
        "hoodie": "hoodie"
    }

    sorted_words = sorted(plural_map.keys(), key=len, reverse=True)

    for word in sorted_words:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, message):
            return plural_map[word]

    return None


def extract_specific_size(message):
    message = message.upper().strip()
    letter_match = re.search(r'\b(XS|S|M|L|XL|XXL)\b', message)
    if letter_match:
        return letter_match.group(1)

    num_match = re.search(r'\b(2[8-9]|3[0-6])\b', message)
    if num_match:
        return num_match.group(1)

    return None


def extract_price(message):
    match = re.search(r'(?:₹|rs\.?|for\s+)?\b([1-9]\d{2,4})\b', message, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


# ============================================================
# 3. DETECT INTENT
# ============================================================

def detect_intent(message):
    text = message.lower().strip()

    # Passive Acknowledgments vs Direct Affirmative/Negative
    if text in ["ok", "okay", "k", "got it", "alright", "fine", "understood"]:
        return "ACKNOWLEDGMENT"
    if text in ["yes", "yeah", "yep", "sure"]:
        return "AFFIRMATIVE"
    if text in ["no", "nope", "nah"]:
        return "NEGATIVE"

    # Ordering Process Inquiry
    if re.search(r'\b(order|ordering|buy|purchase|how to order|how to buy|place order)\b', text):
        return "ORDERING"

    # Specific Dispatch Timing Inquiry ("when it dispatches")
    if re.search(r'\b(when)\b', text) and re.search(r'\b(dispatch|dispatches|dispatched|ship|shipped|ships)\b', text):
        return "WHEN_DISPATCHES"

    # Dispatch Notification Inquiry ("how am I notified of dispatch")
    if re.search(r'\b(know|how|notify|notification|notified|update|status)\b', text) and \
       re.search(r'\b(dispatch|dispatched|sent|shipped)\b', text):
        return "DISPATCH_NOTIFICATION"

    # Delivery Delays & Product Support Issues
    if re.search(r'\b(delay|delayed|late|not delivered|not received|haven\'t received|stuck|where is my)\b', text) or \
       re.search(r'\b(defect|defective|damaged|wrong|broken|missing|issue|problem|faulty|complaint|bad|size issue)\b', text):
        return "PRODUCT_OR_DELIVERY_ISSUE"

    # Standard Delivery & Shipping Questions
    if re.search(r'\b(deliver|delivery|shipping|ship|dispatched|dispatch|track|tracking)\b', text):
        return "DELIVERY"

    # Greetings / Farewells
    if re.search(r'\b(hi|hy|hello|hey|good morning|good evening)\b', text):
        return "GREETING"
    if re.search(r'\b(bye|goodbye|quit|exit)\b', text):
        return "GOODBYE"
    if re.search(r'\b(thank|thanks|thx)\b', text):
        return "THANKS"

    # Multi-attribute Query (Price + Size/Product)
    if extract_price(text) and (extract_specific_size(text) or find_product(text)):
        return "COMPLEX_QUERY"

    # Product Mention (Direct Product Enquiries)
    if find_product(text):
        return "PRODUCT_ENQUIRY"

    # Specific Product Feature Queries
    if re.search(r'\b(return|refund|exchange|replace)\b', text):
        return "RETURN"
    if re.search(r'\b(price|cost|how much|rate)\b', text):
        return "PRICE"
    if re.search(r'\b(avail|stock|in stock|have|left)\b', text):
        return "AVAILABILITY"

    # Size Checks
    if extract_specific_size(text):
        return "SPECIFIC_SIZE"
    if re.search(r'\b(size|sizes|fit)\b', text):
        return "SIZE"

    return "UNKNOWN"


# ============================================================
# 4. CHATBOT CLASS
# ============================================================

class FashionChatbot:

    def __init__(self):
        self.reset_session()

    def reset_session(self):
        """Clears memory state for a new user/session."""
        self.last_product = None
        self.last_question = None
        self.awaiting_issue_details = False

    def respond(self, message):
        text = message.strip()
        detected_prod = find_product(text)
        if detected_prod:
            self.last_product = detected_prod

        intent = detect_intent(text)

        # Multi-Step Issue Resolution Flow
        if self.awaiting_issue_details and intent not in ["GOODBYE", "GREETING"]:
            self.awaiting_issue_details = False
            self.last_question = None
            return (
                f"Thank you for specifying details: '{text}'. "
                "I have registered this with our support operations team. "
                "We are actively checking with our courier/warehouse partners. "
                "If the order is found lost or damaged, a replacement or full refund will be processed immediately to your original payment method within 24 hours."
            )

        # Acknowledgments ("ok", "got it")
        if intent == "ACKNOWLEDGMENT":
            self.last_question = None
            return "Great! Feel free to ask if you need anything else, like tracking, product details, or return options."

        # Handle Ordering Process
        elif intent == "ORDERING":
            self.last_question = None
            return (
                "To place an order, follow these simple steps:\n"
                "1. Select the product of your choice from the preferred brand.\n"
                "2. Choose an available size along with your preferred color.\n"
                "3. Click 'Add to Cart' to move the item to your shopping cart.\n"
                "4. Proceed to checkout and complete payment via online UPI, Debit Card, or Credit Card."
            )

        # Handle Affirmative ("yes") / Negative ("no")
        elif intent == "AFFIRMATIVE":
            if self.last_question == "ASKED_DELIVERY_DETAILS":
                self.last_question = None
                return (
                    "Standard shipping takes 3–5 business days. Once dispatched, "
                    "orders arrive within 24–48 hours! Shipping is free on orders over ₹999. "
                    "Let me know if you need help with anything else!"
                )

            elif self.last_question == "ASKED_CHECK_SIZES" and self.last_product:
                sizes = products[self.last_product]["sizes"]
                self.last_question = "ASKED_SPECIFIC_SIZE"
                return f"For the {self.last_product}, available sizes are {', '.join(sizes)}. Which specific size are you looking for?"

            elif self.last_question == "ASKED_SPECIFIC_SIZE" and self.last_product:
                sizes = products[self.last_product]["sizes"]
                return f"Great! Please tell me which size you need from the available options: {', '.join(sizes)}."

            elif self.last_question == "ASKED_CHECK_AVAILABILITY" and self.last_product:
                stock = products[self.last_product]["stock"]
                self.last_question = "ASKED_DELIVERY_DETAILS"
                return f"The {self.last_product} currently has {stock} units in stock. Can I help with delivery details?"

            else:
                self.last_question = None
                return "Sounds good! What else can I help you check today?"

        elif intent == "NEGATIVE":
            self.last_question = None
            return "No problem! Let me know if you'd like to browse other items, check prices, or ask policy questions."

        # Dispatch Timing Inquiry ("when it dispatches")
        elif intent == "WHEN_DISPATCHES":
            self.last_question = None
            return (
                "Your product will be dispatched right after the payment is successfully completed! "
                "Orders are processed and handed to our courier partner within 24 hours of payment confirmation."
            )

        # Dispatch Notification Inquiry
        elif intent == "DISPATCH_NOTIFICATION":
            self.last_question = None
            return (
                "Once your product is dispatched, you will receive an automated notification via Email and SMS message! "
                "The message contains your Product Code, Order ID, Dispatch Time, and Dispatch Address, "
                "along with a direct tracking link."
            )

        # Complex Multi-Attribute Query
        elif intent == "COMPLEX_QUERY":
            product = self.last_product
            price_query = extract_price(text)
            size_query = extract_specific_size(text)

            if not product:
                return "Which product are you asking about?"

            data = products[product]
            within_budget = data["price_min"] <= price_query <= data["price_max"]
            size_available = size_query in data["sizes"] if size_query else True

            if within_budget and size_available:
                self.last_question = "ASKED_DELIVERY_DETAILS"
                size_str = f" in size {size_query}" if size_query else ""
                return (
                    f"Yes! We have {product}s available within ₹{price_query}{size_str}. "
                    f"Our prices range from ₹{data['price_min']} to ₹{data['price_max']}, and we currently have {data['stock']} units in stock. "
                    f"Would you like information on delivery or ordering?"
                )

            elif price_query < data["price_min"] and size_available:
                size_str = f" in size {size_query}" if size_query else ""
                return (
                    f"Sorry, our {product}s{size_str} start at ₹{data['price_min']}, "
                    f"so we don't have options for ₹{price_query}. Would you like to check other products?"
                )

            elif within_budget and not size_available:
                return (
                    f"We have {product}s around ₹{price_query}, but size {size_query} is currently unavailable. "
                    f"Available sizes are: {', '.join(data['sizes'])}."
                )

            else:
                return (
                    f"Sorry, we don't have {product}s for ₹{price_query} in size {size_query}. "
                    f"Price range for {product}s is ₹{data['price_min']}–₹{data['price_max']} in sizes {', '.join(data['sizes'])}."
                )

        # Delivery Delays / Support
        elif intent == "PRODUCT_OR_DELIVERY_ISSUE":
            self.awaiting_issue_details = True
            self.last_question = None
            return (
                "I'm sorry to hear you're experiencing an issue with your order/delivery! "
                "Could you please specify the exact issue you are facing (e.g., delay in delivery, damaged item, wrong size received, or missing product) along with your Order ID?"
            )

        # Standard Intents
        elif intent == "GREETING":
            self.last_question = None
            return "Hello! Welcome to our Fashion Store. How can I help you today?"

        elif intent == "DELIVERY":
            self.last_question = "ASKED_DELIVERY_DETAILS"
            return (
                "Orders are dispatched within 24 hours right after payment is completed. Standard delivery takes 2–3 business days. "
                "Delivery is free for orders above ₹999! Would you like details on how to track or know when it dispatches?"
            )

        elif intent == "PRODUCT_ENQUIRY":
            product = self.last_product
            data = products[product]
            self.last_question = "ASKED_CHECK_AVAILABILITY"
            return (
                f"We have {data['category']} from {data['brand']}. "
                f"Prices range from ₹{data['price_min']} to ₹{data['price_max']}. "
                f"Available sizes are {', '.join(data['sizes'])}. "
                f"Would you like to check current stock availability?"
            )

        elif intent == "PRICE":
            if self.last_product:
                product = self.last_product
                data = products[product]
                self.last_question = "ASKED_CHECK_SIZES"
                return (
                    f"The price range for {product} is ₹{data['price_min']} – ₹{data['price_max']}. "
                    f"Would you like to check available sizes?"
                )
            return "Which product's price range would you like to check?"

        elif intent == "SPECIFIC_SIZE":
            requested_size = extract_specific_size(text)
            self.last_question = "ASKED_DELIVERY_DETAILS"
            if self.last_product:
                product = self.last_product
                sizes = products[product]["sizes"]
                if requested_size in sizes:
                    return (
                        f"Yes, size {requested_size} is available for {product}! "
                        f"We have {products[product]['stock']} units left in stock. "
                        f"Would you like to check delivery details?"
                    )
                return f"Sorry, size {requested_size} isn't available for {product}. We carry sizes: {', '.join(sizes)}."
            return f"We carry size {requested_size} across multiple items! Which product are you interested in?"

        elif intent == "SIZE":
            if self.last_product:
                product = self.last_product
                sizes = products[product]["sizes"]
                self.last_question = "ASKED_SPECIFIC_SIZE"
                return f"For the {product}, available sizes are {', '.join(sizes)}. Do you need a specific size?"
            return "Which product would you like size information for?"

        elif intent == "AVAILABILITY":
            if self.last_product:
                product = self.last_product
                stock = products[product]["stock"]
                self.last_question = "ASKED_DELIVERY_DETAILS"
                if stock > 0:
                    return f"Yes, {product} is in stock ({stock} units available)! Would you like delivery details?"
                return f"Sorry, {product} is currently out of stock."
            return "Which product's stock availability would you like to check?"

        elif intent == "RETURN":
            self.last_question = None
            return "Our policy allows returns or exchanges within 7 days of delivery for unused items in original condition."

        elif intent == "THANKS":
            self.last_question = None
            return "You're welcome! Let me know if you need anything else."

        elif intent == "GOODBYE":
            self.last_question = None
            return "Thank you for visiting! Have a wonderful day."

        else:
            self.last_question = None
            if text.lower() in ["product", "products", "clothes", "clothing", "catalog"]:
                return "We offer T-Shirts, Shirts, Jeans, Jackets, Dresses, and Hoodies. Which one would you like to explore?"
            return "I'm sorry, I didn't quite catch that. You can ask about our products, price ranges, sizes, delivery time, tracking, or order issues!"


# ============================================================
# 5. MULTI-CUSTOMER EXECUTION LOOP
# ============================================================

bot = FashionChatbot()

def start_new_chat():
    bot.reset_session()
    print("\n==============================================")
    print("       FASHION STORE CUSTOMER SUPPORT")
    print("==============================================")
    print("Bot: Hello! Welcome to our Fashion Store.")
    print("Bot: How can I help you today?\n")
    print("(Type 'bye' to end the session.)\n")

start_new_chat()

while True:
    user_message = input("You: ")
    if not user_message.strip():
        continue

    response = bot.respond(user_message)
    print("Bot:", response)
    print()

    if detect_intent(user_message) == "GOODBYE":
        new_customer = input("Start a new customer chat session? (yes/no): ").strip().lower()
        if new_customer in ["yes", "y"]:
            start_new_chat()
        else:
            print("Session ended. Goodbye!")
            break
