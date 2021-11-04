Orders API
===

Functions realized:
---
> Get all users
>> `GET /users/`
> ```json
>    [{
>        "age": 31,
>        "email": "elliot16@mymail.com",
>        "first_name": "Hudson",
>        "id": 1,
>        "last_name": "Pauloh",
>        "phone": "6197021684",
>        "role": "customer"
>    },
>    {
>        "age": 41,
>        "email": "lawton46@mymail.com",
>        "first_name": "George",
>        "id": 2,
>        "last_name": "Matter",
>        "phone": "8314786677",
>        "role": "executor"
>    }]
>```

> Get a user by ID
>> `GET /users/id`
> ```json
>   {
>       "age": 20,
>       "email": "joshua18@mymail.com",
>       "first_name": "Lester",
>       "id": 5,
>       "last_name": "Archibaldoh",
>       "phone": "8825887253",
>       "role": "executor"
>   }
>```

> Add a user
>> `POST /users/`
> ```json
>   {
>       "age": 20,
>       "email": "joshua18@mymail.com",
>       "first_name": "Lester",
>       "last_name": "Archibaldoh",
>       "phone": "8825887253",
>       "role": "executor"
>   }
>``` 

> Update a user with ID
>> `PUT /users/id`
> ```json
>   {
>       "age": 20,
>       "email": "joshua18@mymail.com",
>       "first_name": "Lester",
>       "last_name": "Archibaldoh",
>       "phone": "8825887253",
>       "role": "executor"
>   }
>``` 

> Delete a user with ID
>> `DELETE /users/id`

> Get all orders
>> `GET /orders/`
> ```json
>   [{
>        "address": "4759 William Haven Apt. 194\nWest Corey, TX 43780",
>        "customer_id": 3,
>        "description": "Встретить тетю на вокзале с табличкой. Отвезти ее в магазин, помочь погрузить покупки. Привезти тетю домой, занести покупки и чемодан в квартиру",
>        "end_date": "03/28/2057",
>        "executor_id": 6,
>        "id": 0,
>        "name": "Встретить тетю на вокзале",
>        "price": 5512,
>        "start_date": "02/08/2013"
>    },
>    {
>        "address": "9387 Grimes Green Apt. 801\nPagetown, NM 44165",
>        "customer_id": 18,
>        "description": "Позвать в гости девушку и шикануть перед ней — заказать коробку конфет с доставкой на дом",
>        "end_date": "03/10/2076",
>        "executor_id": 25,
>        "id": 1,
>        "name": "Позвать в гости девушку",
>        "price": 2800,
>        "start_date": "01/24/2016"
>    }]
>```

> Get an order by ID
>> `GET /orders/id`
> ```json
>    {
>        "address": "9387 Grimes Green Apt. 801\nPagetown, NM 44165",
>        "customer_id": 18,
>        "description": "Позвать в гости девушку и шикануть перед ней — заказать коробку конфет с доставкой на дом",
>        "end_date": "03/10/2076",
>        "executor_id": 25,
>        "id": 1,
>        "name": "Позвать в гости девушку",
>        "price": 2800,
>        "start_date": "01/24/2016"
>    }
>```

> Add an order
>> `POST /orders/`
> ```json
>   {
>    "address": "75945 Jennifer Loaf\nPooleland, PA 25707",
>    "customer_id": 3,
>    "description": "Организовать переезд: упаковать вещи в коробки, погрузить, перевезти на машине, разгрузить и расставить всё по местам",
>    "end_date": "03/21/2006",
>    "executor_id": 18,
>    "name": "Организовать переезд: упаковать вещи",
>    "price": 491,
>    "start_date": "06/06/2011"
>   }
> ```

> Update an order with ID (you can change any field)
>> `PUT /orders/id`
> ```json
>   {
>    "address": "59179 Bruce Gardens Apt. 413\nLauramouth, AR 13687",
>    "customer_id": 6,
>    "description": "Сделать разом мелкий ремонт: повесить полочку в ванной, заклеить щели в окнах, починить выпадающую розетку, смазать дверные петли",
>    "end_date": "06/15/2037",
>    "executor_id": 28,
>    "name": "Сделать разом мелкий ремонт:",
>    "price": 7378,
>    "start_date": "09/22/2019"
>   }
> ```

> Delete an order by ID
>> `DELETE /orders/id`

> Get all offers
>> `GET /offers/`
> ```json
>   [{
>        "executor_id": 10,
>        "id": 0,
>        "order_id": 36
>    },
>    {
>        "executor_id": 4,
>        "id": 1,
>        "order_id": 35
>    }]
> ```   

> Get an offer by ID
>> `GET /offers/id`
> ```json
>   {
>    "executor_id": 7,
>    "id": 10,
>    "order_id": 20
>   }
> ```

> Add an offer with ID
>> `POST /offers/id`
> ```json
>   {
>    "executor_id": 8,
>    "id": 100,
>    "order_id": 18
>   }
> ```

> Update an offer with ID
>> `PUT /offers/id`
> ```json
>   {
>    "executor_id": 10,
>    "order_id": 20
>   }
> ```

> Delete an offer with ID
>> `DELETE /offers/id`

Dependencies
---
- Flask
- flask-sqlalchemy
- prettytable