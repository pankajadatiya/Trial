import re
import streamlit as st

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

    sorted_words = sorted(
        plural_map.keys(),
        key=len,
        reverse=True
    )

    for word in sorted_words:
        pattern = r'\b' + re.escape(word) + r'\b'

        if re.search(pattern, message):
            return plural_map[word]

    return None


def extract_specific_size(message):
    message = message.upper().strip()

    letter_match = re.search(
        r'\b(XS|S|M|L|XL|XXL)\b',
        message
    )

    if letter_match:
        return letter_match.group(1)

    num_match = re.search(
        r'\b(2[8-9]|3[0-6])\b',
        message
    )

    if num_match:
        return num_match.group(1)

    return None


def extract_price(message):
    match = re.search(
        r'(?:₹|rs\.?|for\s+)?\b([1-9]\d{2,4})\b',
        message,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    return None


# ============================================================
# 3. DETECT INTENT
# ============================================================

def detect_intent(message):

    text = message.lower().strip()

    if text in [
        "ok",
        "okay",
        "k",
        "got it",
        "alright",
        "fine",
        "understood"
    ]:
        return "ACKNOWLEDGMENT"

    if text in [
        "yes",
        "yeah",
        "yep",
        "sure"
    ]:
        return "AFFIRMATIVE"

    if text in [
        "no",
        "nope",
        "nah"
    ]:
        return "NEGATIVE"

    if re.search(
        r'\b(order|ordering|buy|purchase|how to order|how to buy|place order)\b',
        text
    ):
        return "ORDERING"

    if (
        re.search(r'\b(when)\b', text)
        and
        re.search(
            r'\b(dispatch|dispatches|dispatched|ship|shipped|ships)\b',
            text
        )
    ):
        return "WHEN_DISPATCHES"

    if (
        re.search(
            r'\b(know|how|notify|notification|notified|update|status)\b',
            text
        )
        and
        re.search(
            r'\b(dispatch|dispatched|sent|shipped)\b',
            text
        )
    ):
        return "DISPATCH_NOTIFICATION"

    if (
        re.search(
            r'\b(delay|delayed|late|not delivered|not received|haven\'t received|stuck|where is my)\b',
            text
        )
        or
        re.search(
            r'\b(defect|defective|damaged|wrong|broken|missing|issue|problem|faulty|complaint|bad|size issue)\b',
            text
        )
    ):
        return "PRODUCT_OR_DELIVERY_ISSUE"

    if re.search(
        r'\b(deliver|delivery|shipping|ship|dispatched|dispatch|track|tracking)\b',
        text
    ):
        return "DELIVERY"

    if re.search(
        r'\b(hi|hy|hello|hey|good morning|good evening)\b',
        text
    ):
        return "GREETING"

    if re.search(
        r'\b(bye|goodbye|quit|exit)\b',
        text
    ):
        return "GOODBYE"

    if re.search(
        r'\b(thank|thanks|thx)\b',
        text
    ):
        return "THANKS"

    if extract_price(text) and (
        extract_specific_size(text)
        or find_product(text)
    ):
        return "COMPLEX_QUERY"

    if find_product(text):
        return "PRODUCT_ENQUIRY"

    if re.search(
        r'\b(return|refund|exchange|replace)\b',
        text
    ):
        return "RETURN"

    if re.search(
        r'\b(price|cost|how much|rate)\b',
        text
    ):
        return "PRICE"

    if re.search(
        r'\b(avail|stock|in stock|have|left)\b',
        text
    ):
        return "AVAILABILITY"

    if extract_specific_size(text):
        return "SPECIFIC_SIZE"

    if re.search(
        r'\b(size|sizes|fit)\b',
        text
    ):
        return "SIZE"

    return "UNKNOWN"


# ============================================================
# 4. CHATBOT CLASS
# ============================================================

class FashionChatbot:

    def __init__(self):
        self.reset_session()

    def reset_session(self):

        self.last_product = None
        self.last_question = None
        self.awaiting_issue_details = False

    def respond(self, message):

        text = message.strip()

        detected_prod = find_product(text)

        if detected_prod:
            self.last_product = detected_prod

        intent = detect_intent(text)

        # ----------------------------------------------------
        # Multi-Step Issue Resolution
        # ----------------------------------------------------

        if (
            self.awaiting_issue_details
            and intent not in ["GOODBYE", "GREETING"]
        ):

            self.awaiting_issue_details = False
            self.last_question = None

            return (
                f"Thank you for specifying details: '{text}'. "
                "I have registered this with our support operations team. "
                "We are actively checking with our courier/warehouse partners. "
                "If the order is found lost or damaged, a replacement or full "
                "refund will be processed immediately to your original payment "
                "method within 24 hours."
            )

        # ----------------------------------------------------
        # Acknowledgment
        # ----------------------------------------------------

        if intent == "ACKNOWLEDGMENT":

            self.last_question = None

            return (
                "Great! Feel free to ask if you need anything else, "
                "like tracking, product details, or return options."
            )

        # ----------------------------------------------------
        # Ordering
        # ----------------------------------------------------

        elif intent == "ORDERING":

            self.last_question = None

            return (
                "To place an order, follow these simple steps:\n\n"
                "1. Select the product of your choice from the preferred brand.\n"
                "2. Choose an available size along with your preferred color.\n"
                "3. Click 'Add to Cart' to move the item to your shopping cart.\n"
                "4. Proceed to checkout and complete payment via online UPI, "
                "Debit Card, or Credit Card."
            )

        # ----------------------------------------------------
        # Affirmative
        # ----------------------------------------------------

        elif intent == "AFFIRMATIVE":

            if self.last_question == "ASKED_DELIVERY_DETAILS":

                self.last_question = None

                return (
                    "Standard shipping takes 3–5 business days. "
                    "Once dispatched, orders arrive within 24–48 hours! "
                    "Shipping is free on orders over ₹999. "
                    "Let me know if you need help with anything else!"
                )

            elif (
                self.last_question == "ASKED_CHECK_SIZES"
                and self.last_product
            ):

                sizes = products[self.last_product]["sizes"]

                self.last_question = "ASKED_SPECIFIC_SIZE"

                return (
                    f"For the {self.last_product}, available sizes are "
                    f"{', '.join(sizes)}. Which specific size are you looking for?"
                )

            elif (
                self.last_question == "ASKED_SPECIFIC_SIZE"
                and self.last_product
            ):

                sizes = products[self.last_product]["sizes"]

                return (
                    f"Great! Please tell me which size you need from "
                    f"the available options: {', '.join(sizes)}."
                )

            elif (
                self.last_question == "ASKED_CHECK_AVAILABILITY"
                and self.last_product
            ):

                stock = products[self.last_product]["stock"]

                self.last_question = "ASKED_DELIVERY_DETAILS"

                return (
                    f"The {self.last_product} currently has {stock} "
                    "units in stock. Can I help with delivery details?"
                )

            else:

                self.last_question = None

                return (
                    "Sounds good! What else can I help you check today?"
                )

        # ----------------------------------------------------
        # Negative
        # ----------------------------------------------------

        elif intent == "NEGATIVE":

            self.last_question = None

            return (
                "No problem! Let me know if you'd like to browse other "
                "items, check prices, or ask policy questions."
            )

        # ----------------------------------------------------
        # Dispatch timing
        # ----------------------------------------------------

        elif intent == "WHEN_DISPATCHES":

            self.last_question = None

            return (
                "Your product will be dispatched right after the payment "
                "is successfully completed! Orders are processed and handed "
                "to our courier partner within 24 hours of payment confirmation."
            )

        # ----------------------------------------------------
        # Dispatch notification
        # ----------------------------------------------------

        elif intent == "DISPATCH_NOTIFICATION":

            self.last_question = None

            return (
                "Once your product is dispatched, you will receive an "
                "automated notification via Email and SMS message! "
                "The message contains your Product Code, Order ID, Dispatch "
                "Time, and Dispatch Address, along with a direct tracking link."
            )

        # ----------------------------------------------------
        # Complex query
        # ----------------------------------------------------

        elif intent == "COMPLEX_QUERY":

            product = self.last_product

            price_query = extract_price(text)
            size_query = extract_specific_size(text)

            if not product:
                return "Which product are you asking about?"

            data = products[product]

            within_budget = (
                data["price_min"]
                <= price_query
                <= data["price_max"]
            )

            size_available = (
                size_query in data["sizes"]
                if size_query
                else True
            )

            if within_budget and size_available:

                self.last_question = "ASKED_DELIVERY_DETAILS"

                size_str = (
                    f" in size {size_query}"
                    if size_query
                    else ""
                )

                return (
                    f"Yes! We have {product}s available within ₹{price_query}"
                    f"{size_str}. Our prices range from "
                    f"₹{data['price_min']} to ₹{data['price_max']}, "
                    f"and we currently have {data['stock']} units in stock. "
                    "Would you like information on delivery or ordering?"
                )

            elif price_query < data["price_min"] and size_available:

                size_str = (
                    f" in size {size_query}"
                    if size_query
                    else ""
                )

                return (
                    f"Sorry, our {product}s{size_str} start at "
                    f"₹{data['price_min']}, so we don't have options "
                    f"for ₹{price_query}. Would you like to check other products?"
                )

            elif within_budget and not size_available:

                return (
                    f"We have {product}s around ₹{price_query}, but size "
                    f"{size_query} is currently unavailable. "
                    f"Available sizes are: {', '.join(data['sizes'])}."
                )

            else:

                return (
                    f"Sorry, we don't have {product}s for ₹{price_query} "
                    f"in size {size_query}. Price range for {product}s is "
                    f"₹{data['price_min']}–₹{data['price_max']} in sizes "
                    f"{', '.join(data['sizes'])}."
                )

        # ----------------------------------------------------
        # Delivery issue
        # ----------------------------------------------------

        elif intent == "PRODUCT_OR_DELIVERY_ISSUE":

            self.awaiting_issue_details = True
            self.last_question = None

            return (
                "I'm sorry to hear you're experiencing an issue with your "
                "order/delivery! Could you please specify the exact issue "
                "you are facing, such as delay in delivery, damaged item, "
                "wrong size received, or missing product, along with your "
                "Order ID?"
            )

        # ----------------------------------------------------
        # Greeting
        # ----------------------------------------------------

        elif intent == "GREETING":

            self.last_question = None

            return (
                "Hello! Welcome to our Fashion Store. "
                "How can I help you today?"
            )

        # ----------------------------------------------------
        # Delivery
        # ----------------------------------------------------

        elif intent == "DELIVERY":

            self.last_question = "ASKED_DELIVERY_DETAILS"

            return (
                "Orders are dispatched within 24 hours right after payment "
                "is completed. Standard delivery takes 2–3 business days. "
                "Delivery is free for orders above ₹999! "
                "Would you like details on how to track or know when it dispatches?"
            )

        # ----------------------------------------------------
        # Product enquiry
        # ----------------------------------------------------

        elif intent == "PRODUCT_ENQUIRY":

            product = self.last_product

            data = products[product]

            self.last_question = "ASKED_CHECK_AVAILABILITY"

            return (
                f"We have {data['category']} from {data['brand']}. "
                f"Prices range from ₹{data['price_min']} to "
                f"₹{data['price_max']}. "
                f"Available sizes are {', '.join(data['sizes'])}. "
                "Would you like to check current stock availability?"
            )

        # ----------------------------------------------------
        # Price
        # ----------------------------------------------------

        elif intent == "PRICE":

            if self.last_product:

                product = self.last_product
                data = products[product]

                self.last_question = "ASKED_CHECK_SIZES"

                return (
                    f"The price range for {product} is "
                    f"₹{data['price_min']} – ₹{data['price_max']}. "
                    "Would you like to check available sizes?"
                )

            return (
                "Which product's price range would you like to check?"
            )

        # ----------------------------------------------------
        # Specific size
        # ----------------------------------------------------

        elif intent == "SPECIFIC_SIZE":

            requested_size = extract_specific_size(text)

            self.last_question = "ASKED_DELIVERY_DETAILS"

            if self.last_product:

                product = self.last_product
                sizes = products[product]["sizes"]

                if requested_size in sizes:

                    return (
                        f"Yes, size {requested_size} is available for "
                        f"{product}! We have "
                        f"{products[product]['stock']} units left in stock. "
                        "Would you like to check delivery details?"
                    )

                return (
                    f"Sorry, size {requested_size} isn't available for "
                    f"{product}. We carry sizes: {', '.join(sizes)}."
                )

            return (
                f"We carry size {requested_size} across multiple items! "
                "Which product are you interested in?"
            )

        # ----------------------------------------------------
        # Size
        # ----------------------------------------------------

        elif intent == "SIZE":

            if self.last_product:

                product = self.last_product
                sizes = products[product]["sizes"]

                self.last_question = "ASKED_SPECIFIC_SIZE"

                return (
                    f"For the {product}, available sizes are "
                    f"{', '.join(sizes)}. Do you need a specific size?"
                )

            return (
                "Which product would you like size information for?"
            )

        # ----------------------------------------------------
        # Availability
        # ----------------------------------------------------

        elif intent == "AVAILABILITY":

            if self.last_product:

                product = self.last_product
                stock = products[product]["stock"]

                self.last_question = "ASKED_DELIVERY_DETAILS"

                if stock > 0:

                    return (
                        f"Yes, {product} is in stock "
                        f"({stock} units available)! "
                        "Would you like delivery details?"
                    )

                return (
                    f"Sorry, {product} is currently out of stock."
                )

            return (
                "Which product's stock availability would you like to check?"
            )

        # ----------------------------------------------------
        # Return
        # ----------------------------------------------------

        elif intent == "RETURN":

            self.last_question = None

            return (
                "Our policy allows returns or exchanges within 7 days "
                "of delivery for unused items in original condition."
            )

        # ----------------------------------------------------
        # Thanks
        # ----------------------------------------------------

        elif intent == "THANKS":

            self.last_question = None

            return (
                "You're welcome! Let me know if you need anything else."
            )

        # ----------------------------------------------------
        # Goodbye
        # ----------------------------------------------------

        elif intent == "GOODBYE":

            self.last_question = None

            return (
                "Thank you for visiting! Have a wonderful day."
            )

        # ----------------------------------------------------
        # Unknown
        # ----------------------------------------------------

        else:

            self.last_question = None

            if text.lower() in [
                "product",
                "products",
                "clothes",
                "clothing",
                "catalog"
            ]:

                return (
                    "We offer T-Shirts, Shirts, Jeans, Jackets, "
                    "Dresses, and Hoodies. Which one would you "
                    "like to explore?"
                )

            return (
                "I'm sorry, I didn't quite catch that. "
                "You can ask about our products, price ranges, "
                "sizes, delivery time, tracking, or order issues!"
            )


# ============================================================
# 5. STREAMLIT APPLICATION
# ============================================================

st.set_page_config(
    page_title="UrbanWear | Fashion Assistant",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 6. PRODUCT IMAGES
# ============================================================

PRODUCT_IMAGES = {

    "t-shirt":
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=85",

    "shirt":
        "https://images.unsplash.com/photo-1603252110481-7ba873bf42ab?auto=format&fit=crop&w=800&q=85",

    "jeans":
        "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=800&q=85",

    "jacket":
        "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=85",

    "dress":
        "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=800&q=85",

    "hoodie":
        "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=800&q=85"
}


PRODUCT_EMOJI = {

    "t-shirt": "👕",
    "shirt": "👔",
    "jeans": "👖",
    "jacket": "🧥",
    "dress": "👗",
    "hoodie": "🧥"
}


# ============================================================
# 7. CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap'
);

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 5% 5%,
            rgba(255, 99, 132, .12),
            transparent 25%
        ),

        radial-gradient(
            circle at 95% 15%,
            rgba(111, 76, 255, .12),
            transparent 25%
        ),

        linear-gradient(
            135deg,
            #fff9fb 0%,
            #f8f7ff 48%,
            #f4fbff 100%
        );
}

.hero {

    border-radius: 28px;

    padding: 34px 38px;

    background:
        linear-gradient(
            120deg,
            #6d28d9 0%,
            #db2777 52%,
            #f97316 100%
        );

    color: white;

    box-shadow:
        0 16px 45px rgba(109,40,217,.22);

    margin-bottom: 22px;
}

.hero h1 {

    font-family:
        'Playfair Display',
        serif;

    font-size: 42px;

    margin:
        0 0 8px 0;
}

.hero p {

    font-size: 17px;

    margin: 0;

    opacity: .95;
}

.pill {

    display: inline-block;

    background:
        rgba(255,255,255,.20);

    border:
        1px solid
        rgba(255,255,255,.30);

    border-radius: 999px;

    padding:
        6px 13px;

    margin-bottom: 13px;

    font-size: 13px;

    font-weight: 700;
}

.product-card {

    background:
        rgba(255,255,255,.92);

    border:
        1px solid
        rgba(120,90,150,.12);

    border-radius: 20px;

    padding: 12px;

    box-shadow:
        0 8px 25px
        rgba(30,20,60,.07);

    margin-bottom: 10px;
}

.product-card h4 {

    margin:
        5px 0 3px 0;

    color: #25133f;
}

.product-card p {

    margin: 0;

    color: #6b6275;

    font-size: 13px;
}

.price {

    color: #d61f69;

    font-size: 18px;

    font-weight: 800;
}

.stock {

    color: #138a54;

    font-size: 12px;

    font-weight: 700;
}

.section-title {

    font-family:
        'Playfair Display',
        serif;

    color: #28123f;

    font-size: 27px;

    margin:
        10px 0 15px 0;
}

.info-box {

    border-radius: 16px;

    padding:
        14px 16px;

    background:
        linear-gradient(
            135deg,
            #fff 0%,
            #f7f3ff 100%
        );

    border:
        1px solid #eadff7;
}

[data-testid="stMetric"] {

    background: white;

    border-radius: 16px;

    padding: 10px;

    box-shadow:
        0 5px 18px
        rgba(30,20,60,.06);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 8. SESSION STATE
# ============================================================

if "bot" not in st.session_state:

    st.session_state.bot = FashionChatbot()


if "messages" not in st.session_state:

    st.session_state.messages = [

        {
            "role": "assistant",

            "content":
                "✨ Welcome to **UrbanWear Fashion Store**!\n\n"
                "I can help you with products, prices, sizes, "
                "stock, delivery, tracking, returns and order issues. "
                "What are you looking for today?"
        }

    ]


if "selected_product" not in st.session_state:

    st.session_state.selected_product = None


if "customer_active" not in st.session_state:

    st.session_state.customer_active = True


# ============================================================
# 9. FUNCTIONS
# ============================================================

def new_customer():

    st.session_state.bot = FashionChatbot()

    st.session_state.messages = [

        {
            "role": "assistant",

            "content":
                "👋 **New customer session started!**\n\n"
                "Welcome to UrbanWear. What can I help you explore?"
        }

    ]

    st.session_state.selected_product = None

    st.session_state.customer_active = True


def send_message(text):

    if not text or not text.strip():

        return

    text = text.strip()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": text
        }
    )

    response = st.session_state.bot.respond(text)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    detected = find_product(text)

    if detected:

        st.session_state.selected_product = detected

    if detect_intent(text) == "GOODBYE":

        st.session_state.customer_active = False


# ============================================================
# 10. HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="pill">
            ✦ AI-ASSISTED FASHION SUPPORT
        </div>

        <h1>
            UrbanWear Fashion Assistant
        </h1>

        <p>
            Your interactive style desk for products,
            prices, sizes, stock, delivery & support.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 11. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛍️ UrbanWear")

    st.caption(
        "Fashion support • Product discovery • Customer care"
    )

    if st.button(
        "✨ New Customer",
        use_container_width=True,
        type="primary"
    ):

        new_customer()

        st.rerun()

    st.divider()

    st.markdown("### ⚡ Quick Questions")

    quick_questions = [

        "Show me jeans",

        "What is the price of a t-shirt?",

        "What sizes are available?",

        "What is in stock?",

        "How long is delivery?",

        "What is your return policy?"

    ]

    for q in quick_questions:

        if st.button(
            q,
            key="quick_" + q,
            use_container_width=True
        ):

            send_message(q)

            st.rerun()

    st.divider()

    st.markdown("### 💡 Try asking")

    st.info(
        "“Do you have jeans in size 32?”\n\n"
        "“I need a t-shirt around ₹800.”\n\n"
        "“When will my order dispatch?”"
    )


# ============================================================
# 12. MAIN LAYOUT
# ============================================================

left, right = st.columns(
    [1.65, 1],
    gap="large"
)


# ============================================================
# 13. LEFT SIDE
# ============================================================

with left:

    st.markdown(
        '<div class="section-title">'
        '💬 Customer Support'
        '</div>',
        unsafe_allow_html=True
    )

    tabs = st.tabs(
        [
            "✨ Shop Products",
            "🤖 Chat Assistant"
        ]
    )

    # --------------------------------------------------------
    # SHOP PRODUCTS
    # --------------------------------------------------------

    with tabs[0]:

        st.markdown(
            "#### Explore the collection"
        )

        cols = st.columns(3)

        for i, (product, data) in enumerate(products.items()):

            with cols[i % 3]:

                st.image(
                    PRODUCT_IMAGES[product],
                    use_container_width=True
                )

                st.markdown(
                    f"""
                    <div class="product-card">

                        <h4>
                            {PRODUCT_EMOJI[product]}
                            {data['category']}
                        </h4>

                        <p>
                            <b>{data['brand']}</b>
                            • Sizes:
                            {', '.join(data['sizes'])}
                        </p>

                        <p class="price">
                            ₹{data['price_min']:,}
                            –
                            ₹{data['price_max']:,}
                        </p>

                        <p class="stock">
                            ● {data['stock']}
                            units currently in stock
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"Ask about {product.title()}",
                    key=f"product_{product}",
                    use_container_width=True
                ):

                    st.session_state.selected_product = product

                    send_message(
                        f"Tell me about {product}"
                    )

                    st.rerun()

    # --------------------------------------------------------
    # CHAT ASSISTANT
    # --------------------------------------------------------

    with tabs[1]:

        st.markdown(
            "#### Chat with your fashion assistant"
        )

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"],
                avatar=(
                    "🧑"
                    if message["role"] == "user"
                    else "🤖"
                )
            ):

                st.markdown(
                    message["content"]
                )

        if st.session_state.customer_active:

            prompt = st.chat_input(
                "Ask about products, sizes, prices, delivery, returns..."
            )

            if prompt:

                send_message(prompt)

                st.rerun()

        else:

            st.success(
                "Session completed. Start a new customer chat "
                "from the sidebar."
            )


# ============================================================
# 14. RIGHT SIDE
# ============================================================

with right:

    st.markdown(
        '<div class="section-title">'
        '👗 Store Snapshot'
        '</div>',
        unsafe_allow_html=True
    )

    total_products = len(products)

    total_stock = sum(
        item["stock"]
        for item in products.values()
    )

    m1, m2 = st.columns(2)

    m1.metric(
        "Collections",
        total_products
    )

    m2.metric(
        "Units in Stock",
        total_stock
    )

    st.markdown(
        "### 🔎 Current Product"
    )

    current = st.session_state.selected_product

    if current and current in products:

        data = products[current]

        st.image(
            PRODUCT_IMAGES[current],
            caption=(
                f"{data['category']} • "
                f"{data['brand']}"
            ),
            use_container_width=True
        )

        st.markdown(
            f"""
            <div class="info-box">

                <h3>
                    {PRODUCT_EMOJI[current]}
                    {current.title()}
                </h3>

                <p>
                    <b>Brand:</b>
                    {data['brand']}
                </p>

                <p>
                    <b>Price:</b>
                    ₹{data['price_min']:,}
                    –
                    ₹{data['price_max']:,}
                </p>

                <p>
                    <b>Sizes:</b>
                    {', '.join(data['sizes'])}
                </p>

                <p>
                    <b>Stock:</b>
                    {data['stock']} units
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="info-box">

                <h3>
                    🌟 Nothing selected yet
                </h3>

                <p>
                    Choose a product above or ask
                    the assistant about a product.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        "### 📦 Support Services"
    )

    services = [

        ("💰", "Price & Availability"),

        ("📏", "Size Assistance"),

        ("🚚", "Delivery & Dispatch"),

        ("📍", "Tracking Support"),

        ("↩️", "Returns & Exchanges"),

        ("🆘", "Order Issues")

    ]

    for icon, label in services:

        st.markdown(
            f"""
            <div class="product-card">

                <b>
                    {icon} {label}
                </b>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 15. FOOTER
# ============================================================

st.divider()

st.caption(
    "UrbanWear Fashion Assistant • "
    "Streamlit customer-support prototype • "
    "Powered by the student's rule-based conversational logic"
)
