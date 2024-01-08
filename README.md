# gDataBase 
## _User Management Service via gRPC_

This service has the task of creating, editing, deleting the user and fetching the user's information
Requests are sent from the grpc client side to the gDataBase service



## Features

- Create New User (Admin)
- Edit User Information
- Edit User Password
- Fetch User Data
- ✨ Change User Role (Admin) ✨


This repository is made of 2 separate services
1. postgres service
2. gRPC Host

The gRPC service receives requests from the client and sends them to the database

## How It Works


> 
> This service is completely dockerized and you need to set environment in it
> But before doing this, you need to create a network manually via docker so that in the
> future you can put all the services you need on an internal network of
> containers.

Create Network via docker:

```sh
docker network create share-net
```

Then set Environments in __docker-compose.yml__ .
| Environments | Value | Description |
| ------ | ------ | ------ |
| POSTGRES_DATABASE | test_db | _database name of postgres_ |
| POSTGRES_USERNAME | test_user | _username of postgres_ |
| POSTGRES_PASSWORD | test_pass | _postgres password for that database name_ |
| ADMIN_USERNAME | test_admin | _set default username for admin user_ |
| ADMIN_PASSWORD | test_admin_pass | set default password for admin user |
| POSTGRES_HOST | db | _postgres service host name_ |
| POSTGRES_PORT | 5432 | _postgres port_ |
| GRPC_PORT | 3333 | _gRPC port_ |
> Note: POSTGRES_HOST is available in docker-compose.yml (**db service**)

In Finally
```sh
docker compose up
```

Now You can access to gRPC Host in docker internal network 
```sh
[::]:3333
```

## Architecture

![Architecture](https://github.com/amir-wyvern/database-user-management/blob/main/pic.png)


## License

MIT

**Free Software, Hell Yeah!**

