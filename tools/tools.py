"""Tutorial sales tools using fictional data and process-local memory.

Production code should get customer identity from an authenticated session
and use a payment provider for checkout.
"""

from copy import deepcopy

from content.product import CURRENCY, PRODUCTS, PRODUCT_GROUPS
from tools.tool_definitions import TOOL_DEFINITIONS

# The application supplies this demo customer; the model cannot choose an account.
CUSTOMER = {"name": "Alex", "preferences": ""}
ORDERS = [{"order_id": "demo-001", "product_id": "nova-phone-x6", "quantity": 1,
           "status": "delivered"}]


def get_products() -> dict:
    """Return the complete electronics catalog, including specifications."""
    return {"currency": CURRENCY, "products": deepcopy(PRODUCTS)}


def search_products(
    category: str = "",
    max_price_cents: int = 0,
    color: str = "",
    use_case: str = "",
) -> dict:
    """Search products by category, budget, color, or intended use.

    Args:
        category: Category or subcategory, such as computers, laptops, or audio.
        max_price_cents: Maximum price in EUR cents. Use 0 for no price limit.
        color: Desired color. Leave empty when color does not matter.
        use_case: Intended use, such as travel, gaming, office, or photography.
    """
    if type(max_price_cents) is not int or max_price_cents < 0:
        return {"error": "max_price_cents must be a nonnegative integer."}

    category = category.strip().lower()
    color = color.strip().lower()
    use_case = use_case.strip().lower()
    matches = {}

    for product_id, product in PRODUCTS.items():
        searchable_uses = product["use_cases"] + product["tags"]
        if category and category not in {
            product["category"].lower(), product["subcategory"].lower()
        }:
            continue
        if max_price_cents and product["price_cents"] > max_price_cents:
            continue
        if color and color not in (item.lower() for item in product["colors"]):
            continue
        if use_case and not any(use_case in item.lower() for item in searchable_uses):
            continue
        if product["stock"] > 0:
            matches[product_id] = deepcopy(product)

    return {"currency": CURRENCY, "count": len(matches), "products": matches}


def get_product(product_id: str) -> dict:
    """Return full details for one product using its exact catalog ID."""
    product = PRODUCTS.get(product_id)
    if product is None:
        return {"error": "Unknown product ID. Use search_products first."}
    return {"product_id": product_id, "currency": CURRENCY, **deepcopy(product)}


def get_product_group(group_name: str) -> dict:
    """Return a curated product group such as work_from_home or mobile_travel."""
    product_ids = PRODUCT_GROUPS.get(group_name)
    if product_ids is None:
        return {"error": f"Unknown group. Available groups: {list(PRODUCT_GROUPS)}"}
    return {
        "group": group_name,
        "currency": CURRENCY,
        "products": {product_id: deepcopy(PRODUCTS[product_id]) for product_id in product_ids},
    }


def get_customer() -> dict:
    """Return the current demo customer's name and saved preferences."""
    return deepcopy(CUSTOMER)


def remember_preferences(preferences: str) -> dict:
    """Save preferences explicitly shared by the customer for this process only."""
    if not preferences.strip():
        return {"error": "Please provide a nonempty preference."}
    CUSTOMER["preferences"] = preferences.strip()
    return get_customer()


def get_order_history() -> dict:
    """Return the current demo customer's previous orders."""
    return {"orders": deepcopy(ORDERS)}


def recommend_products(max_budget_cents: int, use_case: str = "") -> dict:
    """Find in-stock products within a budget, excluding previously bought items.

    The agent can use descriptions and saved preferences to explain its choice.
    """
    if type(max_budget_cents) is not int or max_budget_cents < 0:
        return {"error": "Budget must be a nonnegative integer in EUR cents."}
    purchased = {order["product_id"] for order in ORDERS}
    use_case = use_case.strip().lower()
    return {"currency": CURRENCY, "products": {
        product_id: deepcopy(product)
        for product_id, product in PRODUCTS.items()
        if product["price_cents"] <= max_budget_cents
        and product_id not in purchased
        and product["stock"] > 0
        and (not use_case or any(
            use_case in item.lower() for item in product["use_cases"] + product["tags"]
        ))
    }}


def create_demo_checkout(product_id: str, quantity: int) -> dict:
    """Simulate checkout without collecting card details or charging money."""
    if product_id not in PRODUCTS:
        return {"error": "Unknown product ID. Use get_products to see the catalog."}
    if type(quantity) is not int or not 1 <= quantity <= 10:
        return {"error": "Quantity must be an integer between 1 and 10."}
    return {
        "product_id": product_id,
        "quantity": quantity,
        "total_cents": PRODUCTS[product_id]["price_cents"] * quantity,
        "currency": CURRENCY,
        "status": "simulation_only",
        "message": "No payment was charged and no order was placed.",
    }


LLM_TOOLS = [
    search_products,
    get_product,
    get_product_group,
    get_customer,
    remember_preferences,
    get_order_history,
    recommend_products,
    create_demo_checkout,
]

AVAILABLE_FUNCTIONS = {function.__name__: function for function in LLM_TOOLS}

ALL_TOOLS = [
    {"name": function.__name__, "function": function} for function in LLM_TOOLS
]
