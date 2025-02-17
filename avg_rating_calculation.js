function calculateAndAddAvgRating() {
    try {
      db.products.aggregate([
        {
          $addFields: {
            avg_rating: {
              $avg: "$reviews.rating"
            }
          }
        },
        {
          $out: "products"
        }
      ]);
    } catch (error) {
        print('Error in calculating average ratings')
    }

}
  
