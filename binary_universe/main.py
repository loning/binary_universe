"""
二进制宇宙模拟 [核心理论版本号：1.0]
基于二进制宇宙理论的模拟程序，使用MVVM架构

本程序严格实现了二进制宇宙理论的所有公理：
1. 二进制宇宙基元公理：宇宙的所有状态均由二进制比特表达
2. XOR演化公理：宇宙的演化唯一由二进制异或运算控制
3. 递归结构公理：宇宙的整体结构为递归定义，可表示为 U_{t+1} = XOR(U_t, F(U_t))
4. 量子经典域统一公理：量子态与经典态在本质上是同构的，可通过XOR互相转换
5. 观察者与观测公理：观察者为宇宙的自参照子模式，观测过程是XOR操作
6. 自参照与递归性公理：任何状态对自身异或得到奇点，表现为绝对同一性
"""

import sys
import os
import locale
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLocale, QTranslator, QCoreApplication
from view.binary_view import BinaryUniverseView
from viewmodel.binary_viewmodel import BinaryUniverseViewModel

def main():
    """主程序入口"""
    # 设置系统默认编码为UTF-8
    try:
        # Windows平台需要设置控制台编码
        if sys.platform.startswith('win'):
            import codecs
            # 设置控制台输出编码
            if sys.stdout.encoding != 'UTF-8':
                sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            if sys.stderr.encoding != 'UTF-8':
                sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass
        
    # 尝试设置系统locale为中文
    try:
        if sys.platform.startswith('win'):
            locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
        elif sys.platform.startswith('darwin'):  # macOS
            locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
        else:  # Linux等其他系统
            locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    except:
        # 如果失败，使用系统默认设置
        locale.setlocale(locale.LC_ALL, '')
    
    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 设置Qt应用程序的locale
    chinese_locale = QLocale(QLocale.Chinese, QLocale.China)
    QLocale.setDefault(chinese_locale)
    
    # 尝试加载中文翻译（如果存在）
    translator = QTranslator(app)
    QCoreApplication.installTranslator(translator)
    
    print("启动二进制宇宙模拟器 [核心理论版本号：1.0]")
    print("实现了全部6个公理的严格形式化模拟")
    
    # 创建视图模型实例
    viewmodel = BinaryUniverseViewModel(sequence_length=8)
    
    # 创建视图实例
    view = BinaryUniverseView(viewmodel)
    
    # 显示视图
    view.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 