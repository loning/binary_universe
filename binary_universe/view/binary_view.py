import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager
import networkx as nx
from matplotlib.animation import FuncAnimation
from typing import Dict, Any, List, Optional
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QSpinBox, 
                           QComboBox, QTabWidget, QGridLayout, QSlider)
from PyQt5.QtCore import Qt, pyqtSlot, QTimer
from PyQt5.QtGui import QFont, QFontDatabase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# 用于存储找到的中文字体
CHINESE_FONT = None

# macOS系统上注册额外的中文字体
def register_chinese_fonts():
    global CHINESE_FONT
    
    # 设置默认字体
    try:
        # 尝试设置全局字体
        matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Bitstream Vera Sans',
                                                'Lucida Grande', 'Verdana', 'Geneva', 'Lucid',
                                                'Arial', 'Helvetica', 'Avant Garde', 'sans-serif']
        matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    except:
        pass
        
    # 注册系统字体
    if sys.platform == 'darwin':  # macOS
        try:
            # 典型的macOS中文字体位置
            font_dirs = [
                '/System/Library/Fonts',
                '/Library/Fonts',
                os.path.expanduser('~/Library/Fonts')
            ]
            
            # 尝试找到并加载中文字体
            for font_dir in font_dirs:
                if not os.path.exists(font_dir):
                    continue
                    
                font_files = os.listdir(font_dir)
                for font_file in font_files:
                    if any(name in font_file for name in ['PingFang', 'Heiti', 'Songti', 'Kaiti']):
                        try:
                            font_path = os.path.join(font_dir, font_file)
                            # 创建字体属性
                            CHINESE_FONT = font_manager.FontProperties(fname=font_path)
                            return
                        except:
                            continue
        except Exception as e:
            print(f"查找macOS中文字体时出错: {e}")
    
    elif sys.platform.startswith('win'):  # Windows
        try:
            # Windows 常见中文字体
            for font_name in ['SimHei', 'Microsoft YaHei', 'SimSun', 'FangSong', 'KaiTi']:
                try:
                    CHINESE_FONT = font_manager.FontProperties(family=font_name)
                    return
                except:
                    continue
        except Exception as e:
            print(f"查找Windows中文字体时出错: {e}")
    
    else:  # Linux 和其他系统
        try:
            # Linux 常见中文字体
            for font_name in ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Droid Sans Fallback']:
                try:
                    CHINESE_FONT = font_manager.FontProperties(family=font_name)
                    return
                except:
                    continue
        except Exception as e:
            print(f"查找Linux中文字体时出错: {e}")
    
    # 如果没有找到中文字体，创建默认字体
    try:
        # 尝试使用系统默认字体
        CHINESE_FONT = font_manager.FontProperties()
        print("未找到专用中文字体，使用系统默认字体")
    except:
        print("警告：无法设置任何字体")

# 调用函数注册中文字体
register_chinese_fonts()

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from viewmodel.binary_viewmodel import BinaryUniverseViewModel

# 创建一个自定义的matplotlib画布
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.fig.tight_layout()

class BinaryUniverseView(QMainWindow):
    """二进制宇宙可视化界面"""
    
    def __init__(self, viewmodel=None):
        super().__init__()
        
        if viewmodel is None:
            self.viewmodel = BinaryUniverseViewModel()
        else:
            self.viewmodel = viewmodel
            
        # 使用全局字体
        self.chinese_font = CHINESE_FONT
            
        # 注册为观察者
        self.viewmodel.register_observer(self)
        
        self.init_ui()
        
        # 启动定时器进行自动演化
        self.evolution_timer = QTimer()
        self.evolution_timer.timeout.connect(self.step_evolution)
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('二进制宇宙模拟 [核心理论版本号：1.0]')
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置应用程序默认字体
        app = QApplication.instance()
        if app:
            # 尝试设置系统支持中文的字体
            font_families = ['SimHei', 'Microsoft YaHei', 'SimSun', 'STSong', 'WenQuanYi Micro Hei']
            font_set = False
            
            # 尝试设置字体
            try:
                if sys.platform == 'darwin':  # macOS
                    app_font = QFont(".AppleSystemUIFont")  # macOS系统UI字体
                    app.setFont(app_font)
                    font_set = True
                else:
                    # 获取系统可用字体
                    available_fonts = [f.family() for f in QFontDatabase().families()]
                    for font_name in font_families:
                        if font_name in available_fonts:
                            app_font = QFont(font_name)
                            app.setFont(app_font)
                            font_set = True
                            break
            except Exception as e:
                print(f"设置Qt字体时出错: {e}")
                    
            if not font_set:
                # 尝试使用默认系统字体
                app_font = app.font()
                app.setFont(app_font)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 控制面板
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        # 添加控制按钮
        self.step_btn = QPushButton('单步演化')
        self.step_btn.clicked.connect(self.step_evolution)
        
        self.auto_btn = QPushButton('自动演化')
        self.auto_btn.clicked.connect(self.toggle_auto_evolution)
        self.auto_btn.setCheckable(True)
        
        self.reset_btn = QPushButton('重置宇宙')
        self.reset_btn.clicked.connect(self.reset_universe)
        
        # 序列长度选择器
        length_label = QLabel('序列长度:')
        self.length_spin = QSpinBox()
        self.length_spin.setRange(4, 32)
        self.length_spin.setValue(8)
        self.length_spin.valueChanged.connect(self.on_length_changed)
        
        # 可视化模式选择器
        mode_label = QLabel('可视化模式:')
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(['矩阵', '热图', '图表', '二叉树', '量子态', '哲学视图'])
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)
        
        # 添加实验按钮
        self.quantum_exp_btn = QPushButton('量子-经典实验')
        self.quantum_exp_btn.clicked.connect(self.run_quantum_experiment)
        
        self.observer_exp_btn = QPushButton('观察者实验')
        self.observer_exp_btn.clicked.connect(self.run_observer_experiment)
        
        # 添加观察者控制按钮
        self.create_observer_btn = QPushButton('创建观察者')
        self.create_observer_btn.clicked.connect(self.create_observer)
        
        self.remove_observer_btn = QPushButton('移除观察者')
        self.remove_observer_btn.clicked.connect(self.remove_observer)
        
        # 量子相干度控制
        coherence_label = QLabel('量子相干度:')
        self.coherence_slider = QSlider(Qt.Horizontal)
        self.coherence_slider.setRange(0, 100)
        self.coherence_slider.setValue(50)  # 默认0.5
        self.coherence_slider.valueChanged.connect(self.on_coherence_changed)
        
        # 创建控制面板布局
        control_layout = QHBoxLayout(control_panel)
        
        # 第一行控制按钮
        row1_widget = QWidget()
        row1_layout = QHBoxLayout(row1_widget)
        row1_layout.addWidget(self.step_btn)
        row1_layout.addWidget(self.auto_btn)
        row1_layout.addWidget(self.reset_btn)
        row1_layout.addWidget(length_label)
        row1_layout.addWidget(self.length_spin)
        row1_layout.addWidget(mode_label)
        row1_layout.addWidget(self.mode_combo)
        
        # 第二行控制按钮
        row2_widget = QWidget()
        row2_layout = QHBoxLayout(row2_widget)
        row2_layout.addWidget(self.quantum_exp_btn)
        row2_layout.addWidget(self.observer_exp_btn)
        row2_layout.addWidget(self.create_observer_btn)
        row2_layout.addWidget(self.remove_observer_btn)
        row2_layout.addWidget(coherence_label)
        row2_layout.addWidget(self.coherence_slider)
        
        # 将两行添加到控制面板
        control_layout = QVBoxLayout(control_panel)
        control_layout.addWidget(row1_widget)
        control_layout.addWidget(row2_widget)
        
        # 添加控制面板到主布局
        main_layout.addWidget(control_panel)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        
        # 主视图标签页
        self.main_view_tab = QWidget()
        main_view_layout = QVBoxLayout(self.main_view_tab)
        
        # 添加主可视化画布
        self.main_canvas = MplCanvas(self, width=12, height=6)
        main_view_layout.addWidget(self.main_canvas)
        
        # 状态信息面板
        info_panel = QWidget()
        info_layout = QGridLayout(info_panel)
        
        self.state_label = QLabel('当前状态: ')
        self.entropy_label = QLabel('熵: 0')
        self.singularity_label = QLabel('奇点计数: 0')
        self.steps_label = QLabel('历史步数: 0')
        self.observer_label = QLabel('观察者: 无')
        
        info_layout.addWidget(self.state_label, 0, 0)
        info_layout.addWidget(self.entropy_label, 0, 1)
        info_layout.addWidget(self.singularity_label, 1, 0)
        info_layout.addWidget(self.steps_label, 1, 1)
        info_layout.addWidget(self.observer_label, 2, 0, 1, 2)
        
        main_view_layout.addWidget(info_panel)
        
        # 递归简化标签页
        self.simplification_tab = QWidget()
        simplification_layout = QVBoxLayout(self.simplification_tab)
        
        self.simplification_canvas = MplCanvas(self, width=12, height=6)
        simplification_layout.addWidget(self.simplification_canvas)
        
        self.simplification_btn = QPushButton('计算递归简化路径')
        self.simplification_btn.clicked.connect(self.show_recursive_simplification)
        simplification_layout.addWidget(self.simplification_btn)
        
        # 量子态可视化标签页
        self.quantum_tab = QWidget()
        quantum_layout = QVBoxLayout(self.quantum_tab)
        
        self.quantum_canvas = MplCanvas(self, width=12, height=6)
        quantum_layout.addWidget(self.quantum_canvas)
        
        # 观察者实验标签页
        self.observer_tab = QWidget()
        observer_layout = QVBoxLayout(self.observer_tab)
        
        self.observer_canvas = MplCanvas(self, width=12, height=6)
        observer_layout.addWidget(self.observer_canvas)
        
        # 哲学解读标签页
        self.philosophy_tab = QWidget()
        philosophy_layout = QVBoxLayout(self.philosophy_tab)
        
        self.philosophy_canvas = MplCanvas(self, width=12, height=6)
        philosophy_layout.addWidget(self.philosophy_canvas)
        
        self.philosophy_text = QLabel("哲学解读将在这里显示")
        self.philosophy_text.setWordWrap(True)
        self.philosophy_text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.philosophy_text.setMinimumHeight(100)
        philosophy_layout.addWidget(self.philosophy_text)
        
        # 添加标签页到标签页控件
        self.tab_widget.addTab(self.main_view_tab, "主视图")
        self.tab_widget.addTab(self.simplification_tab, "递归简化")
        self.tab_widget.addTab(self.quantum_tab, "量子状态")
        self.tab_widget.addTab(self.observer_tab, "观察者实验")
        self.tab_widget.addTab(self.philosophy_tab, "哲学解读")
        
        # 添加标签页控件到主布局
        main_layout.addWidget(self.tab_widget)
        
        # 初始渲染
        self.update({})
        
    def update(self, data: Dict[str, Any]):
        """
        实现观察者更新方法，接收视图模型的通知
        
        参数:
            data: 更新数据
        """
        # 获取最新模型数据
        model_data = self.viewmodel.get_model_data()
        
        # 更新UI信息
        current_state = model_data["current_state"]
        self.state_label.setText(f'当前状态: {np.array2string(current_state)}')
        self.entropy_label.setText(f'熵: {model_data["current_entropy"]}')
        self.singularity_label.setText(f'奇点计数: {model_data["singularity_count"]}')
        self.steps_label.setText(f'历史步数: {len(model_data["state_history"]) - 1}')
        
        # 更新观察者信息
        observer_data = model_data.get("observer_data")
        if observer_data:
            observer_state = observer_data["observer_state"]
            observer_entropy = observer_data["observer_entropy"]
            self.observer_label.setText(f'观察者: {np.array2string(observer_state)} (熵: {observer_entropy})')
        else:
            self.observer_label.setText('观察者: 无')
        
        # 更新哲学解读
        if "philosophical_interpretation" in model_data:
            self.philosophy_text.setText(model_data["philosophical_interpretation"])
            
            # 更新哲学视图
            if model_data["visualization_mode"] == "philosophical":
                self._update_philosophical_view(model_data)
        
        # 根据可视化模式更新主视图
        visualization_mode = data.get("visualization_mode", model_data["visualization_mode"])
        self._update_main_view(model_data, visualization_mode)
        
        # 如果当前在量子状态标签页，更新量子态可视化
        if self.tab_widget.currentIndex() == 2:  # 量子状态标签页索引
            self._visualize_quantum_state(model_data.get("quantum_state", {}), model_data)
        
    def _update_main_view(self, data: Dict[str, Any], visualization_mode: str):
        """
        更新主视图
        
        参数:
            data: 模型数据
            visualization_mode: 可视化模式
        """
        # 清除当前图形
        self.main_canvas.axes.clear()
        
        # 获取状态历史
        state_history = data["state_history"]
        
        # 根据不同模式进行可视化
        if visualization_mode == "matrix":
            self._visualize_matrix_mode(state_history, data)
        elif visualization_mode == "heatmap":
            self._visualize_heatmap_mode(state_history, data)
        elif visualization_mode == "graph":
            self._visualize_graph_mode(state_history, data)
        elif visualization_mode == "binary_tree":
            self._visualize_binary_tree_mode(state_history, data)
        elif visualization_mode == "quantum_state":
            self._visualize_quantum_state(data.get("quantum_state", {}), data)
        elif visualization_mode == "philosophical":
            self._update_philosophical_view(data)
            
        # 更新画布
        self.main_canvas.fig.tight_layout()
        self.main_canvas.draw()
        
    def _visualize_matrix_mode(self, state_history: List[np.ndarray], data: Dict[str, Any]):
        """矩阵可视化模式"""
        if not state_history:
            return
            
        # 获取最新的几个状态进行可视化
        max_states = min(10, len(state_history))
        recent_states = state_history[-max_states:]
        
        # 创建一个矩阵视图
        num_states = len(recent_states)
        sequence_length = data["sequence_length"]
        
        # 创建一个二维数组用于显示
        matrix = np.zeros((num_states, sequence_length))
        for i, state in enumerate(recent_states):
            matrix[i] = state
            
        # 绘制矩阵
        self.main_canvas.axes.imshow(matrix, cmap='binary', interpolation='nearest')
        
        # 添加网格线
        self.main_canvas.axes.set_xticks(np.arange(-0.5, sequence_length, 1), minor=True)
        self.main_canvas.axes.set_yticks(np.arange(-0.5, num_states, 1), minor=True)
        self.main_canvas.axes.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        
        # 在每个单元格中央添加文本
        for i in range(num_states):
            for j in range(sequence_length):
                self.main_canvas.axes.text(j, i, str(int(matrix[i, j])), 
                                        ha='center', va='center', color='red')
                
        # 设置轴标签，使用中文字体
        self.main_canvas.axes.set_xlabel('位索引', fontproperties=self.chinese_font)
        self.main_canvas.axes.set_ylabel('时间步 (最近的状态)', fontproperties=self.chinese_font)
        self.main_canvas.axes.set_title('二进制宇宙状态矩阵', fontproperties=self.chinese_font)
        
        # 标记奇点
        for pos in data["singularity_positions"]:
            if pos >= len(state_history) - max_states:
                relative_pos = pos - (len(state_history) - max_states)
                self.main_canvas.axes.axhline(y=relative_pos, color='red', linestyle='-', alpha=0.3)
                self.main_canvas.axes.text(sequence_length/2, relative_pos, '奇点', 
                                        color='red', ha='center', fontsize=12, fontproperties=self.chinese_font)
                
    def _visualize_heatmap_mode(self, state_history: List[np.ndarray], data: Dict[str, Any]):
        """热图可视化模式"""
        if not state_history:
            return
            
        # 最多显示50个状态
        max_states = min(50, len(state_history))
        recent_states = state_history[-max_states:]
        
        # 创建热图数据
        sequence_length = data["sequence_length"]
        matrix = np.zeros((len(recent_states), sequence_length))
        for i, state in enumerate(recent_states):
            matrix[i] = state
            
        # 绘制热图
        im = self.main_canvas.axes.imshow(matrix, cmap='viridis', aspect='auto')
        self.main_canvas.fig.colorbar(im, ax=self.main_canvas.axes, label='状态值')
        
        # 设置轴标签
        self.main_canvas.axes.set_xlabel('位索引', fontproperties=self.chinese_font)
        self.main_canvas.axes.set_ylabel('时间步', fontproperties=self.chinese_font)
        self.main_canvas.axes.set_title('二进制宇宙状态演化热图', fontproperties=self.chinese_font)
        
        # 标记奇点
        for pos in data["singularity_positions"]:
            if pos >= len(state_history) - max_states:
                relative_pos = pos - (len(state_history) - max_states)
                self.main_canvas.axes.axhline(y=relative_pos, color='red', linestyle='-', alpha=0.7)
                
    def _visualize_graph_mode(self, state_history: List[np.ndarray], data: Dict[str, Any]):
        """图表可视化模式"""
        if not state_history:
            return
            
        # 计算每一步的熵
        entropy_history = [np.sum(state) for state in state_history]
        steps = range(len(entropy_history))
        
        # 绘制熵变化
        self.main_canvas.axes.plot(steps, entropy_history, 'b-', label='熵')
        
        # 标记奇点
        for pos in data["singularity_positions"]:
            self.main_canvas.axes.axvline(x=pos, color='red', linestyle='--', alpha=0.7)
            if len(entropy_history) > 0:  # 确保有熵数据
                max_entropy = max(entropy_history) if max(entropy_history) > 0 else 1
                self.main_canvas.axes.text(pos, max_entropy/2, '奇点', 
                                      color='red', ha='center', rotation=90, fontproperties=self.chinese_font)
            
        # 设置轴标签
        self.main_canvas.axes.set_xlabel('时间步', fontproperties=self.chinese_font)
        self.main_canvas.axes.set_ylabel('熵', fontproperties=self.chinese_font)
        self.main_canvas.axes.set_title('二进制宇宙熵演化', fontproperties=self.chinese_font)
        
        # 图例
        if self.chinese_font:
            legend = self.main_canvas.axes.legend(prop=self.chinese_font)
        else:
            legend = self.main_canvas.axes.legend()
        
        # 如果数据点过多，只显示最近的一部分
        if len(steps) > 100:
            self.main_canvas.axes.set_xlim(max(0, len(steps)-100), len(steps))
            
    def _visualize_binary_tree_mode(self, state_history: List[np.ndarray], data: Dict[str, Any]):
        """二叉树可视化模式"""
        if not state_history:
            return
            
        # 创建一个有向图
        G = nx.DiGraph()
        
        # 状态转换为字符串用于图节点
        state_strs = [''.join(map(str, state)) for state in state_history]
        
        # 添加节点
        for i, state_str in enumerate(state_strs):
            # 节点属性：时间步和是否为奇点
            is_singularity = i in data["singularity_positions"]
            G.add_node(state_str, time_step=i, is_singularity=is_singularity)
            
            # 如果不是第一个状态，添加一条边连接前一个状态
            if i > 0:
                G.add_edge(state_strs[i-1], state_str)
                
        # 使用分层布局
        pos = nx.spring_layout(G)
        
        # 绘制节点
        node_colors = []
        for node in G.nodes():
            if G.nodes[node].get('is_singularity', False):
                node_colors.append('red')
            else:
                node_colors.append('skyblue')
                
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500, ax=self.main_canvas.axes)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, arrows=True, ax=self.main_canvas.axes)
        
        # 绘制标签
        nx.draw_networkx_labels(G, pos, font_size=8, ax=self.main_canvas.axes)
        
        # 设置图表标题
        self.main_canvas.axes.set_title('二进制宇宙状态转换图', fontproperties=self.chinese_font)
        self.main_canvas.axes.axis('off')
        
    def _visualize_quantum_state(self, quantum_state: Dict[str, complex], data: Dict[str, Any]):
        """量子态可视化模式"""
        # 清除之前的图形
        self.quantum_canvas.axes.clear()
        
        if not quantum_state:
            self.quantum_canvas.draw()
            return
            
        # 提取量子态数据
        states = list(quantum_state.keys())
        amplitudes = list(quantum_state.values())
        probabilities = [abs(amp)**2 for amp in amplitudes]
        
        # 按概率排序
        sorted_indices = np.argsort(probabilities)[::-1]  # 降序
        top_n = min(10, len(sorted_indices))  # 最多显示前10个状态
        top_indices = sorted_indices[:top_n]
        
        top_states = [states[i] for i in top_indices]
        top_probs = [probabilities[i] for i in top_indices]
        
        # 创建条形图
        positions = range(len(top_states))
        bars = self.quantum_canvas.axes.bar(positions, top_probs, align='center', alpha=0.7)
        
        # 设置颜色，根据相位角着色
        for i, idx in enumerate(top_indices):
            amp = amplitudes[idx]
            phase = np.angle(amp)
            normalized_phase = (phase + np.pi) / (2 * np.pi)  # 归一化到[0,1]
            # 使用HSV色彩空间，相位决定色调
            bars[i].set_color(plt.cm.hsv(normalized_phase))
            
        # 在顶部显示态字符串
        for i, (state, prob) in enumerate(zip(top_states, top_probs)):
            self.quantum_canvas.axes.text(i, prob + 0.02, state, 
                                         ha='center', va='bottom', rotation=45, fontsize=9)
            # 显示概率值
            self.quantum_canvas.axes.text(i, prob/2, f'{prob:.2f}', 
                                         ha='center', va='center', color='white', fontsize=8)
        
        # 设置轴标签
        self.quantum_canvas.axes.set_xlabel('量子态', fontproperties=self.chinese_font)
        self.quantum_canvas.axes.set_ylabel('概率', fontproperties=self.chinese_font)
        title = f'量子态概率分布 (相干度: {data.get("coherence_degree", 0.5):.2f})'
        self.quantum_canvas.axes.set_title(title, fontproperties=self.chinese_font)
        
        # 设置轴刻度
        self.quantum_canvas.axes.set_xticks(positions)
        self.quantum_canvas.axes.set_xticklabels([f'态{i+1}' for i in range(len(top_states))])
        self.quantum_canvas.axes.set_ylim(0, 1.1)
        
        # 添加图例说明相位颜色
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=plt.cm.hsv(0), label='相位 0°'),
            Patch(facecolor=plt.cm.hsv(0.25), label='相位 90°'),
            Patch(facecolor=plt.cm.hsv(0.5), label='相位 180°'),
            Patch(facecolor=plt.cm.hsv(0.75), label='相位 270°')
        ]
        
        if self.chinese_font:
            self.quantum_canvas.axes.legend(handles=legend_elements, prop=self.chinese_font)
        else:
            self.quantum_canvas.axes.legend(handles=legend_elements)
        
        # 更新画布
        self.quantum_canvas.fig.tight_layout()
        self.quantum_canvas.draw()
    
    def _update_philosophical_view(self, data: Dict[str, Any]):
        """哲学视图可视化模式"""
        # 清除之前的图形
        self.philosophy_canvas.axes.clear()
        
        # 从模型获取哲学数据
        philosophical_data = self.viewmodel.get_philosophical_analysis()
        
        current_state = philosophical_data["current_state"]
        entropy = philosophical_data["entropy"]
        entropy_percentage = philosophical_data["entropy_percentage"]
        steps_to_singularity = philosophical_data["steps_to_singularity"]
        is_singularity = philosophical_data["is_singularity"]
        
        # 创建熵和奇点距离的双轴图
        fig = self.philosophy_canvas.fig
        ax1 = self.philosophy_canvas.axes
        
        # 绘制熵仪表盘
        ax1.set_aspect('equal')
        wedge = ax1.pie([entropy_percentage, 100-entropy_percentage], 
                       startangle=90, counterclock=False,
                       colors=['#ff9999', '#eeeeee'], 
                       wedgeprops={'width': 0.3, 'edgecolor': 'w'},
                       radius=1.0)
        
        # 中心显示熵值和奇点距离
        if is_singularity:
            center_text = "奇点状态"
        else:
            center_text = f"熵: {entropy}\n距奇点: {steps_to_singularity}步"
            
        ax1.text(0, 0, center_text, ha='center', va='center', fontproperties=self.chinese_font,
                fontsize=14, fontweight='bold')
        
        # 设置标题
        title = "宇宙状态哲学解析"
        ax1.set_title(title, fontproperties=self.chinese_font, fontsize=16)
        
        # 添加说明文本
        explanation = f"""状态: {np.array2string(current_state)}
熵占比: {entropy_percentage:.1f}%
自参照性: {"已达奇点" if is_singularity else f"距奇点{steps_to_singularity}步"}
"""
        ax1.text(1.1, -0.1, explanation, ha='left', va='center', 
                fontproperties=self.chinese_font, fontsize=10,
                transform=ax1.transAxes)
        
        # 更新哲学解读文本
        if "philosophical_interpretation" in philosophical_data:
            self.philosophy_text.setText(philosophical_data["philosophical_interpretation"])
        
        # 更新画布
        self.philosophy_canvas.fig.tight_layout()
        self.philosophy_canvas.draw()
    
    def step_evolution(self):
        """执行单步演化"""
        self.viewmodel.evolve_universe(1)
        
    def toggle_auto_evolution(self):
        """切换自动演化状态"""
        if self.auto_btn.isChecked():
            # 开始自动演化，每500毫秒一步
            self.evolution_timer.start(500)
            self.auto_btn.setText('停止演化')
        else:
            # 停止自动演化
            self.evolution_timer.stop()
            self.auto_btn.setText('自动演化')
            
    def reset_universe(self):
        """重置宇宙状态"""
        sequence_length = self.length_spin.value()
        self.viewmodel.reset_universe(sequence_length)
        
    def on_length_changed(self, value):
        """序列长度改变回调"""
        # 仅在重置时应用新长度
        pass
        
    def on_mode_changed(self, index):
        """可视化模式改变回调"""
        mode_map = {
            0: "matrix",
            1: "heatmap",
            2: "graph",
            3: "binary_tree",
            4: "quantum_state",
            5: "philosophical"
        }
        
        if index in mode_map:
            self.viewmodel.set_visualization_mode(mode_map[index])
            # 触发更新
            self.update({})
            
    def show_recursive_simplification(self):
        """显示递归简化路径"""
        # 获取递归简化数据
        simplification_data = self.viewmodel.get_recursive_simplification_path()
        path = simplification_data["simplification_path"]
        steps = simplification_data["steps_to_singularity"]
        
        # 清除之前的图形
        self.simplification_canvas.axes.clear()
        
        # 创建一个矩阵视图
        sequence_length = self.viewmodel.model.sequence_length
        num_states = len(path)
        
        # 创建一个二维数组用于显示
        matrix = np.zeros((num_states, sequence_length))
        for i, state in enumerate(path):
            matrix[i] = state
            
        # 绘制矩阵
        self.simplification_canvas.axes.imshow(matrix, cmap='binary', interpolation='nearest')
        
        # 添加网格线
        self.simplification_canvas.axes.set_xticks(np.arange(-0.5, sequence_length, 1), minor=True)
        self.simplification_canvas.axes.set_yticks(np.arange(-0.5, num_states, 1), minor=True)
        self.simplification_canvas.axes.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        
        # 在每个单元格中央添加文本
        for i in range(num_states):
            for j in range(sequence_length):
                self.simplification_canvas.axes.text(j, i, str(int(matrix[i, j])), 
                                        ha='center', va='center', color='red')
                
        # 设置轴标签
        self.simplification_canvas.axes.set_xlabel('位索引', fontproperties=self.chinese_font)
        self.simplification_canvas.axes.set_ylabel('简化步骤', fontproperties=self.chinese_font)
        title = f'递归简化路径 (步数: {steps})'
        self.simplification_canvas.axes.set_title(title, fontproperties=self.chinese_font)
        
        # 更新画布
        self.simplification_canvas.fig.tight_layout()
        self.simplification_canvas.draw()
        
    def run_quantum_experiment(self):
        """运行量子经典实验"""
        # 获取实验数据
        exp_data = self.viewmodel.execute_quantum_classical_experiment()
        
        # 清除之前的图形
        self.quantum_canvas.axes.clear()
        
        # 创建图表布局
        gs = self.quantum_canvas.fig.add_gridspec(2, 2)
        ax1 = self.quantum_canvas.fig.add_subplot(gs[0, 0])  # 原始量子态
        ax2 = self.quantum_canvas.fig.add_subplot(gs[0, 1])  # 观察者测量
        ax3 = self.quantum_canvas.fig.add_subplot(gs[1, 0])  # 量子干涉
        ax4 = self.quantum_canvas.fig.add_subplot(gs[1, 1])  # 量子退相干
        
        # 提取实验数据
        quantum_amplitudes = exp_data["quantum_amplitudes"]
        classical_no_observer = exp_data["classical_state_no_observer"]
        classical_with_observer = exp_data["classical_state_with_observer"]
        interference_result = exp_data["interference_result"]
        decoherence_result = exp_data["decoherence_result"]
        observer_state = exp_data["observer_state"]
        interference_state = exp_data["interference_state"]
        coherence_degree = exp_data["coherence_degree"]
        
        # 绘制原始量子态
        self._plot_quantum_state(ax1, quantum_amplitudes, 
                               "原始量子态", f"相干度: {coherence_degree:.2f}")
        
        # 绘制观察者测量效果
        obs_data = {
            "observer_state": np.array2string(observer_state),
            "no_observer": np.array2string(classical_no_observer),
            "with_observer": np.array2string(classical_with_observer)
        }
        self._plot_observer_measurement(ax2, obs_data, "观察者测量效果")
        
        # 绘制量子干涉效果
        interference_data = {
            "state1": np.array2string(exp_data["original_state"]),
            "state2": np.array2string(interference_state),
            "result": np.array2string(interference_result)
        }
        self._plot_interference(ax3, interference_data, "量子干涉效果")
        
        # 绘制量子退相干效果
        decoherence_data = {
            "environment": np.array2string(exp_data["environment_state"]),
            "before": np.array2string(exp_data["original_state"]),
            "after": np.array2string(decoherence_result)
        }
        self._plot_decoherence(ax4, decoherence_data, "量子退相干效果")
        
        # 更新画布
        self.quantum_canvas.fig.tight_layout()
        self.quantum_canvas.draw()
        
        # 切换到量子实验标签页
        self.tab_widget.setCurrentIndex(2)
    
    def _plot_quantum_state(self, ax, quantum_amplitudes, title, subtitle=""):
        """绘制量子态可视化"""
        if not quantum_amplitudes:
            return
            
        # 提取量子态数据
        states = list(quantum_amplitudes.keys())
        amplitudes = list(quantum_amplitudes.values())
        probabilities = [abs(amp)**2 for amp in amplitudes]
        
        # 按概率排序
        sorted_indices = np.argsort(probabilities)[::-1]  # 降序
        top_n = min(5, len(sorted_indices))  # 最多显示前5个状态
        top_indices = sorted_indices[:top_n]
        
        top_states = [states[i] for i in top_indices]
        top_probs = [probabilities[i] for i in top_indices]
        
        # 创建条形图
        positions = range(len(top_states))
        bars = ax.bar(positions, top_probs, align='center', alpha=0.7)
        
        # 设置颜色，根据相位角着色
        for i, idx in enumerate(top_indices):
            amp = amplitudes[idx]
            phase = np.angle(amp)
            normalized_phase = (phase + np.pi) / (2 * np.pi)  # 归一化到[0,1]
            # 使用HSV色彩空间，相位决定色调
            bars[i].set_color(plt.cm.hsv(normalized_phase))
        
        # 设置轴标签
        ax.set_xlabel('量子态', fontproperties=self.chinese_font)
        ax.set_ylabel('概率', fontproperties=self.chinese_font)
        ax.set_title(f'{title}\n{subtitle}', fontproperties=self.chinese_font)
        
        # 设置轴刻度
        ax.set_xticks(positions)
        ax.set_xticklabels([f'{s[:3]}...' for s in top_states], rotation=45)
        ax.set_ylim(0, 1.0)
    
    def _plot_observer_measurement(self, ax, data, title):
        """绘制观察者测量效果"""
        labels = ['无观察者', '有观察者']
        values = [1, 1]  # 仅用于显示两个条
        
        bars = ax.bar(labels, values, alpha=0.6)
        bars[0].set_color('green')
        bars[1].set_color('orange')
        
        # 添加数据文本
        ax.text(0, 0.8, f"结果: {data['no_observer']}", 
               ha='center', va='center', fontproperties=self.chinese_font)
        ax.text(1, 0.8, f"结果: {data['with_observer']}", 
               ha='center', va='center', fontproperties=self.chinese_font)
        ax.text(0.5, 0.4, f"观察者: {data['observer_state']}", 
               ha='center', va='center', fontproperties=self.chinese_font)
        
        ax.set_ylim(0, 1.2)
        ax.set_title(title, fontproperties=self.chinese_font)
        ax.set_xticklabels(labels, fontproperties=self.chinese_font)
    
    def _plot_interference(self, ax, data, title):
        """绘制量子干涉效果"""
        labels = ['态1', '态2', '干涉结果']
        values = [1, 1, 1]  # 仅用于显示三个条
        
        bars = ax.bar(labels, values, alpha=0.6)
        bars[0].set_color('blue')
        bars[1].set_color('green')
        bars[2].set_color('purple')
        
        # 添加数据文本
        ax.text(0, 0.8, f"{data['state1']}", 
               ha='center', va='center', fontproperties=self.chinese_font)
        ax.text(1, 0.8, f"{data['state2']}", 
               ha='center', va='center', fontproperties=self.chinese_font)
        ax.text(2, 0.8, f"{data['result']}", 
               ha='center', va='center', fontproperties=self.chinese_font)
        
        ax.set_ylim(0, 1.2)
        ax.set_title(title, fontproperties=self.chinese_font)
        ax.set_xticklabels(labels, fontproperties=self.chinese_font)
    
    def _plot_decoherence(self, ax, data, title):
        """绘制量子退相干效果"""
        labels = ['退相干前', '环境', '退相干后']
        values = [1, 1, 1]  # 仅用于显示三个条
        
        bars = ax.bar(labels, values, alpha=0.6)
        bars[0].set_color('blue')
        bars[1].set_color('yellow')
        bars[2].set_color('red')
        
        # 添加数据文本
        ax.text(0, 0.8, f"{data['before']}", 
               ha='center', va='center', fontproperties=self.chinese_font)
        ax.text(1, 0.8, f"{data['environment']}", 
               ha='center', va='center', fontproperties=self.chinese_font)
        ax.text(2, 0.8, f"{data['after']}", 
               ha='center', va='center', fontproperties=self.chinese_font)
        
        ax.set_ylim(0, 1.2)
        ax.set_title(title, fontproperties=self.chinese_font)
        ax.set_xticklabels(labels, fontproperties=self.chinese_font)
    
    def run_observer_experiment(self):
        """运行观察者实验"""
        # 获取实验数据
        exp_data = self.viewmodel.execute_observer_experiment()
        
        # 清除之前的图形
        self.observer_canvas.axes.clear()
        
        # 获取数据
        observer_history = exp_data["observer_history"]
        observed_history = exp_data["observed_history"]
        
        # 创建两个子图
        gs = self.observer_canvas.fig.add_gridspec(2, 1)
        ax1 = self.observer_canvas.fig.add_subplot(gs[0, 0])
        ax2 = self.observer_canvas.fig.add_subplot(gs[1, 0])
        
        # 计算每一步的熵
        observer_entropy = [np.sum(state) for state in observer_history]
        observed_entropy = [np.sum(state) for state in observed_history]
        steps = range(len(observer_history))
        
        # 绘制观察者熵变化
        ax1.plot(steps, observer_entropy, 'b-', label='观察者熵')
        ax1.set_ylabel('熵', fontproperties=self.chinese_font)
        ax1.set_title('观察者熵演化', fontproperties=self.chinese_font)
        if self.chinese_font:
            ax1.legend(prop=self.chinese_font)
        else:
            ax1.legend()
        
        # 绘制被观察者熵变化
        ax2.plot(steps, observed_entropy, 'r-', label='被观察者熵')
        ax2.set_xlabel('时间步', fontproperties=self.chinese_font)
        ax2.set_ylabel('熵', fontproperties=self.chinese_font)
        ax2.set_title('被观察者熵演化', fontproperties=self.chinese_font)
        if self.chinese_font:
            ax2.legend(prop=self.chinese_font)
        else:
            ax2.legend()
        
        # 更新画布
        self.observer_canvas.fig.tight_layout()
        self.observer_canvas.draw()
        
    def on_coherence_changed(self, value):
        """量子相干度改变回调"""
        # 将滑块值(0-100)转换为相干度(0-1)
        coherence = value / 100.0
        self.viewmodel.set_coherence_degree(coherence)
        # 如果在量子态视图中，立即更新
        if self.viewmodel.visualization_mode == "quantum_state":
            self.update({})
    
    def create_observer(self):
        """创建观察者"""
        self.viewmodel.create_observer()
        model_data = self.viewmodel.get_model_data()
        observer_data = model_data.get("observer_data")
        if observer_data:
            observer_state = observer_data["observer_state"]
            observer_entropy = observer_data["observer_entropy"]
            self.observer_label.setText(f'观察者: {np.array2string(observer_state)} (熵: {observer_entropy})')
    
    def remove_observer(self):
        """移除观察者"""
        self.viewmodel.remove_observer()
        self.observer_label.setText('观察者: 无')
        
    def closeEvent(self, event):
        """窗口关闭事件处理"""
        # 停止自动演化
        self.evolution_timer.stop()
        # 注销观察者
        self.viewmodel.unregister_observer(self)
        event.accept() 