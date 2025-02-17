# Get the product IDs for "fresh" category from the products collection
fresh_category_products_id = db.products.distinct("_id", {"category": "fresh"})

# Get the product IDs for "other" category from the products collection
other_category_products_id = db.products.distinct("_id", {"category": "other"})

def generate_product_quantity_plot(date):
    # Aggregation pipeline for fresh category products in stores
    fresh_inventory_pipeline = [
        {
            "$match": {
                "location.type": "Point",  # Assuming this field exists to distinguish stores from other locations
                "available_groceries.product_id": {"$in": fresh_category_products_id}
            }
        },
        {
            "$unwind": "$available_groceries"
        },
        {
            "$match": {
                "available_groceries.product_id": {"$in": fresh_category_products_id}
            }
        },
        {
            "$group": {
                "_id": "$available_groceries.product_id",
                "total_quantity": {"$sum": "$available_groceries.quantity"}
            }
        },
        {
            "$sort": {"total_quantity": -1}
        },
    ]

    # Aggregation pipeline for other category products in daily_inventory_levels
    other_inventory_pipeline = [
        {
            "$match": {
                "date": date,
                "storage_warehouses.products.product_id": {"$in": other_category_products_id}
            }   
        },
        {
            "$unwind": "$storage_warehouses"
        },
        {
            "$unwind": "$storage_warehouses.products"
        },
        {
            "$match": {
                "storage_warehouses.products.product_id": {"$in": other_category_products_id}
            }
        },
        {
            "$group": {
                "_id": "$storage_warehouses.products.product_id",
                "total_quantity": {"$sum": "$storage_warehouses.products.quantity"}
            }
        },
        {
            "$sort": {"total_quantity": -1}
        },
    ]

    # Execute the fresh inventory aggregation
    fresh_inventory_result = db.stores.aggregate(fresh_inventory_pipeline)

    # Execute the other inventory aggregation
    other_inventory_result = db.daily_inventory_levels.aggregate(other_inventory_pipeline)

    # Extract data for plotting - Fresh category
    fresh_inventory_data = [{"product_id": entry["_id"], "total_quantity": entry["total_quantity"]} for entry in fresh_inventory_result]

    # Extract data for plotting - Other category
    other_inventory_data = [{"product_id": entry["_id"], "total_quantity": entry["total_quantity"]} for entry in other_inventory_result]

    # Sorting fresh inventory data based on total_quantity
    fresh_inventory_data = sorted(fresh_inventory_data, key=lambda x: x["total_quantity"], reverse=True)

    # Sorting other inventory data based on total_quantity
    other_inventory_data = sorted(other_inventory_data, key=lambda x: x["total_quantity"], reverse=True)

    # Aggregation pipeline for fresh category products in current orders
    fresh_orders_pipeline = [
        {
            "$match": {
                "current_orders.date": date,
                "current_orders.items.product_id": {"$in": fresh_category_products_id}
            }
        },
        {
            "$unwind": "$current_orders"
        },
        {
            "$unwind": "$current_orders.items"
        },
        {
            "$match": {
                "current_orders.items.product_id": {"$in": fresh_category_products_id}
            }
        },
        {
            "$group": {
                "_id": "$current_orders.items.product_id",
                "total_quantity": {"$sum": "$current_orders.items.quantity"}
            }
        },
        {
            "$sort": {"total_quantity": -1}
        },
    ]

    # Aggregation pipeline for other category products in current orders
    other_orders_pipeline = [
        {
            "$match": {
                "current_orders.date": date,
                "current_orders.items.product_id": {"$in": other_category_products_id}
            }
        },
        {
            "$unwind": "$current_orders"
        },
        {
            "$unwind": "$current_orders.items"
        },
        {
            "$match": {
                "current_orders.items.product_id": {"$in": other_category_products_id}
            }
        },
        {
            "$group": {
                "_id": "$current_orders.items.product_id",
                "total_quantity": {"$sum": "$current_orders.items.quantity"}
            }
        },
        {
            "$sort": {"total_quantity": -1}
        },
    ]

    # Execute the fresh orders aggregation
    fresh_orders_result = db.customers.aggregate(fresh_orders_pipeline)

    # Execute the other orders aggregation
    other_orders_result = db.customers.aggregate(other_orders_pipeline)

    # Extract data for plotting - Fresh category
    fresh_orders_data = [{"product_id": entry["_id"], "total_quantity": entry["total_quantity"]} for entry in fresh_orders_result]

    # Extract data for plotting - Other category
    other_orders_data = [{"product_id": entry["_id"], "total_quantity": entry["total_quantity"]} for entry in other_orders_result]

    # Sorting fresh orders data based on total_quantity
    fresh_orders_data = sorted(fresh_orders_data, key=lambda x: x["total_quantity"], reverse=True)

    # Sorting other orders data based on total_quantity
    other_orders_data = sorted(other_orders_data, key=lambda x: x["total_quantity"], reverse=True)

    # Plotting for Fresh Category
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))

    # Fresh Category Plots
    bar1 = axes[0].bar(range(len(fresh_orders_data)), [entry["total_quantity"] for entry in fresh_orders_data], color='red', alpha=0.7)
    axes[0].set_title(f'Fresh Products - Current Orders Performance on  Date:({date})')
    axes[0].set_ylabel('Total Quantity')

    # Add integer labels on top of the bars
    for rect in bar1:
        height = rect.get_height()
        axes[0].annotate(f'{int(height)}', xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), 
                         textcoords="offset points", ha='center', va='bottom')

    # Adjusting X-axis labels for the bottom plot
    axes[0].set_xticks(range(len(fresh_orders_data)))
    axes[0].set_xticklabels([entry["product_id"] for entry in fresh_orders_data], rotation=45, ha='right', rotation_mode='anchor')

    bar2 = axes[1].bar(range(len(fresh_inventory_data)), [entry["total_quantity"] for entry in fresh_inventory_data], color='blue', alpha=0.7)
    axes[1].set_title(f'Fresh Products - Inventory Levels on  Date:({date})')
    axes[1].set_xlabel('Product ID')
    axes[1].set_ylabel('Total Quantity')

    # Add integer labels on top of the bars
    for rect in bar2:
        height = rect.get_height()
        axes[1].annotate(f'{int(height)}', xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), 
                         textcoords="offset points", ha='center', va='bottom')

    # Adjusting X-axis labels for the bottom plot
    axes[1].set_xticks(range(len(fresh_inventory_data)))
    axes[1].set_xticklabels([entry["product_id"] for entry in fresh_inventory_data], rotation=45, ha='right', rotation_mode='anchor')

    plt.tight_layout()
    plt.show()

    # Plotting for Other Category
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))

    # Other Category Plots
    bar3 = axes[0].bar(range(len(other_orders_data)), [entry["total_quantity"] for entry in other_orders_data], color='red', alpha=0.7)
    axes[0].set_title(f'Other Category Products - Current Orders Performance on Date:({date})')
    axes[0].set_ylabel('Total Quantity')

    # Add integer labels on top of the bars
    for rect in bar3:
        height = rect.get_height()
        axes[0].annotate(f'{int(height)}', xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), 
                         textcoords="offset points", ha='center', va='bottom')

    # Adjusting X-axis labels for the bottom plot
    axes[0].set_xticks(range(len(other_orders_data)))
    axes[0].set_xticklabels([entry["product_id"] for entry in other_orders_data], rotation=45, ha='right', rotation_mode='anchor')

    bar4 = axes[1].bar(range(len(other_inventory_data)), [entry["total_quantity"] for entry in other_inventory_data], color='blue', alpha=0.7)
    axes[1].set_title(f'Other Category Products - Inventory Levels for  Date:({date})')
    axes[1].set_xlabel('Product ID')
    axes[1].set_ylabel('Total Quantity')

    # Add integer labels on top of the bars
    for rect in bar4:
        height = rect.get_height()
        axes[1].annotate(f'{int(height)}', xy=(rect.get_x() + rect.get_width() / 2, height), xytext=(0, 3), 
                         textcoords="offset points", ha='center', va='bottom')

    # Adjusting X-axis labels for the bottom plot
    axes[1].set_xticks(range(len(other_inventory_data)))
    axes[1].set_xticklabels([entry["product_id"] for entry in other_inventory_data], rotation=45, ha='right', rotation_mode='anchor')

    plt.tight_layout()
    plt.show()

# Example usage
date = datetime(2023, 12, 5)  # Change this date as needed
generate_product_quantity_plot(date)
