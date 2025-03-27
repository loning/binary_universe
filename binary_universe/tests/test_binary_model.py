import unittest
import numpy as np
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.binary_model import BinaryUniverseModel

class TestBinaryUniverseModel(unittest.TestCase):
    """测试二进制宇宙模型的核心功能"""
    
    def setUp(self):
        """每个测试方法执行前的设置"""
        # 创建一个序列长度为8的模型实例，初始状态固定，便于测试
        self.model = BinaryUniverseModel(sequence_length=8)
        # 设置一个固定的初始状态，便于测试
        self.model.reset(initial_state=np.array([1, 0, 1, 1, 0, 1, 0, 0], dtype=np.int8))
        
    def test_xor_operation(self):
        """测试XOR操作符公理"""
        # 准备两个测试序列
        seq1 = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        seq2 = np.array([0, 1, 0, 1, 0, 1, 0, 1], dtype=np.int8)
        
        # 期望的XOR结果
        expected = np.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=np.int8)
        
        # 执行XOR操作
        result = self.model.xor_operation(seq1, seq2)
        
        # 验证结果
        np.testing.assert_array_equal(result, expected)
        
        # 测试XOR的性质：a ⊕ a = 0
        self_xor = self.model.xor_operation(seq1, seq1)
        np.testing.assert_array_equal(self_xor, np.zeros_like(seq1))
        
    def test_recursive_reference_function(self):
        """测试递归引用函数"""
        state = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        
        # 测试实现的左移函数
        expected = np.array([0, 1, 0, 1, 0, 1, 0, 1], dtype=np.int8)
        result = self.model.recursive_reference_function(state)
        
        np.testing.assert_array_equal(result, expected)
        
    def test_evolve_state(self):
        """测试状态演化公理：U_{t+1} = XOR(U_t, F(U_t))"""
        # 获取初始状态
        initial_state = self.model.get_current_state()
        
        # 手动计算期望的下一个状态
        mapped_state = self.model.recursive_reference_function(initial_state)
        expected_next_state = self.model.xor_operation(initial_state, mapped_state)
        
        # 执行演化
        self.model.evolve_state()
        
        # 获取实际的下一个状态
        actual_next_state = self.model.get_current_state()
        
        # 验证结果
        np.testing.assert_array_equal(actual_next_state, expected_next_state)
        
    def test_entropy_calculation(self):
        """测试熵的计算"""
        # 测试全0状态的熵为0
        state = np.zeros(8, dtype=np.int8)
        self.assertEqual(self.model.calculate_entropy(state), 0)
        
        # 测试全1状态的熵为序列长度
        state = np.ones(8, dtype=np.int8)
        self.assertEqual(self.model.calculate_entropy(state), 8)
        
        # 测试混合状态的熵
        state = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        self.assertEqual(self.model.calculate_entropy(state), 4)
        
    def test_entropy_change(self):
        """测试熵变化计算"""
        state1 = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        state2 = np.array([0, 1, 0, 1, 0, 1, 0, 1], dtype=np.int8)
        
        # 熵变化应该等于XOR结果的熵
        xor_result = self.model.xor_operation(state1, state2)
        expected_change = self.model.calculate_entropy(xor_result)
        
        actual_change = self.model.entropy_change(state1, state2)
        
        self.assertEqual(actual_change, expected_change)
        
    def test_classical_to_quantum(self):
        """测试经典态到量子态的映射"""
        # 选择一个经典态
        classical_state = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        
        # 测试零相干度（确定态）
        quantum_state_zero = self.model.classical_to_quantum(classical_state, coherence_degree=0.0)
        self.assertEqual(len(quantum_state_zero), 1)  # 只有一个态
        self.assertIn('10101010', quantum_state_zero)  # 原始态应该存在
        
        # 测试最大相干度
        quantum_state_max = self.model.classical_to_quantum(classical_state, coherence_degree=1.0)
        self.assertGreater(len(quantum_state_max), 1)  # 应该有多个态
        self.assertIn('10101010', quantum_state_max)  # 原始态应该存在
        
        # 测试概率归一化
        total_prob = sum(abs(amp)**2 for amp in quantum_state_max.values())
        self.assertAlmostEqual(total_prob, 1.0, places=6)
        
    def test_quantum_to_classical_no_observer(self):
        """测试量子态到经典态的映射（无观察者）"""
        # 创建一个简单的量子态
        classical_state = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        quantum_state = self.model.classical_to_quantum(classical_state, coherence_degree=0.0)
        
        # 没有观察者的情况下，应该返回概率最高的态
        classical_result = self.model.quantum_to_classical(quantum_state)
        
        # 在这种简单情况下，应该返回原始态
        np.testing.assert_array_equal(classical_result, classical_state)
        
    def test_quantum_to_classical_with_observer(self):
        """测试量子态到经典态的映射（有观察者）"""
        # 创建一个简单的量子态
        classical_state = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        quantum_state = self.model.classical_to_quantum(classical_state, coherence_degree=0.5)
        
        # 创建一个观察者
        observer = np.array([0, 1, 0, 1, 0, 1, 0, 1], dtype=np.int8)
        
        # 有观察者的情况下，测量结果应该受观察者的影响
        classical_result = self.model.quantum_to_classical(quantum_state, observer)
        
        # 结果应该是一个有效的二进制序列
        self.assertEqual(len(classical_result), len(classical_state))
        self.assertTrue(all(bit in [0, 1] for bit in classical_result))
        
    def test_quantum_interference(self):
        """测试量子干涉过程"""
        state1 = np.array([1, 0, 0, 0, 0, 0, 0, 0], dtype=np.int8)
        state2 = np.array([0, 1, 0, 0, 0, 0, 0, 0], dtype=np.int8)
        
        interference = self.model.quantum_interference(state1, state2)
        
        # 检查干涉结果是否符合预期
        self.assertIsInstance(interference, dict)
        
        # 干涉态应该包含各种可能的XOR组合
        self.assertGreater(len(interference), 0)
        
        # 概率和应该为1
        total_prob = sum(abs(amp)**2 for amp in interference.values())
        self.assertAlmostEqual(total_prob, 1.0, places=6)
        
    def test_quantum_decoherence(self):
        """测试量子退相干过程"""
        classical_state = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        quantum_state = self.model.classical_to_quantum(classical_state, coherence_degree=0.8)
        
        environment = np.array([1, 1, 1, 1, 0, 0, 0, 0], dtype=np.int8)
        
        decoherence = self.model.quantum_decoherence(quantum_state, environment)
        
        # 检查退相干结果是否符合预期
        self.assertIsInstance(decoherence, dict)
        self.assertEqual(len(decoherence), len(quantum_state))
        
        # 概率和仍应该为1
        total_prob = sum(abs(amp)**2 for amp in decoherence.values())
        self.assertAlmostEqual(total_prob, 1.0, places=6)
        
    def test_observation_process(self):
        """测试观察过程：Obs(O, x) = O ⊕ x"""
        observer = np.array([1, 1, 0, 0, 1, 1, 0, 0], dtype=np.int8)
        observed = np.array([0, 1, 0, 1, 0, 1, 0, 1], dtype=np.int8)
        
        # 期望的观察结果
        expected = np.array([1, 0, 0, 1, 1, 0, 0, 1], dtype=np.int8)
        
        # 执行观察
        result = self.model.observation_process(observer, observed)
        
        # 验证结果
        np.testing.assert_array_equal(result, expected)
        
    def test_observer_evolution(self):
        """测试观察者与被观察对象的演化"""
        observer = np.array([1, 1, 0, 0, 1, 1, 0, 0], dtype=np.int8)
        observed = np.array([0, 1, 0, 1, 0, 1, 0, 1], dtype=np.int8)
        
        # 演化一步
        new_observer, new_observed = self.model.observer_evolution(observer, observed)
        
        # 验证类型和长度
        self.assertEqual(len(new_observer), len(observer))
        self.assertEqual(len(new_observed), len(observed))
        self.assertTrue(all(bit in [0, 1] for bit in new_observer))
        self.assertTrue(all(bit in [0, 1] for bit in new_observed))
        
        # 验证观察者和被观察者都发生了变化
        self.assertTrue(any(new_observer[i] != observer[i] for i in range(len(observer))))
        self.assertTrue(any(new_observed[i] != observed[i] for i in range(len(observed))))
        
    def test_self_reference(self):
        """测试自参照机制：Self(x) = x ⊕ x = 0"""
        state = np.array([1, 0, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        
        # 自参照结果应该是全0向量（奇点）
        expected = np.zeros_like(state)
        result = self.model.self_reference(state)
        
        np.testing.assert_array_equal(result, expected)
        
    def test_recursive_simplification(self):
        """测试递归简化过程"""
        # 一些状态可能需要多步才能简化为全0
        state = np.array([1, 1, 0, 0, 1, 1, 0, 0], dtype=np.int8)
        
        # 执行递归简化
        simplified, steps, path = self.model.recursive_simplification(state)
        
        # 验证最终结果是全0（奇点）
        self.assertTrue(np.all(simplified == 0))
        
        # 验证步骤数大于0
        self.assertGreater(steps, 0)
        
        # 验证路径长度为steps+1（初始状态 + steps步变化）
        self.assertEqual(len(path), steps + 1)
        
        # 验证路径的第一个元素是初始状态
        np.testing.assert_array_equal(path[0], state)
        
        # 验证路径的最后一个元素是全0
        np.testing.assert_array_equal(path[-1], np.zeros_like(state))
        
    def test_philosophical_meaning(self):
        """测试哲学意义解读"""
        # 测试零态（奇点）
        zero_state = np.zeros(8, dtype=np.int8)
        zero_meaning = self.model.get_philosophical_meaning(zero_state)
        self.assertIn("奇点", zero_meaning)
        self.assertIn("绝对同一性", zero_meaning)
        
        # 测试全1态（最大熵）
        ones_state = np.ones(8, dtype=np.int8)
        ones_meaning = self.model.get_philosophical_meaning(ones_state)
        self.assertIn("最大熵态", ones_meaning)
        self.assertIn("不确定性", ones_meaning)
        
        # 测试普通态
        mid_state = np.array([1, 0, 1, 0, 0, 0, 0, 0], dtype=np.int8)
        mid_meaning = self.model.get_philosophical_meaning(mid_state)
        self.assertIn("熵=", mid_meaning)
        
    def test_singularity_detection(self):
        """测试奇点检测和计数"""
        # 初始化时没有奇点
        singularity_count, positions = self.model.get_singularity_info()
        self.assertEqual(singularity_count, 0)
        self.assertEqual(len(positions), 0)
        
        # 将模型状态设置为全0（奇点）并演化一步
        self.model.reset(initial_state=np.zeros(8, dtype=np.int8))
        self.model.evolve_state()
        
        # 确认奇点被检测到
        singularity_count, positions = self.model.get_singularity_info()
        self.assertEqual(singularity_count, 1)
        self.assertEqual(positions, [1])  # 第二步是奇点（索引1）
        
    def test_reset_with_custom_state(self):
        """测试使用自定义状态重置模型"""
        custom_state = np.array([0, 1, 1, 0, 1, 0, 1, 0], dtype=np.int8)
        
        # 重置模型
        self.model.reset(initial_state=custom_state)
        
        # 验证当前状态
        current_state = self.model.get_current_state()
        np.testing.assert_array_equal(current_state, custom_state)
        
        # 验证历史状态只包含初始状态
        history = self.model.get_state_history()
        self.assertEqual(len(history), 1)
        np.testing.assert_array_equal(history[0], custom_state)

if __name__ == '__main__':
    unittest.main() 