<h1 align="center">Password Manager</h1>

<p align="center">
  Password Manager — это простое веб-приложение для управления паролями, построенное на Django и Docker. Оно позволяет пользователям безопасно хранить и управлять своими учетными данными для различных сервисов.
</p>

<h2>Основные функции</h2>
<ul>
  <li><strong>Регистрация и аутентификация пользователей</strong>: Пользователи могут регистрироваться, входить в систему и выходить из нее.</li>
  <li><strong>Хранение паролей</strong>: Пользователи могут добавлять, редактировать и удалять учетные записи для различных сервисов.</li>
  <li><strong>Шифрование паролей</strong>: Пароли шифруются с использованием Fernet (библиотека <code>cryptography</code>).</li>
  <li><strong>Декодирование паролей</strong>: Пользователи могут получить расшифрованный пароль, используя мастер-пароль.</li>
  <li><strong>API документация</strong>: Используется <code>drf-spectacular</code> для автоматической генерации документации API.</li>
</ul>

<h2>Технологии</h2>
<ul>
  <li><strong>Backend</strong>: Django, Django REST Framework (DRF)</li>
  <li><strong>База данных</strong>: PostgreSQL</li>
  <li><strong>Шифрование</strong>: Fernet (библиотека <code>cryptography</code>)</li>
  <li><strong>Документация API</strong>: drf-spectacular</li>
  <li><strong>Контейнеризация</strong>: Docker, Docker Compose</li>
</ul>

<h2>Установка и запуск</h2>

<h3>Предварительные требования</h3>
<ul>
  <li>Установите <a href="https://docs.docker.com/get-docker/">Docker</a> и <a href="https://docs.docker.com/compose/install/">Docker Compose</a>.</li>
</ul>

<h3>Шаги для запуска</h3>
<ol>
  <li>
    <strong>Клонируйте репозиторий</strong>:
    <pre><code>git clone https://github.com/Afonderkin/PasswordManager
cd PasswordManager</code></pre>
  </li>
  <li>
    <strong>Создайте файл <code>.env</code></strong>:
    Отредактируйте файл <code>.env</code>, указав необходимые значения (например, <code>SECRET_KEY</code>, <code>POSTGRES_DB</code>, <code>POSTGRES_USER</code>, <code>POSTGRES_PASSWORD</code>, <code>FERNET_KEY</code> и т.д.).
  </li>
  <li>
    <strong>Запустите проект с помощью Docker Compose</strong>:
    <pre><code>./run.sh up</code></pre>
    Этот скрипт соберет и запустит контейнеры для базы данных и Django-приложения.
  </li>
  <li>
    <strong>Примените миграции</strong>:
    После запуска контейнеров примените миграции:
    <pre><code>./run.sh migrate</code></pre>
  </li>
  <li>
    <strong>Создайте суперпользователя (опционально)</strong>:
    Если вам нужен доступ к админке Django, создайте суперпользователя:
    <pre><code>./run.sh createsuperuser</code></pre>
  </li>
  <li>
    <strong>Документация API</strong>:
    После запуска проекта документация API будет доступна по адресу:
    <ul>
      <li>Swagger UI: <a href="http://localhost:8000/api/swagger/">http://localhost:8000/api/swagger/</a></li>
      <li>ReDoc: <a href="http://localhost:8000/api/redoc/">http://localhost:8000/api/redoc/</a></li>
    </ul>
  </li>
</ol>

<h3>Остановка проекта</h3>
<p>Чтобы остановить проект, выполните:</p>
<pre><code>./run.sh down</code></pre>

<h2>Структура проекта</h2>
<ul>
  <li><strong>docker-composes/</strong>: Конфигурационные файлы Docker Compose для базы данных и приложения.</li>
  <li><strong>password-manager/</strong>: Основной проект Django.
    <ul>
      <li><strong>accounts/</strong>: Приложение для управления учетными записями и паролями.</li>
      <li><strong>users/</strong>: Приложение для управления пользователями (регистрация, аутентификация).</li>
    </ul>
  </li>
  <li><strong>Dockerfile</strong>: Файл для сборки Docker-образа приложения.</li>
  <li><strong>.env</strong>: Файл с переменными окружения.</li>
  <li><strong>requirements.txt</strong>: Зависимости Python.</li>
  <li><strong>run.sh</strong>: Скрипт для управления контейнерами (запуск, остановка, миграции и т.д.).</li>
</ul>

<h2>Использование API</h2>

<h3>Регистрация пользователя</h3>
<p><strong>Запрос</strong>:</p>
<pre><code>POST /api/register/</code></pre>
<p><strong>Тело запроса</strong>:</p>
<pre><code>{
  "username": "ваш_username",
  "password": "ваш_password"
}</code></pre>

<h3>Вход в систему</h3>
<p><strong>Запрос</strong>:</p>
<pre><code>POST /api/login/</code></pre>
<p><strong>Тело запроса</strong>:</p>
<pre><code>{
  "username": "ваш_username",
  "password": "ваш_password"
}</code></pre>

<h3>Добавление учетной записи</h3>
<p><strong>Запрос</strong>:</p>
<pre><code>POST /api/accounts/</code></pre>
<p><strong>Тело запроса</strong>:</p>
<pre><code>{
  "email": "example@example.com",
  "service_name": "Example Service",
  "password": "your_password"
}</code></pre>

<h3>Получение расшифрованного пароля</h3>
<p><strong>Запрос</strong>:</p>
<pre><code>POST /api/accounts/&lt;id&gt;/decrypt-password/</code></pre>
<p><strong>Тело запроса</strong>:</p>
<pre><code>{
  "master_password": "ваш_мастер_пароль"
}</code></pre>