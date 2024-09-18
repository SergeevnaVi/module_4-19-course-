import logging
import unittest
from runner_tournament import Runner


logging.basicConfig(level=logging.INFO, filemode='w',
                    filename='runner_tests.log', encoding='UTF-8',
                    format='%(asctime)s | %(levelname)s | %(message)s')

class RunnerTest(unittest.TestCase):
    is_frozen = False

    @unittest.skipIf(False, 'Тесты в этом кейсе заморожены')
    def test_walk(self):
        try:
            runner = Runner('Вася', -10)
            for _ in range(10):
                runner.walk()
            self.assertEqual(runner.distance, 50)
            logging.info('"test_walk" выполнен успешно')
        except ValueError:
            logging.warning("Неверная скорость для Runner", exc_info=True)

    @unittest.skipIf(False, 'Тесты в этом кейсе заморожены')
    def test_run(self):
        try:
            runner = Runner(15, 5)
            for _ in range(10):
                runner.run()
            self.assertEqual(runner.distance, 100)
            logging.info('"test_run" выполнен успешно')
        except TypeError:
            logging.warning("Неверный тип данных для объекта Runner", exc_info=True)

    @unittest.skipIf(False, 'Тесты в этом кейсе заморожены')
    def test_challenge(self):
        runner1 = Runner('Вася', 10)
        runner2 = Runner('Илья', 5)
        for _ in range(10):
            runner1.run()
            runner2.walk()
        self.assertNotEqual(runner1.distance, runner2.distance)


if __name__ == '__main__':
    unittest.main()

    t = Tournament(101, first, second)
    print(t.start())