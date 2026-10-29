"""Function schemas passed to the Gemini Interactions API."""


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "name": "search_products",
        "description": "Search in-stock electronics by category, price, color, and intended use.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Category or subcategory, such as phones, laptops, or audio."},
                "max_price_cents": {"type": "integer", "minimum": 0, "description": "Maximum price in EUR cents. Use 0 for no limit."},
                "color": {"type": "string", "description": "Requested color, or an empty string when unspecified."},
                "use_case": {"type": "string", "description": "Intended use, such as travel, gaming, office, or photography."},
            },
        },
    },
    {
        "type": "function",
        "name": "get_product",
        "description": "Get specifications, variants, price, rating, and stock for one product.",
        "parameters": {
            "type": "object",
            "properties": {"product_id": {"type": "string", "description": "Exact ID returned by search_products."}},
            "required": ["product_id"],
        },
    },
    {
        "type": "function",
        "name": "get_product_group",
        "description": "Get a curated product group for a common shopping scenario.",
        "parameters": {
            "type": "object",
            "properties": {
                "group_name": {
                    "type": "string",
                    "enum": ["work_from_home", "mobile_travel", "creator_setup", "smart_home"],
                    "description": "Name of the curated product group.",
                }
            },
            "required": ["group_name"],
        },
    },
    {
        "type": "function",
        "name": "get_customer",
        "description": "Get the current customer's name and saved preferences.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "remember_preferences",
        "description": "Save product preferences explicitly shared by the customer.",
        "parameters": {
            "type": "object",
            "properties": {"preferences": {"type": "string", "description": "Summary of the customer's stated preferences."}},
            "required": ["preferences"],
        },
    },
    {
        "type": "function",
        "name": "get_order_history",
        "description": "Get previous orders for the current customer.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "recommend_products",
        "description": "Find in-stock products within a budget and intended use, excluding previous purchases.",
        "parameters": {
            "type": "object",
            "properties": {
                "max_budget_cents": {"type": "integer", "minimum": 0, "description": "Maximum budget in EUR cents."},
                "use_case": {"type": "string", "description": "Optional use such as travel, gaming, or office."},
            },
            "required": ["max_budget_cents"],
        },
    },
    {
        "type": "function",
        "name": "create_demo_checkout",
        "description": "Create a simulated quote without charging money or placing an order.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "Exact catalog product ID."},
                "quantity": {"type": "integer", "minimum": 1, "maximum": 10, "description": "Number of units."},
            },
            "required": ["product_id", "quantity"],
        },
    },
]
