# Application contract

requireSession verifies a session and sets req.user={id,tenantId,role}; it only authenticates. db is an ordinary Prisma client with no extensions or row security. Invoices are private to ownerId. Users can know invoice IDs belonging to others.
