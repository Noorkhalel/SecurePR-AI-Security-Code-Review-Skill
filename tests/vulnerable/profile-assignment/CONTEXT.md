# Application contract

req.user.id comes from a verified session. db is unextended Prisma. User model has displayName, role and tenantId fields, all accepted by update. A user may change only displayName; request JSON is passed without schema filtering.
