# University API System


The university API system can be authenticated using jwt bearer token and monitored as swagger. It includes mobile, banking, admin, authentication and models.

## Features

- **Flask**: Python's framework which we used for this project.
- **Authentication**: Users can authenticate using JWT bearer token.
- **Swagger Documentation**: API endpoints can be monitored using Swagger.
- **Mobile Integration**: Integration with mobile applications for accessing university services.
- **Banking Integration**: Integration with banking systems for student fee payments.
- **Admin Panel**: Administrative panel for managing users, roles, and permissions.
- **Models**: Data models for storing information about students, tuition_total, and faculty balance.
- **Sqlite**: Database for storing information about students, tuition_total, and faculty balance.

## Operations 

### Mobil

- [ ] `GET`: /Mobil/query-tuition

### Banking

- [ ] `POST`: /Banking/pay-tuition
- [ ] `GET`: /Banking/query-tuition

### Admin

- [ ] `POST`: /Admin/add-tuition
- [ ] `GET`: /Admin/unpaid-tuition-status

### Authentication

- [ ] `POST`: /Authentication/login
