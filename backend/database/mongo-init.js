
db = db.getSiblingDB("admin")

db.createUser({
    user: process.env.DB_ADMIN_USER,
    pwd: process.env.DB_ADMIN_PASSWORD,
    roles: [
        {
            role: "userAdminAnyDatabase",
            db: "admin"
        },
        "readWriteAnyDatabase"
    ]
})

db = db.getSiblingDB(process.env.DB_DATABASE)

db.createCollection("backends")

db.backends.createIndex({
    backend_name: "text"
})

db.createCollection("users")

db.users.insertMany([
    {
        first_name: "TFG Admin Account",
        email: 'admin@test.com',
        password: '$2b$12$17fAsjT3G78K5VKhpHCMX./KaXMPanMXdMyD87W5GA5p2FEcJ4ymu',
        roles: [ 'Admin' ],
        api_keys: {},
        is_verified: true,
    },
    {
        // dummy-account
        username: "dummy-account",
        email: process.env.DB_DUMMY_ACCOUNT,
		password: '$2b$12$.qe2WQYlLi20DXsUX3GIY.QwWyYJiIyEDFvORjsi7tQLUn9m/Isc2',
        roles: ["User"],
        api_keys: {},
        is_verified: true,
    }
])
