# Application contract

checkout is called by an authenticated JSON route with its unfiltered body. Catalog returns an item with authoritative priceCents. Every item must be charged at its catalog price. payments charges exactly totalCents and fulfills without recalculation. No discount or pay-what-you-want feature exists.
