from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
# IP = env.str("ip")  # Xosting ip manzili
X_API_KEY = env.str("X_API_KEY")
DOMAIN = env.str("DOMAIN")
headers = {
    'X-API-KEY': X_API_KEY
}