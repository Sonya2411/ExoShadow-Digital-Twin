import unittest
from unittest.mock import MagicMock
from models import TelemetryFrame, Vector3
from engine import ShadowEngine
from strategies import GaitSymmetryStrategy, HeartRateAnalysisStrategy

class TestExoShadowSystem(unittest.TestCase):

    def setUp(self):
        # Инициализация стратегий для тестов
        self.symmetry_strategy = GaitSymmetryStrategy()
        self.hr_strategy = HeartRateAnalysisStrategy()
        # Создаем движок с набором стратегий
        self.engine = ShadowEngine(strategies=[self.symmetry_strategy, self.hr_strategy])

    def test_gait_symmetry_boundary_conditions(self):
        """Тест граничных условий для симметрии походки (Пункт 4 описания)"""
        # 1. Случай нормы: разница 5 градусов (порог 18)
        frame_ok = TelemetryFrame(
            timestamp=1.0, servo_angles=[20.0, 25.0], 
            heart_rate=70, accel_data=Vector3(x=0, y=1, z=0)
        )
        issues_ok = self.symmetry_strategy.check(frame_ok)
        self.assertEqual(len(issues_ok), 0, "Должно быть 0 аномалий при разнице 5°")

        # 2. Случай аномалии: разница 25 градусов (выше порога)
        frame_fail = TelemetryFrame(
            timestamp=2.0, servo_angles=[20.0, 45.0], 
            heart_rate=70, accel_data=Vector3(x=0, y=1, z=0)
        )
        issues_fail = self.symmetry_strategy.check(frame_fail)
        self.assertEqual(len(issues_fail), 1, "Должна быть 1 аномалия при разнице 25°")
        self.assertEqual(issues_fail[0].type, "Асимметрия походки")

    def test_shadow_engine_dependency_injection(self):
        """Тест интеграции и Dependency Injection (Пункты 1-3 описания)"""
        # Создаем мок-объект для имитации репозитория (заглушка)
        mock_repo = MagicMock()
        
        # Данные для теста
        test_frames = [
            TelemetryFrame(
                timestamp=1.0, servo_angles=[20.0, 50.0], 
                heart_rate=160, accel_data=Vector3(x=0, y=1, z=0)
            )
        ]

        # Выполняем анализ через движок
        issues = self.engine.process_session(test_frames)

        # Проверяем, что выявлено 2 аномалии (и пульс, и симметрия)
        self.assertEqual(len(issues), 2)
        
        # Проверяем логику DI: что движок отработал, не упав без БД
        self.assertTrue(any(iss.type == "Кардио-нагрузка" for iss in issues))

if __name__ == '__main__':
    unittest.main()