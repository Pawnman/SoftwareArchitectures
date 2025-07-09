# Программная инженерия (Software Architecture)

Курсовой проект, представляющий из себя клиент-серверное приложение "Мессенджер" на основании 6-ти лабораторных работ.

## Выполнил учащийся группы М80-109М-23:

    Пешков Максим Юрьевич

## Вариант 5 - Мессенджер

Приложение должно содержать следующие данные:

- Пользователь
- Групповой чат
- Person to Person (PtP) чат
  
Реализовать API:
- Создание нового пользователя
- Поиск пользователя по логину
- Поиск пользователя по маске имя и фамилии
- Создание группового чата
- Добавление пользователя в чат
- Добавление сообщения в групповой чат
- Загрузка сообщений группового чата
- Отправка PtP сообщения пользователю
- Получение PtP списка сообщений для пользователя

# Messenger Microservice Application

## Project Overview
This project involves the development of a **microservice application** for a messaging platform that supports user accounts, group chats, and point-to-point (PtP) messaging. The system is designed with a robust **REST API** for operations such as user creation, user search by login or name, creation of group chats, adding users to chats, and sending/receiving messages. The application integrates both **PostgreSQL** and **MongoDB** databases to store data, and it includes JWT-based authentication and Redis-based caching to enhance performance.

## Business Goal
The goal of this project is to provide a scalable and secure messaging platform that supports both group and PtP messaging. By integrating **authentication**, **message storage**, **caching**, and **microservice architecture**, the platform enables efficient and secure communication for users while offering high availability and performance.

## Tech Stack
- **Backend Framework**:
  - **FastAPI**: For building the REST API services (for user management, messaging, etc.).
  - **PostgreSQL**: For relational data storage, used to store user data and manage group chat data.
  - **MongoDB**: For storing unstructured data (like messages) with scalability.
  - **Redis**: For caching user data to reduce the load on databases and improve response time.
  - **JWT**: For implementing secure authentication via **JSON Web Tokens**.
  - **Docker**: For containerizing the application and simplifying deployment.
  
- **Authentication**:
  - **JWT**: Used for authenticating requests, ensuring secure and authorized access to the application.
  - **Basic Authentication**: The application utilizes basic authentication at the `/auth` endpoint to generate JWT tokens.
  
- **API Gateway**:
  - **API Gateway**: A centralized service that handles routing, authentication, and communication between microservices.
  - **Circuit Breaker**: Implemented to ensure the system remains resilient in case of service failures.

## Key Features
- **User Management**:
  - Create new users and authenticate using JWT tokens.
  - Search users by login, name, or surname using RESTful APIs.
  
- **Messaging Services**:
  - Create and manage group chats.
  - Send and receive messages in group chats and PtP (point-to-point) chats.
  - Use **MongoDB** for efficient storage and retrieval of messages.
  
- **Caching**:
  - Implement **Redis** caching for frequently accessed user data with an expiration time.
  - Comparison of response times and throughput with and without caching using **wrk** (a benchmarking tool).
  
- **Microservices Architecture**:
  - Each component of the application is a microservice (user service, messaging service, chat service) that can scale independently.
  
- **API Gateway**:
  - Central entry point for client requests, managing communication with different services.
  - Implements **Circuit Breaker** for service reliability.

## Architecture
1. **User Service**:
   - Handles user creation, authentication, and searching via REST API.
   - Implements JWT authentication.
   
2. **Chat Service**:
   - Manages group chat and PtP chat creation, sending messages, and retrieving messages.
   - Stores messages in **MongoDB**.
   
3. **API Gateway**:
   - Routes requests to the appropriate services.
   - Implements **Circuit Breaker** for service reliability.
   
4. **Caching Layer**:
   - **Redis** cache stores user data and other frequently queried information.

## Project Development Steps
1. **Database Design**:
   - Designed **PostgreSQL** schema for user data and **MongoDB** collections for messages.
   - Implemented data models for users, messages, and chat groups.
   
2. **API Design**:
   - Developed **REST API** endpoints for CRUD operations on users and messages.
   - Specified API using **OpenAPI 3.0** and saved the specification in **index.yaml**.
   
3. **JWT Authentication**:
   - Implemented authentication for accessing services with **JWT** tokens.
   - Created an `/auth` endpoint to authenticate users via basic credentials and issue a JWT token.

4. **Caching Implementation**:
   - Configured **Redis** for caching user data and improved response times.
   - Used **wrk** to benchmark performance with and without caching.
   
5. **Microservices Integration**:
   - Developed microservices for user management, messaging, and chat functionalities.
   - Integrated **API Gateway** for centralized request handling and routing.

6. **Dockerization**:
   - Created a **Dockerfile** for each service to enable easy deployment.
   - Tested the services locally and in Docker containers for reliability.

7. **Performance Testing**:
   - Used **wrk** for load testing and comparing the system's performance with and without caching.
   - Documented performance results in **performance.md**.

8. **Deployment**:
   - Pushed the code to **GitHub** and ensured proper versioning.

## Example API Endpoints:
- **POST /auth**: Authenticates a user and issues a JWT token.
- **POST /users**: Creates a new user.
- **GET /users/{login}**: Retrieves a user by login.
- **POST /chats/group**: Creates a new group chat.
- **POST /messages**: Sends a new message to a group chat or PtP chat.
- **GET /messages**: Retrieves messages from a chat.

## Docker Commands:
- **Build Docker Image**:
  ```bash
  docker build -t messenger_service .


# Архитектура приложения

<p></p>
<figure>
   <img src="./lab_01/images/Context.png" width="400"/>
   <figcaption>Рисунок 1 - Контекстная схема приложения</figcaption>
  </figure>
<p></p>

<p></p>
<figure>
   <img src="./lab_01/images/Deployment.png" width="400"/>
   <figcaption>Рисунок 2 - Структура развертки приложения</figcaption>
  </figure>
<p></p>
