import unittest

class Runner:
    def __init__(self, name, distance=0):
        self.name = name
        self.distance = distance

    def run(self):
        self.distance += 10

    def walk(self):
        self.distance += 5

    def __str__(self):
        return self.name

class RunnerTest(unittest.TestCase):
    is_frozen = False

    @unittest.skipIf(False, 'Тесты в этом кейсе заморожены')
    def test_walk(self):
        runner = Runner('TestRunner')
        for _ in range(10):
            runner.walk()
        self.assertEqual(runner.distance, 50)

    @unittest.skipIf(False, 'Тесты в этом кейсе заморожены')
    def test_run(self):
        runner = Runner('TestRunner')
        for _ in range(10):
            runner.run()
        self.assertEqual(runner.distance, 100)

    @unittest.skipIf(False, 'Тесты в этом кейсе заморожены')
    def test_challenge(self):
        runner1 = Runner('Runner1')
        runner2 = Runner('Runner2')
        for _ in range(10):
            runner1.run()
            runner2.walk()
        self.assertNotEqual(runner1.distance, runner2.distance)


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in list(self.participants):
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers


class TournamentTest(unittest.TestCase):
    is_frozen = True

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    @unittest.skipIf(True, 'Тесты в этом кейсе заморожены')
    def setUp(self):
        self.runner_usain = Runner("Усэйн", 10)
        self.runner_andrey = Runner("Андрей", 9)
        self.runner_nick = Runner("Ник", 3)

    @classmethod
    def tearDownClass(self):
        for result in self.all_results.values():
            result_print = {place: str(runner) for place, runner in result.items()}
            print(result_print)

    @unittest.skipIf(True, 'Тесты в этом кейсе заморожены')
    def test_race_usain_nick(self):
        tournament = Tournament(90, self.runner_usain, self.runner_nick)
        result = tournament.start()
        self.__class__.all_results[1] = result
        last_runner = max(result, key=lambda x: x)
        first_runner = min(result, key=lambda x: x)
        self.assertTrue(str(result[first_runner]) == "Усэйн")
        self.assertTrue(str(result[last_runner]) == "Ник")

    @unittest.skipIf(True, 'Тесты в этом кейсе заморожены')
    def test_race_andrey_nick(self):
        tournament = Tournament(90, self.runner_andrey, self.runner_nick)
        result = tournament.start()
        self.__class__.all_results[2] = result
        last_runner = max(result, key=lambda x: x)
        first_runner = min(result, key=lambda x: x)
        self.assertTrue(str(result[first_runner]) == "Андрей")
        self.assertTrue(str(result[last_runner]) == "Ник")

    @unittest.skipIf(True, 'Тесты в этом кейсе заморожены')
    def test_race_usain_andrey_nick(self):
        tournament = Tournament(90, self.runner_usain, self.runner_andrey, self.runner_nick)
        result = tournament.start()
        self.__class__.all_results[3] = result
        last_runner = max(result, key=lambda x: x)
        first_runner = min(result, key=lambda x: x)
        self.assertTrue(str(result[first_runner]) == "Усэйн")
        self.assertTrue(str(result[last_runner]) == "Ник")