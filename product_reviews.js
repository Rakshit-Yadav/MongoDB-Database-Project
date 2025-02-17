// this is for making an array called reviews which will
// store the information about ratings

// the code below is to show how to add reviews
db.products.update(
  { "_id": 1 },  // Replace with the actual product ID
  {
    $push: {
      "reviews": {
        $each: [
          { "rating": 4.5, "customer_id": ObjectId("customer_id_1") },
          { "rating": 3.8, "customer_id": ObjectId("customer_id_2") },
          { "rating": 5.0, "customer_id": ObjectId("customer_id_3") }
        ]
      }
    }
  }
)


// Step 1: Aggregate to calculate recommended products
const result = db.customers.aggregate([
  {
    $lookup: {
      from: "products",
      let: { pastOrders: "$past_orders", currentOrders: "$current_orders" },
      pipeline: [
        {
          $match: {
            $expr: {
              $not: {
                $in: ["$_id", { $concatArrays: ["$$pastOrders.product_id", "$$currentOrders.items.product_id"] }]
              }
            }
          }
        }
      ],
      as: "notBoughtProducts"
    }
  },
  {
    $unwind: "$notBoughtProducts"
  },
  {
    $sort: {
      "notBoughtProducts.avg_rating": -1
    }
  },
  {
    $limit: 5
  },
  {
    $group: {
      _id: "$_id",
      recommended_products: {
        $push: {
          product_name: "$notBoughtProducts.product_name",
          avg_rating: "$notBoughtProducts.avg_rating"
        }
      }
    }
  },
  {
    $project: {
      _id: 1,
      recommended_products: 1
    }
  }
]).toArray();

// Step 2: Extract data
const updates = result.map(({ _id, recommended_products }) => ({
  updateOne: {
    filter: { _id: _id },
    update: {
      $set: { recommended_products: recommended_products }
    }
  }
}));

// Step 3: Update customer documents
db.customers.bulkWrite(updates);
