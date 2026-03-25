# Shopping Cart Program

shopping_cart = []

def add_item(item):
    """Add an item to the shopping cart"""
    shopping_cart.append(item)
    print(f"'{item}' added to cart")

def remove_item(item):
    """Remove one instance of an item from the cart"""
    if item in shopping_cart:
        shopping_cart.remove(item)
        print(f"'{item}' removed from cart")
    else:
        print(f"'{item}' is not in the cart")

def print_total_items():
    """Print the total number of items in the cart"""
    total = len(shopping_cart)
    print(f"Total items in cart: {total}")

def display_cart():
    """Display all items in the cart"""
    if not shopping_cart:
        print("Cart is empty")
    else:
        print("\n--- Shopping Cart ---")
        for i, item in enumerate(shopping_cart, 1):
            print(f"{i}. {item}")
        print("--------------------")

# Example usage
if __name__ == "__main__":
    # Add items
    add_item("Apple")
    add_item("Banana")
    add_item("Milk")
    add_item("Bread")
    add_item("Apple")  # Adding duplicate
    
    # Display cart
    display_cart()
    
    # Print total items
    print_total_items()
    
    # Remove an item
    print("\nRemoving Apple...")
    remove_item("Apple")
    
    # Display updated cart
    display_cart()
    
    # Print updated total
    print_total_items()
    
    # Try removing an item that doesn't exist
    print("\nTrying to remove Orange...")
    remove_item("Orange")
