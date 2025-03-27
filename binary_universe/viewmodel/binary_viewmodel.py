import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.binary_model import BinaryUniverseModel

class BinaryUniverseViewModel:
    """二进制宇宙视图模型，连接模型层和视图层 [核心理论版本号：1.0]"""
    
    def __init__(self, sequence_length: int = 8):
        """
        初始化视图模型
        
        参数:
            sequence_length: 二进制序列长度
        """
        self.model = BinaryUniverseModel(sequence_length)
        self.visualization_mode = "matrix"  # 默认可视化模式
        self.available_modes = ["matrix", "heatmap", "graph", "binary_tree", "quantum_state", "philosophical"]
        self.observers = []  # 用于通知视图更新的观察者列表
        self.active_observer = None  # 当前活动的观察者
        self.philosophical_interpretation = "尚未生成哲学解读" # 哲学解读文本
        self.coherence_degree = 0.5  # 量子相干度（0-1）
        
    def register_observer(self, observer):
        """注册视图观察者"""
        if observer not in self.observers:
            self.observers.append(observer)
            
    def unregister_observer(self, observer):
        """注销视图观察者"""
        if observer in self.observers:
            self.observers.remove(observer)
            
    def notify_observers(self, data: Dict[str, Any] = None):
        """通知所有观察者更新"""
        for observer in self.observers:
            observer.update(data)
            
    def evolve_universe(self, steps: int = 1) -> None:
        """
        演化宇宙状态指定步数
        
        参数:
            steps: 演化步数
        """
        for _ in range(steps):
            # 获取演化前状态
            before_state = self.model.get_current_state().copy()
            before_entropy = self.model.calculate_entropy(before_state)
            
            # 生成哲学解读
            self.philosophical_interpretation = self.model.get_philosophical_meaning(before_state)
            
            # 执行状态演化
            self.model.evolve_state()
            
            # 获取演化后状态
            after_state = self.model.get_current_state()
            after_entropy = self.model.calculate_entropy(after_state)
            
            # 计算熵变化
            entropy_change = self.model.entropy_change(before_state, after_state)
            
            # 检查是否达到奇点并更新数据
            singularity_count, singularity_positions = self.model.get_singularity_info()
            is_singularity = np.all(after_state == 0)
            
            # 如果有观察者，让观察者也演化
            observer_data = None
            if self.active_observer is not None:
                old_observer = self.active_observer.copy()
                self.active_observer, observed_state = self.model.observer_evolution(
                    self.active_observer, after_state
                )
                observer_entropy = self.model.calculate_entropy(self.active_observer)
                observer_data = {
                    "observer_state": self.active_observer,
                    "observer_entropy": observer_entropy,
                    "observation_result": self.model.observation_process(self.active_observer, after_state)
                }
            
            # 更新量子态
            quantum_state = self.model.classical_to_quantum(after_state, self.coherence_degree)
            
            # 根据数据情况自动选择可视化方式
            self._auto_select_visualization_mode()
            
            # 准备通知数据
            notification_data = {
                "current_state": after_state.copy(),
                "state_history": self.model.get_state_history(),
                "before_entropy": before_entropy,
                "after_entropy": after_entropy,
                "entropy_change": entropy_change,
                "singularity_count": singularity_count,
                "singularity_positions": singularity_positions,
                "is_singularity": is_singularity,
                "visualization_mode": self.visualization_mode,
                "observer_data": observer_data,
                "quantum_state": quantum_state,
                "philosophical_interpretation": self.philosophical_interpretation
            }
            
            # 通知观察者更新
            self.notify_observers(notification_data)
            
    def reset_universe(self, sequence_length: int = None, initial_state: np.ndarray = None) -> None:
        """
        重置宇宙状态
        
        参数:
            sequence_length: 可选，新的序列长度
            initial_state: 可选，指定的初始状态
        """
        self.model.reset(sequence_length, initial_state)
        self.active_observer = None
        
        # 更新可视化方式
        self._auto_select_visualization_mode()
        
        # 生成哲学解读
        self.philosophical_interpretation = self.model.get_philosophical_meaning()
        
        # 准备通知数据
        notification_data = {
            "current_state": self.model.get_current_state().copy(),
            "state_history": self.model.get_state_history(),
            "before_entropy": None,
            "after_entropy": self.model.calculate_entropy(),
            "entropy_change": None,
            "singularity_count": 0,
            "singularity_positions": [],
            "is_singularity": False,
            "visualization_mode": self.visualization_mode,
            "observer_data": None,
            "quantum_state": self.model.classical_to_quantum(self.model.get_current_state(), self.coherence_degree),
            "philosophical_interpretation": self.philosophical_interpretation
        }
        
        # 通知观察者更新
        self.notify_observers(notification_data)
        
    def _auto_select_visualization_mode(self) -> None:
        """根据数据情况自动选择可视化方式"""
        
        # 获取当前数据
        state_history = self.model.get_state_history()
        state_count = len(state_history)
        
        # 根据历史状态数量选择可视化方式
        if state_count < 10:
            self.visualization_mode = "matrix"  # 状态少时直观显示矩阵
        elif state_count < 50:
            self.visualization_mode = "heatmap"  # 中等数量使用热图
        else:
            self.visualization_mode = "graph"  # 大量数据使用图表
            
        # 如果出现奇点，考虑使用二叉树模式
        singularity_count, _ = self.model.get_singularity_info()
        if singularity_count > 0:
            sequence_length = self.model.sequence_length
            if sequence_length <= 16:  # 二叉树可视化适合较小的序列
                self.visualization_mode = "binary_tree"
                
    def set_visualization_mode(self, mode: str) -> bool:
        """
        手动设置可视化模式
        
        参数:
            mode: 可视化模式名称
            
        返回:
            是否设置成功
        """
        if mode in self.available_modes:
            self.visualization_mode = mode
            return True
        return False
    
    def set_coherence_degree(self, degree: float) -> None:
        """
        设置量子相干度
        
        参数:
            degree: 相干度(0-1)
        """
        self.coherence_degree = max(0.0, min(1.0, degree))
        
    def create_observer(self) -> np.ndarray:
        """
        创建观察者
        
        返回:
            观察者状态
        """
        self.active_observer = self.model.create_observer()
        return self.active_observer
    
    def remove_observer(self) -> None:
        """移除当前观察者"""
        self.active_observer = None
        
    def get_model_data(self) -> Dict[str, Any]:
        """
        获取模型数据用于可视化
        
        返回:
            模型数据字典
        """
        current_state = self.model.get_current_state()
        state_history = self.model.get_state_history()
        singularity_count, singularity_positions = self.model.get_singularity_info()
        
        # 创建观察者数据
        observer_data = None
        if self.active_observer is not None:
            observer_entropy = self.model.calculate_entropy(self.active_observer)
            observer_data = {
                "observer_state": self.active_observer,
                "observer_entropy": observer_entropy,
                "observation_result": self.model.observation_process(self.active_observer, current_state)
            }
        
        return {
            "current_state": current_state,
            "state_history": state_history,
            "current_entropy": self.model.calculate_entropy(),
            "singularity_count": singularity_count,
            "singularity_positions": singularity_positions,
            "visualization_mode": self.visualization_mode,
            "sequence_length": self.model.sequence_length,
            "observer_data": observer_data,
            "quantum_state": self.model.classical_to_quantum(current_state, self.coherence_degree),
            "philosophical_interpretation": self.philosophical_interpretation,
            "coherence_degree": self.coherence_degree
        }
        
    def execute_quantum_classical_experiment(self) -> Dict[str, Any]:
        """
        执行量子经典二元映射实验
        
        返回:
            实验结果数据
        """
        current_state = self.model.get_current_state()
        
        # 经典到量子映射
        quantum_amplitudes = self.model.classical_to_quantum(current_state, self.coherence_degree)
        
        # 量子到经典映射（无观察者）
        classical_state_no_observer = self.model.quantum_to_classical(quantum_amplitudes)
        
        # 量子到经典映射（有观察者）
        if self.active_observer is None:
            self.create_observer()
        classical_state_with_observer = self.model.quantum_to_classical(quantum_amplitudes, self.active_observer)
        
        # 检查统一表示定理
        unified_representation = np.array_equal(
            self.model.quantum_to_classical(
                self.model.classical_to_quantum(classical_state_no_observer, self.coherence_degree)
            ),
            classical_state_no_observer
        )
        
        # 量子干涉实验
        random_state = np.random.randint(0, 2, self.model.sequence_length)
        interference_amplitudes = self.model.quantum_interference(current_state, random_state)
        interference_result = self.model.quantum_to_classical(interference_amplitudes)
        
        # 量子退相干实验
        environment = np.random.randint(0, 2, self.model.sequence_length)
        decoherence_amplitudes = self.model.quantum_decoherence(quantum_amplitudes, environment)
        decoherence_result = self.model.quantum_to_classical(decoherence_amplitudes)
        
        return {
            "original_state": current_state,
            "quantum_amplitudes": quantum_amplitudes,
            "classical_state_no_observer": classical_state_no_observer,
            "classical_state_with_observer": classical_state_with_observer,
            "unified_representation_theorem": unified_representation,
            "observer_state": self.active_observer,
            "interference_state": random_state,
            "interference_amplitudes": interference_amplitudes,
            "interference_result": interference_result,
            "environment_state": environment,
            "decoherence_amplitudes": decoherence_amplitudes,
            "decoherence_result": decoherence_result,
            "coherence_degree": self.coherence_degree
        }
        
    def execute_observer_experiment(self, steps: int = 5) -> Dict[str, Any]:
        """
        执行观察者实验
        
        参数:
            steps: 观察步骤数
            
        返回:
            实验结果数据
        """
        # 初始化观察者和被观察对象
        if self.active_observer is None:
            self.create_observer()
        observer = self.active_observer.copy()
        observed = self.model.get_current_state().copy()
        
        observer_history = [observer.copy()]
        observed_history = [observed.copy()]
        observation_results = [self.model.observation_process(observer, observed)]
        observer_entropy_history = [self.model.calculate_entropy(observer)]
        observed_entropy_history = [self.model.calculate_entropy(observed)]
        
        # 执行多步观察
        for _ in range(steps):
            observer, observed = self.model.observer_evolution(observer, observed)
            observer_history.append(observer.copy())
            observed_history.append(observed.copy())
            observation_results.append(self.model.observation_process(observer, observed))
            observer_entropy_history.append(self.model.calculate_entropy(observer))
            observed_entropy_history.append(self.model.calculate_entropy(observed))
        
        # 更新活动观察者为最终状态
        self.active_observer = observer_history[-1].copy()
        
        return {
            "observer_history": observer_history,
            "observed_history": observed_history,
            "observation_results": observation_results,
            "observer_entropy_history": observer_entropy_history,
            "observed_entropy_history": observed_entropy_history
        }
    
    def get_recursive_simplification_path(self) -> Dict[str, Any]:
        """
        获取当前状态的递归简化路径
        
        返回:
            简化路径数据
        """
        current_state = self.model.get_current_state()
        simplified_state, steps, path = self.model.recursive_simplification(current_state)
        
        # 计算每一步的熵变化
        entropy_path = [self.model.calculate_entropy(state) for state in path]
        
        # 检查是否达到奇点
        reached_singularity = np.all(simplified_state == 0)
        
        return {
            "simplification_path": path,
            "entropy_path": entropy_path,
            "steps_to_singularity": steps,
            "reached_singularity": reached_singularity,
            "philosophical_interpretation": self.model.get_philosophical_meaning(simplified_state)
        }
    
    def get_philosophical_analysis(self) -> Dict[str, Any]:
        """
        获取当前状态的哲学分析
        
        返回:
            哲学分析数据
        """
        current_state = self.model.get_current_state()
        entropy = self.model.calculate_entropy(current_state)
        self_reference = self.model.self_reference(current_state)
        is_singularity = np.all(current_state == 0)
        
        # 更新哲学解读
        self.philosophical_interpretation = self.model.get_philosophical_meaning(current_state)
        
        # 检查如果当前状态进行递归简化，需要多少步到达奇点
        _, steps_to_singularity, _ = self.model.recursive_simplification(current_state)
        
        return {
            "current_state": current_state,
            "entropy": entropy,
            "self_reference_result": self_reference,
            "is_singularity": is_singularity,
            "steps_to_singularity": steps_to_singularity,
            "philosophical_interpretation": self.philosophical_interpretation,
            "entropy_percentage": entropy / self.model.sequence_length * 100
        } 