import time


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = password
        self.age = age

    def __str__(self):
        return f'User: {self.nickname}, Password: {self.password}, Age: {self.age}'


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def register(self, nickname, password, age):
        for user in self.users:
            if nickname == user.nickname:
                print(f"Пользователь {nickname} уже существует")
                return
        self.users.append(User(nickname, hash(password), age))
        self.current_user = self.users[-1]  # автоматический вход

    def log_in(self, nickname, password):
        if self.current_user is None:
            for user in self.users:
                if user.nickname == nickname and hash(password) == user.password:
                    self.current_user = user
                    print('Вы успешно авторизовались!')
                    return
            print('Неверный логин или пароль')
            return
        print('Вы уже авторизованы!')

    def log_out(self):
        if self.current_user is None:
            print('Вы не вошли в аккаунт!')
            return
        self.current_user = None

    def add(self, *videos_list):
        for video in videos_list:
            if video.title not in [v.title for v in self.videos]:
                self.videos.append(video)

    def get_videos(self, search_w):
        res = []
        for video in self.videos:
            if search_w.lower() in video.title.lower():
                res.append(video.title)
        return res

    def watch_video(self, title):
        if self.current_user is None:
            print('Войдите в аккаунт, чтобы смотреть видео')
            return
        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print('Вам нет 18 лет, пожалуйста покиньте страницу')
                    return
                print('Воспроизведение: ', end=' ')
                for sec in range(video.duration):
                    print(sec, end=' ')
                    time.sleep(1)
                print('Конец видео.')
                return
        print('Видео не найдено!')


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
